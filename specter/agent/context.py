"""Specter session context management — track pentest state across turns."""

from __future__ import annotations

import json
import re
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from pydantic import BaseModel, Field, PrivateAttr

from specter.agent.blackboard import Blackboard
from specter.agent.reasoning_state import ReasoningState


class PentestPhase(str, Enum):
    """Penetration test phases."""

    IDLE = "Idle"
    RECON = "Recon"
    VULN_DISCOVERY = "Vulnerability Discovery"
    EXPLOITATION = "Exploitation"
    POST_EXPLOITATION = "Post-Exploitation"
    REPORTING = "Reporting"


class VulnerabilityFinding(BaseModel):
    """A single vulnerability finding."""

    title: str = Field(description="Vulnerability title")
    severity: str = Field(default="Medium", description="Critical/High/Medium/Low/Info")
    vuln_type: str = Field(default="", description="Vulnerability type (SQLi, XSS, RCE, etc.)")
    description: str = Field(default="", description="Detailed description")
    evidence: str = Field(default="", description="Proof/evidence of the finding")
    cve: Optional[str] = Field(default=None, description="Associated CVE ID")
    remediation: str = Field(default="", description="Fix recommendation")
    poc_script: Optional[str] = Field(default=None, description="Generated PoC script path")
    evidence_level: str = Field(default="L1", description="L1-L4 evidence strength")
    lifecycle_status: str = Field(
        default="candidate",
        description="candidate/pending_verification/verified/rejected/needs_manual_review",
    )

    # ★ Vulnerability verification status tracking
    verified: bool = Field(default=False, description="Whether it has been verified by PoC")
    verification_status: str = Field(
        default="pending", description="Verification status: pending/verified/rejected"
    )
    verified_at: Optional[str] = Field(default=None, description="Verification timestamp")
    verification_note: str = Field(default="", description="Verification note / exclusion reason")

    # ★ Unique vulnerability identifier (used for deduplication)
    finding_id: str = Field(default="", description="Unique finding id: vuln_type + target + location")

    def model_post_init(self, *args, **kwargs) -> None:
        # ★ Vulnerability completeness validation
        # If severity is High/Critical but evidence, vuln_type, remediation are all empty,
        # this is a placeholder finding — warn but allow it.
        if self.severity in ("Critical", "High"):
            if not self.evidence and not self.vuln_type and not self.remediation:
                self.title = f"[Unverified] {self.title}"
                self.description = (
                    "(⚠️ This finding lacks the evidence/vuln_type/remediation fields; "
                    "the LLM reported it without actual test results. Add evidence before "
                    "treating it as a confirmed vulnerability.)"
                    + (f" {self.description}" if self.description else "")
                )

        # ★ Generate the unique identifier
        if not self.finding_id:
            self.finding_id = self._generate_finding_id()
        self._sync_status_fields()

    def _sync_status_fields(self) -> None:
        """Keep lifecycle and evidence metadata consistent with verification state."""
        if self.verified or self.verification_status == "verified":
            self.verified = True
            self.verification_status = "verified"
            self.lifecycle_status = "verified"
            if self.evidence_level in ("", "L1", "L2", "L3"):
                self.evidence_level = "L4"
            return

        if self.verification_status == "rejected":
            self.verified = False
            self.lifecycle_status = "rejected"
            if self.evidence_level in ("", "L1", "L2"):
                self.evidence_level = "L3"
            return

        self.verified = False
        self.verification_status = "pending"
        if self.lifecycle_status == "needs_manual_review":
            if self.evidence_level in ("", "L1"):
                self.evidence_level = "L2"
            return
        if self.lifecycle_status == "candidate":
            self.evidence_level = self.evidence_level or "L1"
            return
        if self.evidence_level in ("", "L1"):
            self.lifecycle_status = "candidate"
            self.evidence_level = "L1"
        else:
            self.lifecycle_status = "pending_verification"

    def mark_manual_review(self, note: str = "", evidence_level: str = "L2") -> None:
        """Mark a finding as requiring manual review."""
        self.verified = False
        self.verification_status = "pending"
        self.lifecycle_status = "needs_manual_review"
        self.evidence_level = evidence_level
        if note:
            self.verification_note = note

    def _generate_finding_id(self) -> str:
        """Generate unique vulnerability identifier for deduplication.

        Key improvement: also checks the evidence field (populated by Layer 2
        auto-detection) in addition to description, since auto-detected findings
        put URLs/paths in evidence, not description.
        """
        location = ""
        # Try description first, then evidence (Layer 2 auto-findings put URLs there)
        for field in (self.description, self.evidence):
            if not field:
                continue
            url_match = re.search(r'https?://[^\s<>"\')\]]+', field)
            if url_match:
                location = url_match.group(0)
                break
            path_match = re.search(r'/[^\s<>"\')\]]+', field)
            if path_match:
                location = path_match.group(0)
                break

        # Use vuln_type as dedup key; location only if non-empty (avoids "SQLi_")
        if location:
            return f"{self.vuln_type}_{location}"[:50]
        return self.vuln_type[:50]

    def mark_verified(self, note: str = "", evidence_level: str = "L4") -> None:
        """Mark the finding as verified."""
        from datetime import datetime

        self.verified = True
        self.verification_status = "verified"
        self.lifecycle_status = "verified"
        self.evidence_level = evidence_level
        self.verified_at = datetime.now().isoformat()
        self.verification_note = note

    def mark_rejected(self, reason: str, evidence_level: str = "L3") -> None:
        """Mark the finding as rejected (false positive)."""
        from datetime import datetime

        self.verified = False
        self.verification_status = "rejected"
        self.lifecycle_status = "rejected"
        self.evidence_level = evidence_level
        self.verified_at = datetime.now().isoformat()
        self.verification_note = reason


