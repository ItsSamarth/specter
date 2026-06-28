"""Bridge layer: plugin results → SessionState.findings.

Convert the PluginFinding emitted by a plugin into the VulnerabilityFinding used by the Agent,
and merge into SessionState deduplicated by finding_id, so plugin results enter the report-generation pipeline.
"""

from __future__ import annotations

import json
from typing import Any

from specter.agent.context import SessionState, VulnerabilityFinding
from specter.plugins.result import PluginFinding, PluginResult, RiskLevel

# Plugin risk level → vulnerability severity (aligned with VulnerabilityFinding.severity values)
RISK_TO_SEVERITY: dict[RiskLevel, str] = {
    RiskLevel.INFO: "Info",
    RiskLevel.LOW: "Low",
    RiskLevel.MEDIUM: "Medium",
    RiskLevel.HIGH: "High",
    RiskLevel.CRITICAL: "Critical",
}


def _evidence_level_for(confidence: float) -> str:
    """Roughly map evidence level by confidence (plugins do not actively verify over the network, capped at L2)."""
    if confidence >= 0.8:
        return "L2"
    return "L1"


def plugin_finding_to_vuln_finding(
    finding: PluginFinding,
    *,
    plugin_id: str = "",
) -> VulnerabilityFinding:
    """Convert a single PluginFinding into a VulnerabilityFinding."""
    evidence_obj = finding.evidence or {}
    try:
        evidence_text = (
            json.dumps(evidence_obj, ensure_ascii=False)
            if isinstance(evidence_obj, (dict, list))
            else str(evidence_obj)
        )
    except (TypeError, ValueError):
        evidence_text = str(evidence_obj)

    source = plugin_id or finding.metadata.get("plugin_id", "")
    description = finding.description
    if source:
        prefix = f"[plugin:{source}] "
        description = f"{prefix}{description}" if description else prefix.strip()

    return VulnerabilityFinding(
        title=finding.title,
        severity=RISK_TO_SEVERITY.get(finding.risk, "Info"),
        vuln_type=finding.vuln_type,
        description=description,
        evidence=evidence_text[:500],
        remediation=finding.remediation,
        evidence_level=_evidence_level_for(finding.confidence),
        lifecycle_status="pending_verification",
    )


def merge_plugin_results_into_session(
    session: SessionState,
    results: PluginResult | list[PluginResult],
) -> int:
    """Merge findings from a batch of plugin results into the session; return the count added (after dedup)."""
    if isinstance(results, PluginResult):
        results = [results]

    added = 0
    for result in results:
        for finding in result.findings:
            vuln = plugin_finding_to_vuln_finding(finding, plugin_id=result.plugin_id)
            if session.add_finding(vuln):
                added += 1
    return added


def summarize_plugin_results(results: list[PluginResult]) -> dict[str, Any]:
    """Summarize a batch of plugin results for CLI / report display."""
    findings = sum(len(result.findings) for result in results)
    errors = [result for result in results if result.error and not result.skipped]
    skipped = [result for result in results if result.skipped]
    return {
        "plugins": len(results),
        "findings": findings,
        "errors": len(errors),
        "skipped": len(skipped),
    }
