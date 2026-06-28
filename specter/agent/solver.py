"""Goal-driven OODA solve loop — replaces the fixed-round workflow with a blackboard graph.

Loop structure (no fixed rounds):
  1. Seed the initial Fact from origin/goal.
  2. REASON: read the whole graph → decide whether the goal is reached / propose new Intents / propose none.
  3. EXPLORE: claim an Intent, actually execute it with tools, and write the confirmed conclusion back as a new Fact.
  4. Termination: goal reached / exploration frontier exhausted (no Intents and Reason proposes none) / safety budget hit.

The safety budget (max_steps) is only a runaway backstop, not a workflow phase counter;
normally the loop ends early on "goal reached" or "frontier exhausted".
"""

from __future__ import annotations

import asyncio
import contextvars
import json
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from specter.agent.blackboard import Blackboard, BoardIntent, IntentStatus
from specter.agent.llm_client import build_chat_completion_kwargs, call_llm_auto
from specter.agent.think_filter import strip_think_tags

# Signals that an exploration step "made progress / confirmed a conclusion" (broad matching, to avoid missing intents with progress)
_ADVANCE_MARKERS = [
    "confirmed",
    "success",
    "obtained",
    "retrieved",
    "extracted",
    "flag{",
    "flag ",
    "bypass succeeded",
    "echoed",
    "vulnerability exists",
    "found",
    "returns 200",
    "returned 200",
    "status: 200",
    "unauthorized",
    "no auth required",
    "endpoint accessible",
    "information disclosure",
    "key finding",
    "major finding",
    "exposed",
    "leak",
    "200 ok",
    "cors",
    "writable",
    "uploadable",
    "downloadable",
    "weak password",
    "injection point",
    "xss",
    "sql inject",
]
# Signals that "this direction is a dead end"
_DEAD_END_MARKERS = [
    "does not exist",
    "not found",
    "unable",
    "fail",
    "dead end",
    "nothing found",
    "no injection",
    "no echo",
    "ruled out",
]
# Negation phrases in a completion reason — used to detect and reject when the model writes "not achieved" into the completion field
_NEGATION_MARKERS = [
    "not reached",
    "not achieved",
    "not recorded",
    "not found",
    "not complete",
    "failed to",
    "not yet",
    "no evidence",
    "insufficient to",
    "cannot prove",
    "cannot confirm",
    "unable to prove",
    "does not satisfy",
]


def _has_negation(text: str) -> bool:
    """Whether the completion reason contains a negation (meaning it was not actually achieved)."""
    return any(m in (text or "") for m in _NEGATION_MARKERS)


_current_worker: contextvars.ContextVar["ExploreWorker | None"] = contextvars.ContextVar(
    "_current_worker", default=None
)


@dataclass
class ExploreWorker:
    intent_id: str
    evidence_buffer: list[str] = field(default_factory=list)
    tc_start: int = 0


class BoardGuard:
    """Serialise mutating Blackboard operations with an asyncio.Lock."""

    def __init__(self, board: Blackboard) -> None:
        self._board = board
        self._lock = asyncio.Lock()

    async def add_fact(self, description: str, source: str = "") -> Any:
        async with self._lock:
            return self._board.add_fact(description, source)

    async def conclude_intent(self, intent_id: str, fact_desc: str, source: str = "") -> Any:
        async with self._lock:
            return self._board.conclude_intent(intent_id, fact_desc, source)

    async def abandon_intent(self, intent_id: str, note: str = "") -> Any:
        async with self._lock:
            return self._board.abandon_intent(intent_id, note)

    async def record_tool_call(self, **kwargs: Any) -> None:
        async with self._lock:
            self._board.record_tool_call(**kwargs)