class StepStatus(str, Enum):
    """Step execution status."""

    SUCCESS = "success"  # success
    FAILURE = "failure"  # failure
    SKIPPED = "skipped"  # skipped
    INFO = "info"  # informational


class StepRecord(BaseModel):
    """Structured record of a single pentest step.

    Used to generate a readable attack-path summary.
    """

    phase: PentestPhase = Field(description="The phase it belongs to")
    round: int = Field(default=0, description="Round number")
    action: str = Field(default="", description="The action performed (e.g. port scan, vuln probe)")
    target: str = Field(default="", description="Target (IP/URL/path, etc.)")
    result: str = Field(default="", description="Brief result summary")
    status: StepStatus = Field(default=StepStatus.INFO, description="Execution status")
    detail: str = Field(default="", description="Detailed information (optional)")

    def to_summary(self) -> str:
        """Convert to a readable summary line."""
        status_icon = {
            StepStatus.SUCCESS: "✅",
            StepStatus.FAILURE: "❌",
            StepStatus.SKIPPED: "⏭️",
            StepStatus.INFO: "ℹ️",
        }.get(self.status, "")

        result = self.result[:60] + ("..." if len(self.result) > 60 else "")
        return f"{status_icon} Round {self.round}: {self.action} → {result}"

    def to_brief(self) -> str:
        """Convert to a short summary (for list display)."""
        return f"{self.action}: {self.result}"[:80]


class TaskConstraints(BaseModel):
    """Structured hard constraints for an autonomous pentest task."""

    allowed_ports: list[int] = Field(default_factory=list)
    blocked_ports: list[int] = Field(default_factory=list)
    allowed_hosts: list[str] = Field(default_factory=list)
    blocked_hosts: list[str] = Field(default_factory=list)
    allowed_paths: list[str] = Field(default_factory=list)
    blocked_paths: list[str] = Field(default_factory=list)
    allowed_actions: list[str] = Field(default_factory=list)
    blocked_actions: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    strict_mode: bool = Field(default=False)

    def is_empty(self) -> bool:
        return not any(
            [
                self.allowed_ports,
                self.blocked_ports,
                self.allowed_hosts,
                self.blocked_hosts,
                self.allowed_paths,
                self.blocked_paths,
                self.allowed_actions,
                self.blocked_actions,
                self.notes,
                self.strict_mode,
            ]
        )

    def to_prompt_block(self) -> str:
        """Render constraints into a stable prompt block for every round."""
        if self.is_empty():
            return ""

        lines = ["## Current Task Hard Constraints"]
        if self.allowed_ports:
            lines.append(f"- Only allowed test ports: {', '.join(str(p) for p in self.allowed_ports)}")
        if self.blocked_ports:
            lines.append(f"- Forbidden test ports: {', '.join(str(p) for p in self.blocked_ports)}")
        if self.allowed_hosts:
            lines.append(f"- Only allowed test hosts: {', '.join(self.allowed_hosts)}")
        if self.blocked_hosts:
            lines.append(f"- Forbidden test hosts: {', '.join(self.blocked_hosts)}")
        if self.allowed_paths:
            lines.append(f"- Only allowed test paths: {', '.join(self.allowed_paths)}")
        if self.blocked_paths:
            lines.append(f"- Forbidden test paths: {', '.join(self.blocked_paths)}")
        if self.allowed_actions:
            lines.append(f"- Only allowed actions: {', '.join(self.allowed_actions)}")
        if self.blocked_actions:
            lines.append(f"- Forbidden actions: {', '.join(self.blocked_actions)}")
        if self.notes:
            lines.append(f"- Other restrictions: {'; '.join(self.notes)}")
        if self.strict_mode:
            lines.append("- Strict mode: when out of scope, only record — do not actively test or invoke tools.")
        return "\n".join(lines)


