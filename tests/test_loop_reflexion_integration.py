import pytest

from specter.agent.context import PentestPhase
from specter.agent.core import AgentCore
from specter.agent.reflexion import FailureCategory
from specter.config.schema import SpecterConfig


def _make_agent(tmp_path, reflexion_enabled=True):
    config = SpecterConfig()
    config.session.output_dir = tmp_path
    config.session.reflexion_enabled = reflexion_enabled
    config.session.reflexion_max_same_vuln_fails = 2
    config.session.reflexion_max_total_no_progress = 5
    return AgentCore(config)


@pytest.mark.asyncio
async def test_consecutive_same_failures_generate_reflexion_prompt(tmp_path, monkeypatch):
    agent = _make_agent(tmp_path, reflexion_enabled=True)
    captured_contexts = []

    from specter.agent import loop_controller

    async def _fake_call_llm_auto(agent_obj, system_prompt, round_context, **kwargs):
        captured_contexts.append(round_context)
        return "Tried sqli payload, ConnectionError request failed."

    monkeypatch.setattr(loop_controller, "call_llm_auto", _fake_call_llm_auto)

    await agent.auto_pentest("Scan example.com for SQL injection vulnerabilities", max_rounds=4)

    assert "🔴 Reflection takeover" in captured_contexts[3]
    assert "Stop repeatedly swapping payloads on the current attack path." in captured_contexts[3]
    assert "Path-switch directive" not in captured_contexts[3]
    assert agent.runtime.same_path_fail_count >= 2


def test_reflexion_disabled_keeps_legacy_same_path_warning(tmp_path):
    agent = _make_agent(tmp_path, reflexion_enabled=False)
    agent.context.state.advance_phase(PentestPhase.VULN_DISCOVERY)
    agent.runtime.same_path_fail_count = 3

    context = agent._build_round_context(5, 5)

    assert "Path-switch directive" in context
    assert "🔴 Reflection takeover" not in context
    assert agent.runtime.same_path_fail_count == 0
    assert agent.runtime.path_switch_forced is True


def test_reflexion_memory_persists_across_cycles(tmp_path):
    """P2-7: persistent cycle retains failure memory across cycles but resets stuck counters."""
    agent = _make_agent(tmp_path, reflexion_enabled=True)

    # cycle 1: accumulate same-category failures
    rx = agent.runtime.reflexion
    for _ in range(2):
        rx.record_attempt(
            path="sqli",
            success=False,
            category=FailureCategory.ENV_CONSTRAINT,
            details="WAF blocked",
            vuln_type="sqli",
        )
    assert rx.state.consecutive_failures == 2
    assert rx.state.vuln_type_fail_count == 2

    # end of cycle 1: write snapshot
    agent._save_reflexion_snapshot()
    assert agent.context.state.reflexion_snapshot

    # cycle 2 boundary: rebuild runtime and restore memory
    agent._reset_runtime_state(user_input="[Persistent Cycle 2] continue pentest")
    rx2 = agent.runtime.reflexion

    # memory retained: failed paths still visible
    assert "sqli" in rx2.get_failed_paths()
    # per-cycle stuck counters reset, stall detection restarts
    assert rx2.state.consecutive_failures == 0
    assert rx2.state.vuln_type_fail_count == 0


def test_reflexion_snapshot_skipped_when_disabled(tmp_path):
    """When reflexion_enabled=False, snapshots are not written or restored."""
    agent = _make_agent(tmp_path, reflexion_enabled=False)
    agent.runtime.reflexion.record_attempt(path="sqli", success=False, vuln_type="sqli")
    agent._save_reflexion_snapshot()
    assert agent.context.state.reflexion_snapshot == {}