class IntentStreamSink:
    """Wraps a StreamSink to prefix output with ``[i00x]``."""

    def __init__(self, inner: Any, intent_id: str) -> None:
        self._inner = inner
        self._prefix = f"[{intent_id}] "
        self._first = True

    def on_status(self, message: str) -> None:
        if self._inner:
            self._inner.on_status(f"{self._prefix}{message}")

    def on_thinking_token(self, token: str) -> None:
        if self._inner:
            self._inner.on_thinking_token(token)

    def on_content_token(self, token: str) -> None:
        if self._inner:
            if self._first:
                self._inner.on_content_token(self._prefix)
                self._first = False
            self._inner.on_content_token(token)

    def on_tool_call(self, tool_name: str, args: str) -> None:
        if self._inner:
            self._inner.on_tool_call(f"{self._prefix}{tool_name}", args)

    def on_tool_result(self, result_summary: str) -> None:
        if self._inner:
            self._inner.on_tool_result(result_summary)

    def on_stream_end(self) -> None:
        if self._inner:
            self._inner.on_stream_end()
        self._first = True


@dataclass
class SolveResult:
    completed: bool
    reason: str
    steps: int
    facts: int
    board: Blackboard


# Flags of the form flag{...} / ctfshow{...} / NSSCTF{...}
_FLAG_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]{1,20}\{[^{}\n]{1,200}\}")


def _extract_flags(text: str) -> list[str]:
    """Extract all flag-shaped tokens in the text (deduplicated, order-preserving)."""
    return list(dict.fromkeys(_FLAG_RE.findall(text or "")))


def _goal_wants_flag(goal: str) -> bool:
    g = (goal or "").lower()
    return any(k in g for k in ("flag", "capture the flag", "ctf", "shell", "getshell"))


def _unverified_flags(claim: str, evidence: str) -> list[str]:
    """Return flags claimed in `claim` but not present in the real tool evidence (suspected hallucination)."""
    return [f for f in _extract_flags(claim) if f not in evidence]


def _completion_is_grounded(goal: str, evidence: str) -> tuple[bool, str]:
    """Evidence check for completion: if the goal requires a flag, a flag must have actually appeared in the real tool output."""
    if not _goal_wants_flag(goal):
        return True, ""
    if _extract_flags(evidence):
        return True, ""
    return False, "The goal requires a flag, but no flag appeared in any real tool output; treated as unverified/suspected hallucination"


def _extract_json(text: str) -> Optional[dict]:
    """Robustly extract a single JSON object from an LLM reply."""
    if not text:
        return None
    cleaned = strip_think_tags(text).strip()
    # Strip the ```json ... ``` code fence
    fence = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1)
    # Try directly
    try:
        obj = json.loads(cleaned)
        return obj if isinstance(obj, dict) else None
    except (ValueError, TypeError):
        pass
    # Fallback: grab the first balanced brace block
    start = cleaned.find("{")
    if start < 0:
        return None
    depth = 0
    for idx in range(start, len(cleaned)):
        ch = cleaned[idx]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                with_suppress = cleaned[start : idx + 1]
                try:
                    obj = json.loads(with_suppress)
                    return obj if isinstance(obj, dict) else None
                except (ValueError, TypeError):
                    return None
    return None


async def _structured_call(agent: Any, prompt: str, *, max_tokens: int = 900) -> str:
    """A tool-free structured LLM call (for Reason / Conclude)."""
    client = agent._get_client()
    messages = [{"role": "user", "content": prompt}]
    kwargs = build_chat_completion_kwargs(agent, messages, max_tokens=max_tokens, temperature=0.2)
    response = client.chat.completions.create(**kwargs)
    if response and response.choices:
        return response.choices[0].message.content or ""
    return ""


