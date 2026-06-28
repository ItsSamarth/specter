"""Specter Vulnerability Verifier — validate findings before they enter the report.

Core principle: an unverified vulnerability = false positive = not written to the report

Workflow:
    1. Receive a vulnerability hypothesis (pending finding)
    2. Generate PoC code
    3. Execute the PoC via python_execute
    4. Decide the result: verified / rejected
    5. Only verified vulnerabilities enter the report
"""

from __future__ import annotations

import subprocess
import tempfile
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from specter.agent.context import VulnerabilityFinding


class VerificationStatus(str, Enum):
    """Vulnerability verification status."""

    PENDING = "pending"  # pending verification
    VERIFIED = "verified"  # verification passed
    REJECTED = "rejected"  # verification failed / false positive
    SKIPPED = "skipped"  # verification skipped (e.g. already-confirmed facts)


class VerificationResult(str, Enum):
    """Verification result detail."""

    # Verified outcomes
    VULN_CONFIRMED = "vuln_confirmed"  # vulnerability confirmed
    SENSITIVE_DATA_EXPOSED = "sensitive_data"  # sensitive data exposed
    SECURITY_BYPASS = "security_bypass"  # security restriction bypassed

    # Rejected outcomes
    FALSE_POSITIVE = "false_positive"  # false positive
    NO_RESPONSE_DIFF = "no_response_diff"  # no response difference
    PARAM_INVALID = "param_invalid"  # invalid parameter
    NORMAL_RESPONSE = "normal_response"  # normal response
    TIMEOUT = "timeout"  # timeout
    ERROR_403_404 = "error_403_404"  # 403/404 normal rejection


@dataclass
class VerifiedFinding:
    """A verified vulnerability finding."""

    # Information from the original finding
    original_finding: VulnerabilityFinding

    # Verification status
    status: VerificationStatus = VerificationStatus.PENDING
    result: Optional[VerificationResult] = None

    # PoC information
    poc_code: Optional[str] = None
    poc_output: Optional[str] = None
    poc_executed_at: Optional[str] = None

    # Verification conclusion
    verified_description: str = ""
    verified_evidence: str = ""
    verified_severity: str = ""  # may be adjusted based on the verification result

    # Rejection reason (if verification failed)
    rejection_reason: str = ""

    # Verifier (metadata)
    verified_by: str = "verifier_module"
    verified_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ── PoC generator ─────────────────────────────────────────────────────────────


