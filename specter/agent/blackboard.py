"""Blackboard graph model — state-space search driven by the Fact / Intent dual primitives.

A pentest is modeled as a directed state-space search from origin toward goal:
- Fact:   a confirmed objective fact (a foothold for exploration)
- Intent: a declared exploration direction (a step not yet executed); it starts from one or more Facts and, once concluded, produces a new Fact
- Termination is decided by 'goal reached / exploration frontier exhausted / safety budget', not a fixed number of rounds

This model is a pure data structure, attached to SessionState for persistence and driven by the OODA loop in solver.py.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class IntentStatus(str, Enum):
    OPEN = "open"  # declared, pending exploration
    EXPLORING = "exploring"  # being explored
    CONCLUDED = "concluded"  # concluded, produced a Fact
    ABANDONED = "abandoned"  # explored but did not advance the goal, abandoned


class BoardFact(BaseModel):
    id: str
    description: str
    source: str = ""  # origin (bootstrap / explore:i003 / hint ...)


class BoardIntent(BaseModel):
    id: str
    from_facts: list[str] = Field(default_factory=list)  # starting Fact ids
    description: str
    status: IntentStatus = IntentStatus.OPEN
    result_fact: str | None = None  # Fact id produced once concluded
    note: str = ""  # abandonment reason / note


class ToolCallRecord(BaseModel):
    """Compact record of an executed tool call — prevents repeating the same tool+args across intents."""
    tool: str
    key_args: str = ""
    intent_id: str = ""
    status: int = 0
    note: str = ""


class Blackboard(BaseModel):
    """Fact/Intent graph. Grows from origin toward goal.

    Inspired by Cairn: besides Fact/Intent, it also keeps a **tool_calls execution log**;
    every tool called during explore is recorded here. The context prompts for both Reason and Explore
    include a summary of this log so the LLM can see "what has already been done" and avoid repeating it.
    """

    origin: str = ""
    goal: str = ""
    facts: list[BoardFact] = Field(default_factory=list)
    intents: list[BoardIntent] = Field(default_factory=list)
    tool_calls: list[ToolCallRecord] = Field(default_factory=list)
    completed: bool = False
    complete_reason: str = ""
    fact_seq: int = Field(default=0, exclude=True)
    intent_seq: int = Field(default=0, exclude=True)

    def model_post_init(self, __context: Any) -> None:
        if self.facts and self.fact_seq == 0:
            nums = [int(f.id[1:]) for f in self.facts if f.id[1:].isdigit()]
            self.fact_seq = max(nums) if nums else len(self.facts)
        if self.intents and self.intent_seq == 0:
            nums = [int(i.id[1:]) for i in self.intents if i.id[1:].isdigit()]
            self.intent_seq = max(nums) if nums else len(self.intents)

    # ── Fact ────────────────────────────────────────────────────────
    def add_fact(self, description: str, source: str = "") -> BoardFact:
        self.fact_seq += 1
        fact = BoardFact(id=f"f{self.fact_seq:03d}", description=description.strip(), source=source)
        self.facts.append(fact)
        return fact

    def get_fact(self, fact_id: str) -> BoardFact | None:
        return next((f for f in self.facts if f.id == fact_id), None)

    def fact_ids(self) -> list[str]:
        return [f.id for f in self.facts]

    # ── Intent ──────────────────────────────────────────────────────
    def add_intent(self, description: str, from_facts: list[str] | None = None) -> BoardIntent:
        self.intent_seq += 1
        valid_from = [fid for fid in (from_facts or []) if self.get_fact(fid)]
        intent = BoardIntent(
            id=f"i{self.intent_seq:03d}",
            from_facts=valid_from,
            description=description.strip(),
        )
        self.intents.append(intent)
        return intent

    def get_intent(self, intent_id: str) -> BoardIntent | None:
        return next((i for i in self.intents if i.id == intent_id), None)

    def open_intents(self) -> list[BoardIntent]:
        return [i for i in self.intents if i.status == IntentStatus.OPEN]

    def active_intents(self) -> list[BoardIntent]:
        """Unconcluded Intents (open + exploring), used to judge whether the exploration frontier is exhausted."""
        return [i for i in self.intents if i.status in (IntentStatus.OPEN, IntentStatus.EXPLORING)]

    def claim_intent(self, intent_id: str) -> BoardIntent | None:
        intent = self.get_intent(intent_id)
        if intent and intent.status == IntentStatus.OPEN:
            intent.status = IntentStatus.EXPLORING
        return intent

    def conclude_intent(self, intent_id: str, fact_description: str, source: str = "") -> BoardFact | None:
        """Exploration produced a valuable conclusion → emit a Fact and link it."""
        intent = self.get_intent(intent_id)
        if intent is None:
            return None
        fact = self.add_fact(fact_description, source=source or f"explore:{intent_id}")
        intent.status = IntentStatus.CONCLUDED
        intent.result_fact = fact.id
        return fact

    def abandon_intent(self, intent_id: str, note: str = "") -> BoardIntent | None:
        intent = self.get_intent(intent_id)
        if intent is not None:
            intent.status = IntentStatus.ABANDONED
            if note:
                intent.note = note
        return intent

    def mark_complete(self, reason: str) -> None:
        self.completed = True
        self.complete_reason = reason.strip()

    # ── Tool call memory ───────────────────────────────────────────
    def record_tool_call(
        self, tool: str, key_args: str, intent_id: str = "",
        status: int = 0, note: str = "",
    ) -> None:
        self.tool_calls.append(ToolCallRecord(
            tool=tool, key_args=key_args[:200], intent_id=intent_id,
            status=status, note=note[:120],
        ))
        if len(self.tool_calls) > 200:
            del self.tool_calls[:100]

    def has_called(self, tool: str, key_args: str) -> bool:
        return any(
            tc.tool == tool and tc.key_args == key_args[:200]
            for tc in self.tool_calls
        )

    def tool_call_summary(self, max_lines: int = 40) -> str:
        if not self.tool_calls:
            return ""
        seen: dict[str, str] = {}
        for tc in self.tool_calls:
            key = f"{tc.tool}({tc.key_args})"
            if key not in seen:
                seen[key] = f"  {tc.intent_id or '-'}: {tc.tool}({tc.key_args})" + (
                    f" → {tc.note}" if tc.note else ""
                )
        lines = list(seen.values())[-max_lines:]
        return "\n".join(lines)

    # ── Rendering ───────────────────────────────────────────────────
    def to_prompt_graph(self, *, include_concluded: bool = True) -> str:
        """Render the graph as compact text for the LLM to read (YAML-style)."""
        lines: list[str] = [f"goal: {self.goal or '(unset)'}", f"origin: {self.origin or '(unset)'}"]

        lines.append("facts:")
        if self.facts:
            for fact in self.facts:
                src = f"  ({fact.source})" if fact.source else ""
                lines.append(f"  - {fact.id}: {fact.description}{src}")
        else:
            lines.append("  (none)")

        lines.append("intents:")
        shown = self.intents if include_concluded else self.active_intents()
        if shown:
            for intent in shown:
                frm = f" from={','.join(intent.from_facts)}" if intent.from_facts else ""
                res = f" -> {intent.result_fact}" if intent.result_fact else ""
                note = f"  // {intent.note}" if intent.note else ""
                lines.append(f"  - {intent.id} [{intent.status.value}]{frm}{res}: {intent.description}{note}")
        else:
            lines.append("  (none)")

        tc_summary = self.tool_call_summary(30)
        if tc_summary:
            lines.append("executed_tools (do not repeat an already-executed tool+args):")
            lines.append(tc_summary)

        return "\n".join(lines)

    def get_summary(self) -> dict[str, object]:
        status_counts: dict[str, int] = {}
        for intent in self.intents:
            status_counts[intent.status.value] = status_counts.get(intent.status.value, 0) + 1
        return {
            "completed": self.completed,
            "facts": len(self.facts),
            "intents": len(self.intents),
            "open_intents": len(self.open_intents()),
            "intent_status_counts": status_counts,
            "complete_reason": self.complete_reason,
        }