def _reason_prompt(board: Blackboard, max_intents: int) -> str:
    # Inspired by Cairn reason.md: explicitly list open and abandoned intents to prevent repeat proposals
    open_list = board.open_intents()
    abandoned = [i for i in board.intents if i.status == IntentStatus.ABANDONED]
    concluded = [i for i in board.intents if i.status == IntentStatus.CONCLUDED]

    open_block = ""
    if open_list:
        open_block = "Intents currently OPEN (being explored or awaiting exploration):\n"
        for i in open_list:
            open_block += f"  - {i.id}: {i.description}\n"
        open_block += "If the open intents already cover every valuable direction, do not propose new ones.\n\n"

    abandoned_block = ""
    if abandoned:
        abandoned_block = "Abandoned intents (dead ends or already verified):\n"
        for i in abandoned[-10:]:
            note = f" — {i.note[:60]}" if i.note else ""
            abandoned_block += f"  - {i.id}: {i.description}{note}\n"
        abandoned_block += "⚠ **Never re-propose a direction identical or highly overlapping with the abandoned intents above.** They are proven dead ends.\n\n"

    concluded_block = ""
    if concluded:
        concluded_block = "Concluded intents (with conclusions):\n"
        for i in concluded[-5:]:
            concluded_block += f"  - {i.id} → {i.result_fact}: {i.description}\n"
        concluded_block += "\n"

    return (
        "You are a senior penetration-testing expert. Below is a snapshot of the current task's \"blackboard graph\": facts are confirmed objective facts, "
        "intents are exploration directions. The graph starts from facts and, through intent exploration, derives new facts, gradually approaching the goal.\n\n"
        f"{open_block}{abandoned_block}{concluded_block}"
        "Decide two things: (1) whether the existing facts already satisfy the goal; (2) if not, whether to propose new exploration directions.\n\n"
        "Return only a single JSON object, nothing else:\n"
        '- If the goal is reached: {"complete": true, "reason": "explain why it is reached", "evidence": ["f002"]}'
        "(complete must be the boolean true; evidence must reference the real fact id(s) that prove it, at least one)\n"
        '- If not reached and new directions should be proposed: {"complete": false, "intents": [{"from": ["f001"], "description": "a high-value, independent exploration direction"}]}\n'
        '- If not reached but no new direction is needed now: {"complete": false}\n\n'
        "Rules:\n"
        "- **The complete field can only be the boolean true or false.**\n"
        "- **The completion decision must be based on confirmed objective facts in `facts`**, never on guesses or wishes, and evidence must reference real fact ids.\n"
        "- If a fact is tagged [unverified]/[completion rejected]/suspected hallucination, you must never use it to decide completion.\n"
        "- **Never re-propose a direction identical or highly overlapping with the abandoned intents** — they have been explored and are dead ends.\n"
        "- If there is still an open intent and the current facts reveal no direction more valuable than the open intents, "
        "return {\"complete\": false} (propose nothing new) and let the open intents continue.\n"
        f"- Propose at most {max_intents} high-value, non-overlapping, independently advanceable directions at a time, each focused on a core idea.\n"
        "- Keep each description concise and focused, not verbose; different intents should cover different dimensions.\n\n"
        "## Blackboard graph\n```\n" + board.to_prompt_graph() + "\n```\n"
    )


def _conclude_prompt(board: Blackboard, intent: BoardIntent, evidence: str) -> str:
    return (
        "This is the \"conclusion phase\". It overrides every earlier instruction to keep exploring / keep sending requests / keep waiting for results — stop acting immediately and only summarize.\n"
        "You may summarize only from information **already actually confirmed** in the \"real tool output\"; do not call more tools and do not wait for unfinished results.\n\n"
        "Return only a single JSON object:\n"
        '{"advanced": true/false, "fact": "the newly confirmed objective fact this time (incremental)"}\n\n'
        "## advanced criteria (broad, biased toward true)\n"
        "advanced=true when (**any one** counts as progress):\n"
        "- Found a new accessible endpoint (even just confirming a 200 response)\n"
        "- Confirmed an unauthorized-accessible API (returns data with no token)\n"
        "- Found tech-stack/version/config information (Server header, error-page leak, etc.)\n"
        "- Found a security-configuration issue (CORS wildcard, missing security headers, sensitive path 403, etc.)\n"
        "- Confirmed a vulnerability exists (injection point/XSS/SSRF/file read, etc.)\n"
        "- Obtained a real flag/shell/credential\n\n"
        "advanced=false only when there is **no new finding at all**: every request was 404/timeout/duplicate of known info.\n\n"
        "## Hard rules\n"
        "- fact must be an objective fact **proven by real tool output**, not a plan, guess, or inference.\n"
        "- **Never fabricate a flag/shell/password/data** — if it did not appear in tool output, you cannot claim to have it.\n"
        "- fact records only incremental info; do not repeat what is already in the graph.\n\n"
        f"## Current exploration direction {intent.id}\n{intent.description}\n\n"
        "## Real tool output from this exploration (your only trustworthy source of facts)\n```\n" + (evidence.strip() or "(no tool output)") + "\n```\n\n"
        "## Blackboard graph\n```\n" + board.to_prompt_graph() + "\n```\n"
    )