class PoCGenerator:
    """Generate PoC code from a vulnerability hypothesis."""

    # Vulnerability type → PoC template mapping
    POC_TEMPLATES: dict[str, str] = {
        "sql_injection": """
import requests

target = "{target}"
params = {{
    "id": "{payload}",
}}

try:
    r = requests.get(target, params=params, timeout=10, verify=False)
    text = r.text.lower()

    # SQL error signatures
    sql_errors = [
        "sql syntax", "mysql", "sqlite", "postgres", "oracle",
        "sqlstate", "microsoft sql", "odbc", "syntax error",
        "you have an error in your sql", "warning: mysql",
    ]

    for err in sql_errors:
        if err in text:
            print(f"[CONFIRMED] SQL injection: SQL error signature detected '{err}'")
            print(f"[INFO] Response status code: {{r.status_code}}")
            exit(0)

    # Check response difference (if a normal baseline is provided)
    baseline_len = {baseline_len}
    if len(r.content) != baseline_len and baseline_len > 0:
        print(f"[POSSIBLE] Abnormal response length: {{len(r.content)}} vs baseline {{baseline_len}}")

    print("[REJECTED] No SQL injection signature detected")
except requests.Timeout:
    print("[REJECTED] Request timed out")
except Exception as e:
    print(f"[ERROR] {{e}}")
""",
        "xss": """
import requests
import sys

target = "{target}"
payload = "{payload}"

try:
    r = requests.get(target, params={{"q": payload}}, timeout=10, verify=False)

    if payload in r.text:
        print(f"[CONFIRMED] XSS: payload appears in the response")
        print(f"[INFO] Response contains: {{payload}}")
        exit(0)

    print("[REJECTED] XSS payload did not appear in the response")
except Exception as e:
    print(f"[ERROR] {{e}}")
""",
        "command_injection": """
import requests

target = "{target}"
params = {{
    "cmd": "{payload}",
}}

try:
    r = requests.get(target, params=params, timeout=10, verify=False)
    text = r.text

    # Command-injection signatures
    cmd_indicators = ["uid=", "gid=", "root:", "/bin/bash", "whoami", "linux"]

    for indicator in cmd_indicators:
        if indicator in text:
            print(f"[CONFIRMED] Command injection: detected '{{indicator}}'")
            exit(0)

    print("[REJECTED] No command-injection signature detected")
except Exception as e:
    print(f"[ERROR] {{e}}")
""",
        "debug_mode": """
import requests

target = "{target}"

try:
    # Normal request
    r_normal = requests.get(target, timeout=10, verify=False)
    len_normal = len(r_normal.content)

    # Debug-mode request
    r_debug = requests.get(target + "/?debug=1", timeout=10, verify=False)
    len_debug = len(r_debug.content)

    print(f"[INFO] Normal response length: {{len_normal}}")
    print(f"[INFO] debug=1 response length: {{len_debug}}")

    # Check for debug-info leakage
    if len_debug != len_normal:
        diff = len_debug - len_normal
        print(f"[POSSIBLE] Debug-mode response differs from normal, difference: {{diff}} bytes")

        # Check whether it really leaks sensitive information
        debug_content = r_debug.text.replace(r_normal.text, "")
        if debug_content:
            sensitive_keywords = ["password", "secret", "api_key", "token", "db_", "connection"]
            for kw in sensitive_keywords:
                if kw.lower() in debug_content.lower():
                    print(f"[CONFIRMED] Debug mode leaks sensitive info: detected '{kw}'")
                    exit(0)

        # If only the length differs but no sensitive info, downgrade to Info
        print("[INFO] Debug-mode response differs but no sensitive-info leak found, downgraded to Info")

    # Check debug-related keywords
    if "debug" in r_debug.text.lower() and r_debug.text.lower().count("debug") > r_normal.text.lower().count("debug"):
        print("[POSSIBLE] Debug mode contains extra debug info")

    print("[REJECTED] No obvious sensitive-info leak found in debug mode")

except Exception as e:
    print(f"[ERROR] {{e}}")
""",
        "lfi": """
import requests

target = "{target}"
payload = "{payload}"

try:
    r = requests.get(target, params={{"file": payload}}, timeout=10, verify=False)
    text = r.text.lower()

    # LFI signatures
    lfi_indicators = ["root:", "/bin/bash", "/bin/sh", "[boot loader]", "windows"]

    for indicator in lfi_indicators:
        if indicator in text:
            print(f"[CONFIRMED] LFI: detected '{{indicator}}'")
            exit(0)

    print("[REJECTED] No LFI signature detected")
except Exception as e:
    print(f"[ERROR] {{e}}")
""",
        "sensitive_file": """
import requests

target = "{target}"
path = "{path}"

try:
    r = requests.get(target + path, timeout=10, verify=False)

    if r.status_code == 200 and len(r.content) > 10:
        print(f"[CONFIRMED] Sensitive file accessible: {{path}}")
        print(f"[INFO] Status: {{r.status_code}}, length: {{len(r.content)}}")

        # Check content type
        ct = r.headers.get("content-type", "")
        print(f"[INFO] Content-Type: {{ct}}")

        exit(0)

    print(f"[REJECTED] File not accessible or empty: {{r.status_code}}")
except Exception as e:
    print(f"[ERROR] {{e}}")
""",
        "info_disclosure": """
import requests

target = "{target}"

try:
    r = requests.get(target, timeout=10, verify=False)
    headers = {{k.lower(): v.lower() for k, v in r.headers.items()}}

    # Check sensitive headers
    sensitive_headers = {
        "x-powered-by": "tech-stack info",
        "server": "server info",
        "x-aspnet-version": "ASP.NET version",
        "x-generator": "generator info",
    }

    found = []
    for header, desc in sensitive_headers.items():
        if header in headers:
            found.append(f"{{header}}: {{headers[header][:50]}}")

    if found:
        print(f"[CONFIRMED] Information disclosure: {{len(found)}} sensitive header(s)")
        for f in found:
            print(f"  - {{f}}")
        exit(0)

    print("[INFO] No obvious information disclosure; this is a normal security-config issue")
    print("[REJECTED] Response-header disclosure - this is a config issue, not a vulnerability")
except Exception as e:
    print(f"[ERROR] {{e}}")
""",
    }

    @classmethod
    def generate_poc(
        cls,
        finding: VulnerabilityFinding,
        target: str,
        baseline_len: int = 0,
    ) -> str:
        """Generate PoC code based on the vulnerability type.

        Args:
            finding: the vulnerability finding
            target: target URL
            baseline_len: normal response length (for comparison)

        Returns:
            PoC Python code string
        """
        vuln_type = (finding.vuln_type or "").lower().replace(" ", "_")
        template = cls.POC_TEMPLATES.get(vuln_type)

        if not template:
            # Generic PoC template
            template = cls._generic_template()

        payload = cls._guess_payload(finding)
        replacements = {
            "{target}": target,
            "{payload}": payload,
            "{baseline_len}": str(baseline_len),
            "{path}": payload,
        }
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, value)
        return template

    @classmethod
    def _generic_template(cls) -> str:
        """Generate a generic PoC template."""
        return """
import requests

target = "{target}"

try:
    print(f"[*] Testing target: {{target}}")

    # Custom verification logic
    r = requests.get(target, timeout=10, verify=False)
    print(f"[*] Response status: {{r.status_code}}")
    print(f"[*] Response length: {{len(r.content)}}")

    # TODO: add verification logic per specific vulnerability type
    print("[INFO] Using the generic template; add verification logic for the specific vulnerability")

except Exception as e:
    print(f"[ERROR] {{e}}")
"""

    @classmethod
    def _guess_payload(cls, finding: VulnerabilityFinding) -> str:
        """Guess a payload based on the vulnerability type."""
        vuln_type = (finding.vuln_type or "").lower()

        payloads = {
            "sql": "1' OR '1'='1",
            "xss": "<script>alert(1)</script>",
            "command": ";id",
            "lfi": "../../../etc/passwd",
        }

        for key, payload in payloads.items():
            if key in vuln_type:
                return payload

        return "test"


