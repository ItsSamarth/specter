"""Specter Report Content Filter — clean raw LLM output into pure report text.

Filtering targets:
    - TOOL_CALL markers and content
    - Python code blocks (print/open/import, etc.)
    - Round/Context markers
    - Debug output
    - think-tag content

Outputs only clean Markdown report text.
"""

from __future__ import annotations

import re
from typing import Optional


class ReportContentFilter:
    """Report content filter — extract clean report text from raw LLM output."""

    # ── Filter patterns ───────────────────────────────────────────────────

    # TOOL_CALL markers (multiple formats)
    TOOL_CALL_PATTERNS = [
        # standard format
        re.compile(r"\[TOOL_CALL\]\s*\{[^}]+\}", re.DOTALL),
        # tool => format
        re.compile(r'\[TOOL_CALL\]\s*\{tool\s*=>\s*"[^"]+"\s*,\s*args\s*=>\s*\{[^}]+\}', re.DOTALL),
        # python_execute format
        re.compile(r'\{tool\s*=>\s*"python_execute"\s*,\s*args\s*=>\s*\{[^}]+\}', re.DOTALL),
        # nmap_scan format
        re.compile(r'\{tool\s*=>\s*"nmap_scan"\s*,\s*args\s*=>\s*\{[^}]+\}', re.DOTALL),
        # fetch format
        re.compile(r"\[TOOL_CALL\]\s*```\s*\{[^}]+\}\s*```", re.DOTALL),
        # simplified tool call
        re.compile(r"\[TOOL_CALL\]\s*[\s\S]+?\[/TOOL_CALL\]"),
        # tool_call format
        re.compile(r"tool_call\s*\(\s*\{[^}]+\}\s*\)", re.DOTALL),
    ]

    # Round markers
    ROUND_PATTERNS = [
        re.compile(r"──\s*Cycle\s*\d+\s*\|\s*Round\s*\d+\s*──", re.DOTALL),
        re.compile(r"──\s*Round\s*\d+\s*──", re.DOTALL),
        re.compile(r"Cycle\s*\d+\s*\|\s*Round\s*\d+", re.IGNORECASE),
        re.compile(r"Round\s+\d+:", re.IGNORECASE),
        re.compile(r"Round\s*\d+", re.IGNORECASE),
    ]

    # think tags (LLM reasoning process)
    THINK_PATTERNS = [
        re.compile(
            r"</?(?:think|thinking|result_info)>?[\s\S]*?</?(?:think|thinking|result_info)>?",
            re.IGNORECASE,
        ),
        re.compile(r"</?(?:think|thinking|result_info)>?[\s\S]*", re.IGNORECASE),
        re.compile(r"<thinking>[\s\S]*?</thinking>?", re.IGNORECASE),
        re.compile(r"<thinking>[\s\S]*", re.IGNORECASE),
        re.compile(r"<reasoning>[\s\S]*?</reasoning>?", re.IGNORECASE),
        re.compile(r"<reasoning>?[\s\S]*", re.IGNORECASE),
        re.compile(r"\[think\]", re.IGNORECASE),
        re.compile(r"##\s*Thinking\s*", re.IGNORECASE),
        re.compile(r"###\s*Reasoning\s*", re.IGNORECASE),
    ]

    # Python code blocks (multiple formats)
    PYTHON_CODE_PATTERNS = [
        # standard ```python ``` format
        re.compile(r"```python\s*[\s\S]*?```"),
        # ``` ``` format (no language tag)
        re.compile(r"```\s*[\s\S]*?```"),
        # single-line print/import statements
        re.compile(r"^\s*print\s*\(", re.MULTILINE),
        re.compile(r"^\s*import\s+", re.MULTILINE),
        re.compile(r"^\s*from\s+\w+\s+import", re.MULTILINE),
        re.compile(r"^\s*with\s+open\s*\(", re.MULTILINE),
        # with statement
        re.compile(r"with\s+open\s*\([^)]+\)\s+as\s+\w+:", re.DOTALL),
        # if __name__ == "__main__"
        re.compile(r'if\s+__name__\s*==\s*["\']__main__["\']:', re.DOTALL),
    ]

    # Debug output markers
    DEBUG_PATTERNS = [
        re.compile(r"^\s*──.*──\s*$", re.MULTILINE),  # separator line
        re.compile(r"^\s*\[=\]+\s*$", re.MULTILINE),  # ===== style
        re.compile(r"tool call|tool_call", re.IGNORECASE),
        re.compile(r"Tool call|Tool result", re.IGNORECASE),
        re.compile(r"\[LLM\s+[A-Z_]+\]", re.IGNORECASE),  # [LLM THINKING], etc.
    ]

    # HTTP request/response (optional filtering)
    HTTP_PATTERNS = [
        re.compile(r"HTTP/\d\.\d\s+\d+\s+[^\n]+", re.IGNORECASE),
        re.compile(r"^(GET|POST|PUT|DELETE|HEAD|OPTIONS)\s+/[^\n]+", re.MULTILINE | re.IGNORECASE),
    ]

    # Phase-switch markers
    PHASE_PATTERNS = [
        re.compile(r"Phase switch\s*[→\-]>\s*\w+", re.IGNORECASE),
        re.compile(r"Entered\s*\w+\s*phase", re.IGNORECASE),
        re.compile(r"Current phase:\s*\w+", re.IGNORECASE),
    ]

    @classmethod
    def filter(cls, content: str) -> str:
        """Filter content, keeping only clean report text.

        Args:
            content: raw LLM output

        Returns:
            the filtered, clean report text
        """
        result = content

        # 1. Remove TOOL_CALL blocks
        result = cls._remove_tool_calls(result)

        # 2. Remove Round markers
        result = cls._remove_round_markers(result)

        # 3. Remove think tags
        result = cls._remove_think_tags(result)

        # 4. Remove Python code blocks
        result = cls._remove_python_code(result)

        # 5. Remove debug output
        result = cls._remove_debug_output(result)

        # 6. Remove phase-switch markers
        result = cls._remove_phase_markers(result)

        # 7. Clean up extra blank lines
        result = cls._cleanup_whitespace(result)

        return result.strip()

    @classmethod
    def _remove_tool_calls(cls, content: str) -> str:
        """Remove TOOL_CALL-related content."""
        result = content

        for pattern in cls.TOOL_CALL_PATTERNS:
            result = pattern.sub("", result)

        # Remove standalone tool_call lines
        result = re.sub(r"^\s*tool_call\s*\(.*$", "", result, flags=re.MULTILINE)
        result = re.sub(r"^\s*\[TOOL_CALL\]\s*$", "", result, flags=re.MULTILINE)

        return result

    @classmethod
    def _remove_round_markers(cls, content: str) -> str:
        """Remove Round/Cycle markers."""
        result = content

        for pattern in cls.ROUND_PATTERNS:
            result = pattern.sub("", result)

        return result

    @classmethod
    def _remove_think_tags(cls, content: str) -> str:
        """Remove think tags and the reasoning process."""
        result = content

        for pattern in cls.THINK_PATTERNS:
            result = pattern.sub("", result)

        return result

    @classmethod
    def _remove_python_code(cls, content: str) -> str:
        """Remove Python code blocks.

        Note: this filters raw code from LLM output, not code examples in the report.
        Report code examples (PoC, etc.) should be added via templates, not here.
        """
        result = content

        for pattern in cls.PYTHON_CODE_PATTERNS:
            result = pattern.sub("", result)

        # Remove standalone large import/print statements
        lines = result.split("\n")
        filtered_lines = []
        in_code_block = False

        for line in lines:
            # Detect code-block boundaries
            if line.strip().startswith("```"):
                in_code_block = not in_code_block
                continue

            # Skip if inside a code block
            if in_code_block:
                continue

            # Filter suspicious code lines
            stripped = line.strip()
            if any(
                stripped.startswith(prefix)
                for prefix in [
                    "import ",
                    "from ",
                    "print(",
                    "with open",
                    "if __name__",
                    "def ",
                    "class ",
                    "return ",
                    "try:",
                    "except:",
                    "requests.",
                    "socket.",
                    "subprocess.",
                ]
            ):
                continue

            filtered_lines.append(line)

        result = "\n".join(filtered_lines)
        return result

    @classmethod
    def _remove_debug_output(cls, content: str) -> str:
        """Remove debug output."""
        result = content

        for pattern in cls.DEBUG_PATTERNS:
            result = pattern.sub("", result)

        # Remove tool-result markers
        result = re.sub(r"\[Result\]\s*:?\s*", "", result)
        result = re.sub(r"\[Output\]\s*:?\s*", "", result)

        return result

    @classmethod
    def _remove_phase_markers(cls, content: str) -> str:
        """Remove phase-switch markers."""
        result = content

        for pattern in cls.PHASE_PATTERNS:
            result = pattern.sub("", result)

        return result

    @classmethod
    def _cleanup_whitespace(cls, content: str) -> str:
        """Clean up extra blank lines and spaces."""
        # Collapse 3+ consecutive blank lines
        result = re.sub(r"\n{3,}", "\n\n", content)

        # Strip leading/trailing spaces per line
        lines = result.split("\n")
        result = "\n".join(line.strip() for line in lines if line.strip())

        return result

    @classmethod
    def is_pure_markdown(cls, content: str) -> bool:
        """Check whether content is pure Markdown (no interfering markers).

        Used to validate that the filtered result is acceptable.
        """
        # Check for interfering markers
        interference_patterns = [
            r"\[TOOL_CALL\]",
            r"\{tool\s*=>",
            r"──\s*Round",
            r"──\s*Cycle",
            r"<thinking>",
            r"```python",
            r"^\s*print\s*\(",
            r"^\s*import\s+",
        ]

        for pattern in interference_patterns:
            if re.search(pattern, content, re.MULTILINE):
                return False

        return True