def _explore_context(board: Blackboard, intent: BoardIntent, step: int, max_rounds: int) -> str:
    from_desc = ""
    if intent.from_facts:
        refs = [board.get_fact(fid) for fid in intent.from_facts]
        from_desc = "\n".join(f"  - {f.id}: {f.description}" for f in refs if f)
        from_desc = f"\nBased on known facts:\n{from_desc}"

    # Executed-tool summary — prevents cross-intent repetition
    tc_summary = board.tool_call_summary(20)
    tc_block = ""
    if tc_summary:
        tc_block = (
            "\n## Already-executed tools (do not call the same tool+args again)\n"
            + tc_summary + "\n"
        )

    # Cairn improvement #5: inject a conclude-override instruction on the last step
    conclude_override = ""
    if step == max_rounds:
        conclude_override = (
            "\n## ⚠ This is the last step — stop exploring immediately and summarize\n"
            "Do not start new tool calls and do not wait for unfinished results.\n"
            "Based on the tool output you have, summarize every objective fact found in this direction.\n\n"
        )

    return (
        f"[Exploration direction {intent.id} · step {step}/{max_rounds}]\n"
        f"goal: {board.goal}\n"
        f"Current direction: {intent.description}{from_desc}\n"
        f"{conclude_override}"
        f"{tc_block}\n"
        "## Execution rules (must follow)\n"
        "1. Actually execute the current direction with tools; every step must have a tool call + response analysis.\n"
        "2. ⚠ Absolutely do not repeat the same tool+args that appear in the \"already-executed tools\" list above.\n"
        "3. ⚠ Fetch each URL only once — if already fetched, analyze the existing result directly.\n"
        "4. If this direction is a dead end, state the reason clearly and stop.\n"
        "\n## Tool-usage chain (choose by target type)\n"
        "Standard web-pentest chain:\n"
        "  (1) js_recon(url=target) — fetch JS to extract endpoints + auto unauthorized probing (**call first**)\n"
        "  (2) dir_enum(url=target) — directory enumeration\n"
        "  (3) space_search(domain=domain) — cyberspace mapping\n"
        "  (4) subdomain_enum(domain=domain) — subdomain enumeration\n"
        "  (5) unauth_test(base_url, endpoints) — unauthorized verification of discovered endpoints\n"
        "  (6) fetch(url, method) — single-request probing (only for specific paths not covered by js_recon/dir_enum)\n"
        "Chrome MCP chain: chrome_navigate → chrome_read_page/chrome_get_web_content → analyze (do not navigate repeatedly)\n"
    )