# ── Verification executor ─────────────────────────────────────────────────────


class VerifierExecutor:
    """Execute PoC verification and decide the result."""

    # Python interpreter path
    PYTHON_CMD = "python"

    @classmethod
    def execute_poc(cls, poc_code: str, timeout: int = 30) -> tuple[int, str]:
        """Execute PoC code.

        Args:
            poc_code: PoC Python code
            timeout: timeout in seconds

        Returns:
            (return code, output content)
        """
        # Write to a temp file
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False,
            encoding="utf-8",
        ) as f:
            f.write(poc_code)
            temp_path = f.name

        try:
            # Execute the PoC
            result = subprocess.run(
                [cls.PYTHON_CMD, temp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
            )

            output = result.stdout + result.stderr
            return result.returncode, output

        except subprocess.TimeoutExpired:
            return -1, "[TIMEOUT] PoC execution timed out"
        except FileNotFoundError:
            return -2, f"[ERROR] Python interpreter not found: {cls.PYTHON_CMD}"
        except Exception as e:
            return -3, f"[ERROR] Execution failed: {e}"
        finally:
            # Clean up the temp file
            try:
                Path(temp_path).unlink()
            except Exception:
                pass

    @classmethod
    def parse_result(cls, output: str, returncode: int) -> VerificationResult:
        """Parse PoC output and decide the verification result.

        Args:
            output: PoC output content
            returncode: return code

        Returns:
            the verification result
        """
        output_lower = output.lower()

        # Execution failed
        if returncode == -1:
            return VerificationResult.TIMEOUT
        if returncode == -2:
            return VerificationResult.ERROR_403_404
        if returncode != 0:
            return VerificationResult.FALSE_POSITIVE

        # Check confirmation markers
        if "[CONFIRMED]" in output or "[VERIFIED]" in output:
            if "sensitive" in output_lower:
                return VerificationResult.SENSITIVE_DATA_EXPOSED
            if "bypass" in output_lower:
                return VerificationResult.SECURITY_BYPASS
            return VerificationResult.VULN_CONFIRMED

        # Check rejection markers
        if "[REJECTED]" in output or "[FALSE]" in output:
            return VerificationResult.FALSE_POSITIVE

        # Check response difference
        if "[POSSIBLE]" in output:
            return VerificationResult.NO_RESPONSE_DIFF

        # Check normal response
        if returncode == 0 and "[CONFIRMED]" not in output:
            return VerificationResult.NORMAL_RESPONSE

        return VerificationResult.FALSE_POSITIVE


# ── Main verifier ─────────────────────────────────────────────────────────────


class VulnerabilityVerifier:
    """Vulnerability verifier — the core verification flow."""

    def __init__(self, target: str, baseline_len: int = 0) -> None:
        """Initialize the verifier.

        Args:
            target: target URL
            baseline_len: normal response length
        """
        self.target = target
        self.baseline_len = baseline_len
        self.verified_findings: list[VerifiedFinding] = []
        self.rejected_findings: list[VerifiedFinding] = []

    def verify(self, finding: VulnerabilityFinding) -> VerifiedFinding:
        """Verify a single vulnerability finding.

        Args:
            finding: the vulnerability finding

        Returns:
            the verified finding (with status and evidence)
        """
        vf = VerifiedFinding(original_finding=finding)

        # Generate the PoC
        poc_code = PoCGenerator.generate_poc(
            finding=finding,
            target=self.target,
            baseline_len=self.baseline_len,
        )
        vf.poc_code = poc_code

        # Execute the PoC
        returncode, output = VerifierExecutor.execute_poc(poc_code)
        vf.poc_output = output
        vf.poc_executed_at = datetime.now().isoformat()

        # Parse the result
        result = VerifierExecutor.parse_result(output, returncode)
        vf.result = result

        # Decide status based on the result
        if result in (
            VerificationResult.VULN_CONFIRMED,
            VerificationResult.SENSITIVE_DATA_EXPOSED,
            VerificationResult.SECURITY_BYPASS,
        ):
            vf.status = VerificationStatus.VERIFIED
            vf._build_verified_finding(output)
        else:
            vf.status = VerificationStatus.REJECTED
            vf._build_rejected_finding(result, output)

        # Store by category
        if vf.status == VerificationStatus.VERIFIED:
            self.verified_findings.append(vf)
        else:
            self.rejected_findings.append(vf)

        return vf

    def verify_batch(self, findings: list[VulnerabilityFinding]) -> list[VerifiedFinding]:
        """Verify findings in batch.

        Args:
            findings: list of vulnerability findings

        Returns:
            list of verified findings (verified only)
        """
        verified = []

        for finding in findings:
            vf = self.verify(finding)
            if vf.status == VerificationStatus.VERIFIED:
                verified.append(vf)

        return verified

    def _build_verified_finding(self, output: str) -> None:
        """Build the detail of a verified finding."""
        vf = self.verified_findings[-1] if self.verified_findings else None
        if not vf:
            return

        original = vf.original_finding

        # Extract confirmation info from the output
        confirmed_lines = [
            line.strip()
            for line in output.split("\n")
            if "[CONFIRMED]" in line or "[VERIFIED]" in line
        ]

        vf.verified_description = (
            f"PoC verification passed. Original description: {original.description}"
            if original.description
            else "PoC verification confirmed the vulnerability exists"
        )
        vf.verified_evidence = "\n".join(confirmed_lines) if confirmed_lines else output[:500]
        vf.verified_severity = original.severity  # keep original severity, adjustable by result

    def _build_rejected_finding(
        self,
        result: VerificationResult,
        output: str,
    ) -> None:
        """Build the detail of a rejected finding."""
        vf = self.rejected_findings[-1] if self.rejected_findings else None
        if not vf:
            return

        original = vf.original_finding

        # Rejection-reason mapping
        rejection_reasons = {
            VerificationResult.FALSE_POSITIVE: "No vulnerability signature detected after PoC execution; judged a false positive",
            VerificationResult.NO_RESPONSE_DIFF: "No response difference; invalid parameter or vulnerability not triggered",
            VerificationResult.PARAM_INVALID: "Invalid parameter; cannot verify the vulnerability hypothesis",
            VerificationResult.NORMAL_RESPONSE: "Normal response returned; the vulnerability does not exist",
            VerificationResult.TIMEOUT: "PoC execution timed out",
            VerificationResult.ERROR_403_404: "Request rejected (403/404); target not exploitable",
        }

        vf.rejection_reason = rejection_reasons.get(
            result,
            f"Verification failed, reason: {result.value}",
        )

        # Record the rejection reason, but do not add it to the report
        print(f"[VERIFIER] Excluded finding: {original.title} | reason: {vf.rejection_reason}")

    def get_verified_report_findings(self) -> list[VulnerabilityFinding]:
        """Get the list of findings that can be written to the report.

        Returns only verified findings; rejected ones are excluded.
        """
        result = []

        for vf in self.verified_findings:
            if vf.status == VerificationStatus.VERIFIED:
                # Clone the finding and update verification info
                finding = vf.original_finding.model_copy()
                finding.evidence = vf.verified_evidence
                finding.description = vf.verified_description
                finding.severity = vf.verified_severity
                result.append(finding)

        return result

    def get_summary(self) -> dict[str, Any]:
        """Get a verification summary."""
        return {
            "total": len(self.verified_findings) + len(self.rejected_findings),
            "verified": len(self.verified_findings),
            "rejected": len(self.rejected_findings),
            "target": self.target,
            "verified_findings": [
                {
                    "title": vf.original_finding.title,
                    "severity": vf.verified_severity,
                    "result": vf.result.value if vf.result else None,
                }
                for vf in self.verified_findings
            ],
            "rejected_findings": [
                {
                    "title": vf.original_finding.title,
                    "reason": vf.rejection_reason,
                }
                for vf in self.rejected_findings
            ],
        }