# ── Convenience functions ───────────────────────────────────────────────────


def filter_report_content(content: str) -> str:
    """Filter report content, keeping only clean Markdown text.

    A convenience wrapper around ReportContentFilter.filter().
    """
    return ReportContentFilter.filter(content)


def deduplicate_report_findings(findings: list, threshold: float = 0.75) -> list:
    """Semantically deduplicate a list of VulnerabilityFinding before rendering.

    Report-layer semantic dedup: beyond the exact dedup in SessionState, apply one
    more semantic merge so the report does not contain multiple wordings of the same
    vulnerability. Keeps the better-evidenced one.

    Args:
        findings: list of VulnerabilityFinding.
        threshold: similarity threshold, default 0.75.

    Returns:
        the deduplicated list, preserving first-seen order.
    """
    from specter.agent.finding_similarity import deduplicate_findings

    return deduplicate_findings(findings, threshold=threshold)


def extract_findings_section(content: str) -> Optional[str]:
    """Extract the vulnerability-list section from a report.

    Returns None if no dedicated vulnerability list is found.
    """
    patterns = [
        r"(##\s*Vulnerability List\s*\n[\s\S]*?)(?=##|\Z)",
        r"(##\s*Detailed Findings\s*\n[\s\S]*?)(?=##|\Z)",
        r"(##\s*Findings\s*\n[\s\S]*?)(?=##|\Z)",
    ]

    for pattern in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def remove_unverified_findings(content: str) -> str:
    """Remove unverified vulnerabilities from report content.

    Vulnerabilities tagged [Unverified] are removed.
    """
    # Remove [Unverified]-tagged vulnerability sections
    pattern = re.compile(
        r"(###\s*\[[^\]]*\]\s*[^\n]*Unverified[^\n]*\n[\s\S]*?)(?=###|\Z)",
        re.IGNORECASE,
    )
    result = pattern.sub("", content)

    # Remove lines containing [Unverified]
    lines = result.split("\n")
    filtered_lines = []
    skip_section = False

    for line in lines:
        # Detect the start of an unverified section
        if "[Unverified]" in line and line.strip().startswith("###"):
            skip_section = True
            continue

        # Detect section end
        if skip_section and line.startswith("##"):
            skip_section = False

        if not skip_section:
            filtered_lines.append(line)

    return "\n".join(filtered_lines)