def _is_duplicate_intent(board: Blackboard, new_desc: str) -> bool:
    """Check whether a new proposal highly overlaps an already-abandoned intent (checks abandoned only, not concluded).

    Only blocks repeating already-failed directions; successful directions can be deepened again on new facts.
    """
    abandoned = [i for i in board.intents if i.status == IntentStatus.ABANDONED]
    if not abandoned:
        return False
    new_lower = new_desc.lower()
    new_words = set(re.findall(r"[a-zA-Z0-9]{2,}", new_lower))
    if len(new_words) < 3:
        return False
    for existing in abandoned:
        old_lower = existing.description.lower()
        old_words = set(re.findall(r"[a-zA-Z0-9]{2,}", old_lower))
        if len(old_words) < 3:
            continue
        overlap = len(new_words & old_words) / max(len(new_words | old_words), 1)
        if overlap > 0.65:
            return True
    return False


async def reason_step(agent: Any, board: Blackboard, max_intents: int) -> dict:
    raw = await _structured_call(agent, _reason_prompt(board, max_intents), max_tokens=1200)
    parsed = _extract_json(raw)
    return parsed or {}


async def explore_step(
    agent: Any,
    board: Blackboard,
    intent: BoardIntent,
    *,
    max_tool_rounds: int,
    evidence_buffer: list[str],
    stream_sink: Any = None,
    skip_context_write: bool = False,
) -> tuple[bool, str]:
    """Actually explore around one Intent; returns (advanced, conclusion-fact description).

    The conclusion phase feeds the model only the "real tool output captured this exploration" as the sole trustworthy fact source, reducing hallucination.
    skip_context_write: in parallel mode, skip writing to agent.context.messages (to avoid cross-writes).
    """
    system_prompt = agent._build_system_prompt(
        agent.context.state.target, auto_mode=True, user_input=intent.description
    )
    evidence_start = len(evidence_buffer)
    tc_start = len(board.tool_calls)
    last_text = ""
    prev_tc_count = tc_start
    no_new_tc_streak = 0
    for step in range(1, max_tool_rounds + 1):
        ctx = _explore_context(board, intent, step, max_tool_rounds)
        text = await call_llm_auto(agent, system_prompt, ctx, stream_sink=stream_sink)
        last_text = text or ""
        if not skip_context_write:
            agent.context.add_assistant_message(f"[Explore {intent.id} step {step}] {last_text}")
        if hasattr(agent, "_finding_parser"):
            agent._finding_parser.parse(last_text)
        lowered = last_text.lower()
        if any(m.lower() in lowered for m in _ADVANCE_MARKERS):
            break
        if any(m in last_text for m in _DEAD_END_MARKERS) and step >= 2:
            break
        # Cairn checkpoint: compare tool_calls count before/after this step — no increase means the model is spinning
        cur_tc_count = len(board.tool_calls)
        if cur_tc_count == prev_tc_count:
            no_new_tc_streak += 1
            if no_new_tc_streak >= 2:
                last_text += "\n[!] Two consecutive steps with no new tool calls (spinning); terminating this direction."
                break
        else:
            # Check whether all calls added this step are repeats (same tool+key_args seen before)
            new_tcs = board.tool_calls[prev_tc_count:]
            all_repeated = all(
                any(old.tool == tc.tool and old.key_args == tc.key_args
                    for old in board.tool_calls[:prev_tc_count])
                for tc in new_tcs
            ) if new_tcs else True
            if all_repeated and step >= 2:
                last_text += "\n[!] All tool calls this step are repeats; terminating this direction."
                break
            no_new_tc_streak = 0
        prev_tc_count = cur_tc_count

    # ── Cairn improvement #2: Conclude phase (see explore-conclude.md) ──────
    # No matter how explore ended (rounds exhausted/advance/dead-end/spinning), enter the conclude phase.
    # conclude summarizes from real tool output, biased toward keeping valuable findings.
    intent_evidence = "\n".join(evidence_buffer[evidence_start:])[-6000:]
    raw = await _structured_call(
        agent, _conclude_prompt(board, intent, intent_evidence), max_tokens=600
    )
    parsed = _extract_json(raw) or {}
    advanced = bool(parsed.get("advanced"))
    fact = str(parsed.get("fact", "")).strip()
    if not fact:
        fact = strip_think_tags(last_text).strip()[:200]

    # ── Cairn improvement #2b: evidence backstop ─────────────────
    # If conclude says advanced=false but the tool output clearly has a 200 response or new finding,
    # force advanced=true (prevents a weak model's conclude from discarding valuable findings).
    if not advanced and intent_evidence:
        evidence_lower = intent_evidence.lower()
        has_data = any(marker in evidence_lower for marker in [
            "status: 200", "200 ok", '"success"', "'success'",
            "unauthorized", "suspected unauthorized", "returned data",
            "endpoint/path", "hit",
        ])
        if has_data and fact:
            advanced = True

    return advanced, fact