class ConstraintViolationEvent(BaseModel):
    """Structured audit event for a blocked constraint violation."""

    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    kind: str = Field(default="constraint_violation")
    code: str = Field(default="", description="Stable violation code")
    severity: str = Field(default="medium", description="low | medium | high")
    source: str = Field(default="", description="command | phase | tool")
    action: str = Field(default="", description="Normalized action name")
    tool_name: str = Field(default="", description="Tool name when source=tool")
    phase: str = Field(default="", description="Current phase label")
    summary: str = Field(default="", description="Human-readable summary")
    detail: str = Field(default="", description="Detailed diagnostic message")


class SessionState(BaseModel):
    """Full session state for a pentest engagement."""

    target: Optional[str] = None
    phase: PentestPhase = PentestPhase.IDLE
    started_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    resume_summary: str = Field(default="", description="Historical-results summary injected on resume")
    resume_meta: dict[str, Any] = Field(default_factory=dict, description="Resume metadata")
    task_constraints: TaskConstraints = Field(default_factory=TaskConstraints)
    constraint_violations: list[str] = Field(default_factory=list)
    constraint_violation_events: list[ConstraintViolationEvent] = Field(default_factory=list)
    reasoning: ReasoningState = Field(default_factory=ReasoningState)
    # Blackboard graph (Fact/Intent) for the goal-driven solver engine, persisted with the session
    board: Blackboard = Field(default_factory=Blackboard)
    # Cross-cycle memory snapshot of the reflexion engine (persistent mode), stored as a dict to avoid a circular import with the reflexion module
    reflexion_snapshot: dict[str, Any] = Field(default_factory=dict)
    findings: list[VulnerabilityFinding] = Field(default_factory=list)
    recon_data: dict[str, Any] = Field(default_factory=dict)
    # ★ Raw step log (backward compatibility)
    executed_steps: list[str] = Field(default_factory=list)
    # ★ Structured step records (used to generate a readable summary)
    step_records: list[StepRecord] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    # ★ Confirmed facts vs unverified assumptions — critical for CTF reasoning
    confirmed_facts: list[str] = Field(default_factory=list, description="Facts confirmed via tool output")
    unverified_assumptions: list[str] = Field(
        default_factory=list, description="Assumptions relied on but not yet verified during reasoning"
    )
    # ★ Recon dimension completion tracking — prevent premature [DONE] in info gathering
    recon_dimensions_completed: dict[str, bool] = Field(
        default_factory=lambda: {
            "server": False,  # Dimension 1: server info (ports/real IP/OS/middleware/database)
            "website": False,  # Dimension 2: website info (architecture/fingerprint/WAF/sensitive dirs/source leak/co-hosted sites/C-segment)
            "domain": False,  # Dimension 3: domain info (WHOIS/ICP filing/subdomains/DNS/cert transparency)
            "personnel": False,  # Dimension 4: personnel info (conditionally triggered — only activated for explicit social-engineering needs)
        },
        description="Completion tracking for the four-dimension recon model",
    )
    recon_dimension4_active: bool = Field(default=False, description="Whether dimension 4 (personnel info) is active")

    # ★ Vulnerability dedup tracking (PrivateAttr is exempt from Pydantic field-naming rules)
    _finding_ids_cache: set[str] = PrivateAttr(default_factory=set)

    # Semantic-dedup similarity threshold (above this counts as a different wording of the same vuln)
    semantic_dedup_threshold: float = Field(
        default=0.75, description="Similarity threshold for semantic dedup (0-1)"
    )

    def add_finding(self, finding: VulnerabilityFinding) -> bool:
        """Add a vulnerability finding with deduplication.

        Deduplication has two layers:
            1. Exact finding_id hash match (fast)
            2. Semantic-similarity match (catches "same vuln, different wording"),
               keeping the one with stronger evidence on a hit

        Returns:
            True if finding was added, False if duplicate (skipped).
        """
        # Generate the finding_id (if not already set)
        if hasattr(finding, "_sync_status_fields"):
            finding._sync_status_fields()
        if not finding.finding_id:
            finding.finding_id = finding._generate_finding_id()

        # Layer 1: exact finding_id dedup
        if finding.finding_id in self._finding_ids_cache:
            print(f"[DEDUP] Skipping duplicate finding: {finding.title} (ID: {finding.finding_id})")
            return False

        # Layer 2: semantic-similarity dedup
        from specter.agent.finding_similarity import (
            _evidence_strength,
            finding_similarity,
        )

        for idx, existing in enumerate(self.findings):
            if finding_similarity(finding, existing) >= self.semantic_dedup_threshold:
                # Semantic duplicate hit: keep the one with stronger evidence
                if _evidence_strength(finding) > _evidence_strength(existing):
                    print(
                        f"[DEDUP-SEM] Semantic duplicate, replacing with stronger-evidence finding: "
                        f"{finding.title} replaces {existing.title}"
                    )
                    self._finding_ids_cache.discard(existing.finding_id)
                    self._finding_ids_cache.add(finding.finding_id)
                    self.findings[idx] = finding
                else:
                    print(f"[DEDUP-SEM] Skipping semantic-duplicate finding: {finding.title}")
                return False

        # Add to the tracking set and list
        self._finding_ids_cache.add(finding.finding_id)
        self.findings.append(finding)
        return True

    def get_verified_findings(self) -> list[VulnerabilityFinding]:
        """Get the list of verified findings.

        Returns only findings with verified=True; unverified ones are excluded.
        """
        return [f for f in self.findings if f.verified]

    def get_rejected_findings(self) -> list[VulnerabilityFinding]:
        """Get the list of rejected findings (false positives)."""
        return [f for f in self.findings if f.verification_status == "rejected"]

    def get_pending_findings(self) -> list[VulnerabilityFinding]:
        """Get the list of findings pending verification."""
        return [f for f in self.findings if f.verification_status == "pending"]

    def get_candidate_findings(self) -> list[VulnerabilityFinding]:
        """Get findings that are still low-confidence candidates."""
        return [f for f in self.findings if f.lifecycle_status == "candidate"]

    def get_pending_verification_findings(self) -> list[VulnerabilityFinding]:
        """Get findings that have some evidence but still need verification."""
        return [f for f in self.findings if f.lifecycle_status == "pending_verification"]

    def get_manual_review_findings(self) -> list[VulnerabilityFinding]:
        """Get findings that require explicit or implicit manual review."""
        return [
            f
            for f in self.findings
            if (
                f.lifecycle_status == "needs_manual_review"
                or (
                    not f.verified
                    and f.verification_status != "rejected"
                    and f.severity in {"Critical", "High"}
                    and f.lifecycle_status in {"candidate", "pending_verification"}
                )
            )
        ]

    def add_recon_subdomain(self, subdomain: str) -> None:
        """Record a discovered subdomain into recon_data['subdomains'].

        The LLM can call this via python_execute when it discovers subdomains
        during the recon phase (dimension 3). Subdomains are displayed in the
        attack surface summary in reports.
        """
        if "subdomains" not in self.recon_data:
            self.recon_data["subdomains"] = []
        if subdomain and subdomain not in self.recon_data["subdomains"]:
            self.recon_data["subdomains"].append(subdomain)

    def add_constraint_violation(self, message: str) -> None:
        """Record a constraint violation audit event."""
        if not message:
            return
        if message not in self.constraint_violations:
            self.constraint_violations.append(message)
        elif self.constraint_violations and self.constraint_violations[-1] != message:
            self.constraint_violations.append(message)

        self.constraint_violations = self.constraint_violations[-20:]

    def add_constraint_violation_event(
        self,
        *,
        source: str,
        action: str = "",
        tool_name: str = "",
        code: str = "",
        severity: str = "medium",
        summary: str,
        detail: str = "",
    ) -> None:
        """Record a structured constraint violation audit event."""
        event = ConstraintViolationEvent(
            source=source,
            action=action,
            tool_name=tool_name,
            code=code,
            severity=severity,
            phase=self.phase.value if hasattr(self.phase, "value") else str(self.phase),
            summary=summary,
            detail=detail or summary,
        )
        self.constraint_violation_events.append(event)
        self.constraint_violation_events = self.constraint_violation_events[-20:]
        self.add_constraint_violation(summary)

    def add_step(
        self,
        step: str,
        action: str = "",
        target: str = "",
        result: str = "",
        status: StepStatus = StepStatus.INFO,
        detail: str = "",
    ) -> None:
        """Record an executed step.

        Args:
            step: Original step string (for backward compatibility).
            action: Short action description (e.g. "port scan", "vuln probe").
            target: Target of the action (e.g. "192.168.1.1:80", "/admin/login").
            result: Brief result summary (e.g. "found 22 open ports").
            status: Execution status.
            detail: Optional detailed information.
        """
        # Keep the raw step (backward compatibility); dedup consecutive entries to avoid title spam polluting the report
        if not self.executed_steps or self.executed_steps[-1] != step:
            self.executed_steps.append(step)
        # Note: step_records creation removed — it was dead code after the return above

        # Create the structured record
        if action:
            record = StepRecord(
                phase=self.phase,
                round=len(self.executed_steps),
                action=action,
                target=target,
                result=result or step[:60],
                status=status,
                detail=detail,
            )
            self.step_records.append(record)

    def get_step_summary(self) -> dict[str, Any]:
        """Generate an attack-path summary.

        Returns:
            A step summary grouped by phase, including key findings.
        """
        # ★ Prefer the structured step_records
        if self.step_records:
            return self._build_step_summary_from_records()

        # ★ Fallback: parse structured info from the raw executed_steps
        if self.executed_steps:
            return self._parse_raw_steps()

        return {"total_steps": 0, "phases": {}, "key_findings": []}

    def _build_step_summary_from_records(self) -> dict[str, Any]:
        """Build a summary from the structured step_records."""
        # Group by phase
        phases: dict[str, list[StepRecord]] = {}
        for record in self.step_records:
            phase_name = record.phase.value
            if phase_name not in phases:
                phases[phase_name] = []
            phases[phase_name].append(record)

        # Generate a summary for each phase
        phase_summaries = {}
        for phase_name, records in phases.items():
            phase_summaries[phase_name] = {
                "count": len(records),
                "actions": list(set(r.action for r in records)),
                "success_count": len([r for r in records if r.status == StepStatus.SUCCESS]),
                "failure_count": len([r for r in records if r.status == StepStatus.FAILURE]),
                "key_results": [r.to_brief() for r in records if r.status == StepStatus.SUCCESS][
                    :5
                ],
            }

        # Extract key findings
        key_findings = [
            r.to_brief() for r in self.step_records if r.status == StepStatus.SUCCESS and r.result
        ][:10]

        return {
            "total_steps": len(self.step_records),
            "phases": phase_summaries,
            "key_findings": key_findings,
        }

    def _parse_raw_steps(self) -> dict[str, Any]:
        """Parse a readable step summary from the raw executed_steps.

        Used when step_records is empty (backward compatibility).
        """
        import re

        # Keyword patterns
        DISCOVERY_KEYWORDS = [
            "found",
            "discover",
            "vuln",
            "port",
            "service",
            "path",
            "leak",
            "confirm",
            "verif",
            "success",
            "connect",
            "accessible",
            "cve",
            "flag",
            "sensitive",
        ]
        FAILURE_KEYWORDS = [
            "fail",
            "error",
            "timeout",
            "timed out",
            "refused",
            "denied",
            "blocked",
            "unable",
            "cannot",
            "404",
            "502",
            "503",
            "not found",
            "not exist",
        ]

        phases: dict[str, dict] = {}
        key_findings: list[str] = []
        total_steps = len(self.executed_steps)

        for i, step in enumerate(self.executed_steps):
            step_lower = step.lower()
            # Extract the Round number
            round_match = re.search(r"Round\s*(\d+)", step)
            int(round_match.group(1)) if round_match else i + 1

            # Determine success/failure
            has_failure = any(kw in step_lower for kw in FAILURE_KEYWORDS)
            has_discovery = any(kw in step_lower for kw in DISCOVERY_KEYWORDS)

            if has_discovery and not has_failure:
                status = StepStatus.SUCCESS
            elif has_failure:
                status = StepStatus.FAILURE
            else:
                status = StepStatus.INFO

            # Extract the action (first meaningful phrase)
            action = self._extract_action(step)

            # Extract the result (key information discovered)
            result = self._extract_result(step)

            # Assign to a phase (guessed from keywords)
            phase = self._guess_phase(step)

            if phase not in phases:
                phases[phase] = {
                    "count": 0,
                    "actions": set(),
                    "success_count": 0,
                    "failure_count": 0,
                    "key_results": [],
                }

            phases[phase]["count"] += 1
            if action:
                phases[phase]["actions"].add(action)
            if status == StepStatus.SUCCESS:
                phases[phase]["success_count"] += 1
                if result:
                    phases[phase]["key_results"].append(f"{action}: {result}" if action else result)
            elif status == StepStatus.FAILURE:
                phases[phase]["failure_count"] += 1

            # Collect key findings
            if status == StepStatus.SUCCESS and result:
                key_findings.append(f"{action}: {result}" if action else result)

        # Convert the sets in phases to lists (for JSON serialization)
        phase_summaries = {}
        for phase_name, data in phases.items():
            phase_summaries[phase_name] = {
                "count": data["count"],
                "actions": list(data["actions"])[:5],
                "success_count": data["success_count"],
                "failure_count": data["failure_count"],
                "key_results": data["key_results"][:5],
            }

        return {
            "total_steps": total_steps,
            "phases": phase_summaries,
            "key_findings": key_findings[:10],
        }

    def get_constraints_prompt_block(self) -> str:
        """Return a stable prompt block for current task constraints."""
        return self.task_constraints.to_prompt_block()

    def _extract_action(self, step: str) -> str:
        """Extract a short action description from the step text."""
        import re

        # Prefer explicit action verbs
        action_pattern = (
            r"\b(?:try|attempt|test|scan|probe|enumerat\w*|verif\w*|exploit\w*|"
            r"check|analyz\w*|access\w*|connect\w*|fetch\w*|brute\w*)\b[^,.;\n]*"
        )
        match = re.search(action_pattern, step, re.IGNORECASE)
        if match:
            return match.group(0).strip()[:30]

        # Fallback: take the first meaningful phrase (strip Round number and think tags)
        clean = re.sub(r"Round\s*\d+:", "", step)
        clean = re.sub(r"<think>.*?</think>", "", clean)
        clean = clean.strip()[:40]
        return clean if clean else "execute step"

    def _extract_result(self, step: str) -> str:
        """Extract a result summary from the step text."""
        import re

        # Extract discovery-type results
        discovery_pattern = (
            r"\b(?:found|discover\w*|confirm\w*|vuln\w*|port|path|connect\w*|"
            r"return\w*|accessible|success\w*|obtained|leaked)\b[^.;\n]*"
        )
        match = re.search(discovery_pattern, step, re.IGNORECASE)
        if match:
            result = match.group(0)[:50]
            # Strip think-tag content
            result = re.sub(r"<think>.*?</think>", "", result)
            return result.strip()

        # Extract failure reasons
        failure_pattern = (
            r"\b(?:fail\w*|error|timed?\s*out|timeout|refused|denied|blocked|"
            r"unable|cannot|404|502|503)\b[^.;\n]*"
        )
        match = re.search(failure_pattern, step, re.IGNORECASE)
        if match:
            return match.group(0)[:50]

        return ""

    def _guess_phase(self, step: str) -> str:
        """Guess which phase a step belongs to from its content."""
        lowered = step.lower()
        # Phase-switch markers
        if "phase switch" in lowered or "entered" in lowered:
            if "recon" in lowered:
                return "Recon"
            elif "vulnerability discovery" in lowered or "vuln discovery" in lowered:
                return "Vulnerability Discovery"
            elif "exploit" in lowered:
                return "Exploitation"
            elif "report" in lowered:
                return "Reporting"

        # Keyword-based classification
        recon_keywords = ["port", "service", "fingerprint", "architecture", "waf", "directory", "subdomain", "whois"]
        vuln_keywords = ["vuln", "injection", "xss", "sql", "csrf", "ssti", "probe"]
        exploit_keywords = ["exploit", "poc", "verif", "payload"]

        for kw in exploit_keywords:
            if kw in lowered:
                return "Exploitation"

        for kw in vuln_keywords:
            if kw in lowered:
                return "Vulnerability Discovery"

        for kw in recon_keywords:
            if kw in lowered:
                return "Recon"

        return self.phase.value  # Use the current phase

    def add_note(self, note: str) -> None:
        """Add a session note, filtering out code/symbol-heavy noise."""
        import re as _re

        # Reject notes that are primarily code/symbols — these pollute evidence extraction
        # and create fake URLs/paths in findings.
        # Count Chinese characters vs code symbols
        chinese = _re.findall(r"[\u4e00-\u9fff]", note)
        code_symbols = _re.findall(
            r"[{}()=+*/<>\-\\[\\]|;|import |def |return |print\(|requests\.|socket\.|re\.|sys\.]",
            note,
        )
        if len(note) > 20 and len(code_symbols) > len(chinese) * 0.5:
            # Too much code, skip it
            return
        # Reject very short notes that are just code symbols or numbers
        if len(note) < 5 or note in ("---", "**", ">>>", "..."):
            return
        self.notes.append(note)

    def add_confirmed_fact(self, fact: str) -> None:
        """Add a confirmed fact (verified by tool output)."""
        if fact and fact not in self.confirmed_facts:
            self.confirmed_facts.append(fact)
        if fact:
            self.reasoning.add_fact(
                key=self._fact_key_from_text(fact),
                value=fact,
                source="confirmed_fact",
                confidence=0.9,
            )

    def _fact_key_from_text(self, fact: str) -> str:
        text = fact.lower()
        if "cve-" in text:
            return "cve"
        if "http://" in text or "https://" in text:
            return "url"
        if "port" in text:
            return "port"
        if "server" in text or "x-powered-by" in text:
            return "service"
        if "waf" in text:
            return "waf"
        return "confirmed_fact"

    def add_assumption(self, assumption: str) -> None:
        """Add an unverified assumption."""
        if assumption and assumption not in self.unverified_assumptions:
            self.unverified_assumptions.append(assumption)

    def mark_recon_dimension(self, dimension: str) -> None:
        """Mark a recon dimension as completed.

        Args:
            dimension: One of 'server', 'website', 'domain', 'personnel'
        """
        if dimension in self.recon_dimensions_completed:
            self.recon_dimensions_completed[dimension] = True

    def is_recon_complete(self) -> bool:
        """Check if all active recon dimensions have been completed at least once.

        Dimension 4 (personnel) is only checked if it's been activated.
        """
        for dim, completed in self.recon_dimensions_completed.items():
            if dim == "personnel" and not self.recon_dimension4_active:
                continue  # Skip inactive dimension 4
            if not completed:
                return False
        return True

    def get_recon_status_text(self) -> str:
        """Get a human-readable recon dimension completion status."""
        parts = []
        dim_names = {
            "server": "Dim 1 (Server)",
            "website": "Dim 2 (Website)",
            "domain": "Dim 3 (Domain)",
            "personnel": "Dim 4 (Personnel)",
        }
        for dim, completed in self.recon_dimensions_completed.items():
            if dim == "personnel" and not self.recon_dimension4_active:
                continue  # Skip inactive dimension 4
            name = dim_names.get(dim, dim)
            parts.append(f"{'✅' if completed else '❌'} {name}")
        incomplete = [
            dim
            for dim, done in self.recon_dimensions_completed.items()
            if (dim != "personnel" or self.recon_dimension4_active) and not done
        ]
        status = " | ".join(parts)
        if incomplete:
            status += f"\n→ {len(incomplete)} dimension(s) still unchecked; keep collecting, do not mark [DONE]"
        return status

    def advance_phase(self, phase: PentestPhase) -> None:
        """Move to a new phase."""
        old_phase = self.phase
        self.phase = phase
        # Record the phase switch
        self.add_step(
            step=f"Phase switch → {phase.value}",
            action="phase switch",
            target=f"{old_phase.value} → {phase.value}",
            result=f"Entered {phase.value} phase",
            status=StepStatus.INFO,
        )

    def save(self, path: Optional[Path] = None) -> Path:
        """Save session state to JSON file."""
        if path is None:
            from specter.config.settings import SESSIONS_DIR

            safe_target = (self.target or "unknown").replace("/", "_").replace(":", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = SESSIONS_DIR / f"{timestamp}_{safe_target}.json"

        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.model_dump(mode="json"), f, ensure_ascii=False, indent=2)
        return path

    @classmethod
    def load(cls, path: Path) -> "SessionState":
        """Load session state from JSON file."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)


class ContextManager:
    """Manages conversation context and session state."""

    def __init__(self, max_history: int = 200) -> None:
        self.max_history = max_history
        self.messages: list[dict[str, str]] = []
        self.state = SessionState()

    def add_user_message(self, content: str) -> None:
        """Add a user message to context."""
        self.messages.append({"role": "user", "content": content})
        self._trim()

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to context."""
        self.messages.append({"role": "assistant", "content": content})
        self._trim()

    def add_system_message(self, content: str) -> None:
        """Add a system message (inserted at beginning)."""
        # System messages are handled separately in the API call
        pass

    def get_messages(self) -> list[dict[str, str]]:
        """Get conversation messages for API call."""
        return self.messages.copy()

    def reset(self) -> None:
        """Reset context and session state."""
        self.messages = []
        self.state = SessionState()

    def _trim(self) -> None:
        """Trim old messages to stay within limit.

        Instead of blindly dropping old messages, we compress them
        into a summary to preserve key discoveries for multi-round loops.
        """
        if len(self.messages) <= self.max_history:
            return

        # Keep the most recent 70% of messages intact
        keep_count = int(self.max_history * 0.7)
        recent = self.messages[-keep_count:]
        old = self.messages[:-keep_count]

        # Compress old messages into a summary instead of discarding
        summary = self._compress_messages(old)

        self.messages = []
        if summary:
            self.messages.append(
                {
                    "role": "system",
                    "content": f"[Previous session summary]\n{summary}",
                }
            )
        self.messages.extend(recent)

    @staticmethod
    def _compress_messages(messages: list[dict[str, str]]) -> str:
        """Compress a list of messages into a concise summary.

        Extracts key findings, tool results, and discoveries from the
        conversation history so the LLM doesn't completely lose context.
        """
        key_parts = []

        for msg in messages:
            content = msg.get("content", "")
            # Extract tool call/result information — these contain actual findings
            if "Tool call:" in content or "Tool result:" in content:
                key_parts.append(content[:300])

            # Extract lines that look like findings/discoveries
            for line in content.split("\n"):
                stripped = line.strip()
                lower = stripped.lower()
                if any(marker in stripped for marker in ["[+]", "[!]", "[-]", "Status:", "Headers:", "Body"]) or any(
                    marker in lower
                    for marker in [
                        "found",
                        "discover",
                        "vuln",
                        "flag",
                        "cve",
                        "port",
                        "open",
                        "service",
                        "path",
                        "leak",
                        "injection",
                        # ★ Negative/failure markers — critical for CTF to avoid repeating
                        "fail",
                        "invalid",
                        "no ",
                        "same response",
                        "blocked",
                        "unsuccessful",
                        "not found",
                        "not exist",
                        "error",
                        "404",
                        "timeout",
                        # ★ Confirmed fact markers — verified by actual tool output
                        "confirmed",
                        "verified",
                        # ★ Assumption markers — things the LLM assumed but didn't verify
                        "assume",
                        "should",
                        "maybe",
                        "possibly",
                        "likely",
                        "guess",
                    ]
                ):
                    key_parts.append(stripped[:200])

        if not key_parts:
            return ""

        # Limit total summary size to avoid context bloat
        summary = "\n".join(key_parts)
        if len(summary) > 3000:
            summary = summary[:3000] + "\n...(more history omitted)"

        return summary

    def trim_messages(self, max_messages: int = 20) -> None:
        """Forcefully trim conversation history to a specific size.

        Used when context overflow causes repeated LLM errors.
        """
        if len(self.messages) > max_messages:
            self.messages = self.messages[-max_messages:]