async def solve(
    agent: Any,
    *,
    origin: str,
    goal: str,
    hints: Optional[list[str]] = None,
    max_steps: int = 40,
    max_intents: int = 3,
    max_tool_rounds: int = 4,
    max_parallel: int = 1,
    stream_sink: Any = None,
    on_event: Optional[Callable[[str, dict], None]] = None,
) -> SolveResult:
    """Run the goal-driven solve loop until the goal is reached / frontier exhausted / safety budget hit."""
    board = agent.context.state.board
    board.origin = origin or board.origin
    board.goal = goal or board.goal
    guard = BoardGuard(board)

    def emit(kind: str, payload: dict) -> None:
        if on_event is not None:
            on_event(kind, payload)

    # Global evidence buffer — the sole trustworthy evidence source for all flag/completion decisions
    evidence_buffer: list[str] = []
    original_execute = agent._execute_mcp_tool

    async def _recording_execute(tool_name: str, tool_args: dict) -> str:
        import json as _json

        key_args = _json.dumps(tool_args, ensure_ascii=False, sort_keys=True)[:200]
        output = await original_execute(tool_name, tool_args)
        out_str = str(output)

        worker = _current_worker.get()
        if worker is not None:
            worker.evidence_buffer.append(out_str)
            if len(worker.evidence_buffer) > 400:
                del worker.evidence_buffer[:200]
            intent_id = worker.intent_id
        else:
            intent_id = ""

        evidence_buffer.append(out_str)
        if len(evidence_buffer) > 400:
            del evidence_buffer[:200]

        status = 0
        if "Status: 200" in out_str:
            status = 200
        elif "Status: 403" in out_str:
            status = 403
        elif "Status: 404" in out_str:
            status = 404
        note = out_str[:100].replace("\n", " ")
        await guard.record_tool_call(
            tool=tool_name, key_args=key_args,
            intent_id=intent_id, status=status, note=note,
        )
        return output

    agent._execute_mcp_tool = _recording_execute  # type: ignore[method-assign]

    try:
        # Seed the initial fact
        if not board.facts:
            seed = f"origin={origin}; goal={goal}"
            if hints:
                seed += "; hints: " + " | ".join(hints)
            board.add_fact(seed, source="origin")

        empty_reason_streak = 0
        consecutive_errors = 0
        complete_reject_streak = 0
        steps = 0

        last_checkpoint = (-1, -1, -1)

        def _graph_checkpoint() -> tuple[int, int, int]:
            return (
                len(board.facts),
                sum(1 for i in board.intents if i.status == IntentStatus.CONCLUDED),
                sum(1 for i in board.intents if i.status == IntentStatus.ABANDONED),
            )

        while steps < max_steps and not board.completed:
            cur_checkpoint = _graph_checkpoint()
            open_intents = board.open_intents()
            skip_reason = (cur_checkpoint == last_checkpoint and open_intents)
            last_checkpoint = cur_checkpoint

            if skip_reason:
                pass
            else:
                try:
                    decision = await reason_step(agent, board, max_intents)
                except Exception as exc:
                    consecutive_errors += 1
                    emit("error", {"phase": "reason", "error": str(exc)})
                    if consecutive_errors >= 3:
                        break
                    continue
                emit("reason", {"decision": decision, "step": steps})

                complete_flag = decision.get("complete")
                if complete_flag is not None and complete_flag is not False:
                    full_evidence = "\n".join(evidence_buffer)
                    reason_text = str(
                        decision.get("reason")
                        or (complete_flag if isinstance(complete_flag, str) else "")
                    ).strip()
                    evidence_ids = [
                        fid for fid in (decision.get("evidence") or []) if board.get_fact(fid)
                    ]
                    grounded, why = _completion_is_grounded(board.goal, full_evidence)
                    fake = _unverified_flags(reason_text, full_evidence)

                    reject_reason: Optional[str] = None
                    if complete_flag is not True:
                        reject_reason = "Completion did not use explicit complete=true; treated as not achieved"
                    elif not reason_text:
                        reject_reason = "Completion claim is missing a reason"
                    elif _has_negation(reason_text):
                        reject_reason = f"Completion reason contains a negation, so it is not actually achieved: {reason_text[:80]}"
                    elif not evidence_ids:
                        reject_reason = "Completion claim references no confirmed fact as evidence"
                    elif not grounded:
                        reject_reason = why
                    elif fake:
                        reject_reason = f"The flag {fake[0]} referenced in the completion claim did not appear in real tool output"

                    if reject_reason is None:
                        board.mark_complete(reason_text)
                        emit("completed", {"reason": reason_text})
                        break
                    board.add_fact(f"[completion rejected] {reject_reason}; keep exploring to verify", source="verify")
                    emit("complete_rejected", {"reason": reject_reason})
                    complete_reject_streak += 1
                    if complete_reject_streak >= 3:
                        break
                    continue
                complete_reject_streak = 0

                for item in decision.get("intents") or []:
                    desc = (item or {}).get("description", "").strip() if isinstance(item, dict) else ""
                    if not desc:
                        continue
                    if _is_duplicate_intent(board, desc):
                        continue
                    board.add_intent(desc, (item or {}).get("from"))

                open_intents = board.open_intents()
                if not open_intents:
                    empty_reason_streak += 1
                    if empty_reason_streak >= 3:
                        break
                    continue
                empty_reason_streak = 0

            # ── Select an intent batch to explore ─────────────────────
            open_intents = board.open_intents()
            if not open_intents:
                empty_reason_streak += 1
                if empty_reason_streak >= 3:
                    break
                continue
            empty_reason_streak = 0

            batch = open_intents[:max_parallel]
            is_parallel = len(batch) > 1 and max_parallel > 1

            for intent in batch:
                board.claim_intent(intent.id)
                emit("explore_start", {"intent_id": intent.id, "description": intent.description})

            if is_parallel:
                results = await _explore_batch(
                    agent, board, batch,
                    max_tool_rounds=max_tool_rounds,
                    evidence_buffer=evidence_buffer,
                    stream_sink=stream_sink,
                )
            else:
                intent = batch[0]
                worker = ExploreWorker(intent_id=intent.id, evidence_buffer=list(evidence_buffer), tc_start=len(board.tool_calls))
                _current_worker.set(worker)
                try:
                    advanced, fact = await explore_step(
                        agent, board, intent,
                        max_tool_rounds=max_tool_rounds,
                        evidence_buffer=worker.evidence_buffer,
                        stream_sink=stream_sink,
                    )
                except Exception as exc:
                    advanced, fact = False, ""
                    results = [(intent, False, f"exploration error: {exc}", True)]
                else:
                    results = [(intent, advanced, fact, False)]
                finally:
                    _current_worker.set(None)
                    evidence_buffer.extend(
                        e for e in worker.evidence_buffer if e not in evidence_buffer
                    )

            any_error = False
            for intent, advanced, fact, is_error in results:
                if is_error:
                    consecutive_errors += 1
                    board.abandon_intent(intent.id, note=fact[:120])
                    emit("error", {"phase": "explore", "intent_id": intent.id, "error": fact})
                    any_error = True
                    continue
                consecutive_errors = 0

                full_evidence = "\n".join(evidence_buffer)
                fake_flags = _unverified_flags(fact, full_evidence)
                if fake_flags:
                    note = f"Claimed flag {fake_flags[0]} but it did not appear in any real tool output; judged a hallucination and rejected"
                    board.abandon_intent(intent.id, note=note)
                    board.add_fact(f"[unverified] explore {intent.id}: {note}", source="verify")
                    emit("hallucination", {"intent_id": intent.id, "flags": fake_flags})
                elif advanced and fact:
                    new_fact = board.conclude_intent(intent.id, fact)
                    emit(
                        "conclude",
                        {"intent_id": intent.id, "fact": new_fact.id if new_fact else "", "desc": fact},
                    )
                    captured = _extract_flags(fact)
                    if captured and _goal_wants_flag(board.goal):
                        board.mark_complete(
                            f"Verified and obtained flag from {new_fact.id if new_fact else 'fact'}: {captured[0]}"
                        )
                        emit("completed", {"reason": board.complete_reason})
                        break
                else:
                    board.abandon_intent(intent.id, note=(fact or "no progress")[:120])
                    emit("abandon", {"intent_id": intent.id, "note": fact})

            if board.completed:
                break

            if any_error and consecutive_errors >= 3:
                break

            steps += len(batch)
            agent.context.state.save()

            if is_parallel:
                summaries = []
                for intent, advanced, fact, is_error in results:
                    tag = "✓" if advanced else ("✗ ERR" if is_error else "—")
                    summaries.append(f"[{intent.id} {tag}] {fact[:120]}")
                agent.context.add_assistant_message(
                    "[Parallel exploration summary]\n" + "\n".join(summaries)
                )
    finally:
        agent._execute_mcp_tool = original_execute  # type: ignore[method-assign]

    reason = (
        board.complete_reason
        if board.completed
        else ("exploration frontier exhausted" if steps < max_steps else "safety budget limit reached")
    )
    return SolveResult(
        completed=board.completed,
        reason=reason,
        steps=steps,
        facts=len(board.facts),
        board=board,
    )


async def _explore_batch(
    agent: Any,
    board: Blackboard,
    intents: list[BoardIntent],
    *,
    max_tool_rounds: int,
    evidence_buffer: list[str],
    stream_sink: Any = None,
) -> list[tuple[BoardIntent, bool, str, bool]]:
    """Run multiple intent explorations concurrently via asyncio.gather.

    Returns list of (intent, advanced, fact, is_error) tuples.
    """

    async def _run_one(intent: BoardIntent) -> tuple[BoardIntent, bool, str, bool]:
        worker = ExploreWorker(
            intent_id=intent.id,
            evidence_buffer=list(evidence_buffer),
            tc_start=len(board.tool_calls),
        )
        sink = IntentStreamSink(stream_sink, intent.id) if stream_sink else None
        ctx_token = _current_worker.set(worker)
        try:
            advanced, fact = await explore_step(
                agent, board, intent,
                max_tool_rounds=max_tool_rounds,
                evidence_buffer=worker.evidence_buffer,
                stream_sink=sink,
                skip_context_write=True,
            )
            return (intent, advanced, fact, False)
        except Exception as exc:
            return (intent, False, f"exploration error: {exc}", True)
        finally:
            _current_worker.reset(ctx_token)
            for e in worker.evidence_buffer:
                if e not in evidence_buffer:
                    evidence_buffer.append(e)

    raw = await asyncio.gather(*(_run_one(i) for i in intents), return_exceptions=True)
    results: list[tuple[BoardIntent, bool, str, bool]] = []
    for idx, r in enumerate(raw):
        if isinstance(r, BaseException):
            results.append((intents[idx], False, f"exploration error: {r}", True))
        else:
            results.append(r)
    return results
