"""Specter Finding Similarity — lightweight semantic deduplication.

A pure-Python semantic dedup for vulnerability findings, with no external NLP
dependencies.

Core capabilities:
    - normalize_text:        text normalization (lowercase, collapse whitespace, URL-path normalization)
    - normalize_vuln_type:   vuln-type normalization (alias mapping, e.g. "sqli" -> "sql_injection")
    - text_similarity:       word-set Jaccard similarity
    - url_similarity:        parse a URL and compare host / path / query parameters
    - finding_similarity:    combined vuln_type / location / description similarity
    - deduplicate_findings:  dedup by a similarity threshold, keeping the better-evidenced one

Complementary to the existing finding_id hash dedup: hash dedup handles exact
matches; this module handles the fuzzy, semantic "same vuln, different wording".
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Optional
from urllib.parse import parse_qs, urlsplit

if TYPE_CHECKING:
    from specter.agent.context import VulnerabilityFinding


# ── Vuln-type normalization map ─────────────────────────────────────────

# alias -> canonical type. Keys are lowercase, whitespace-collapsed.
_VULN_TYPE_ALIASES: dict[str, str] = {
    # SQL injection
    "sqli": "sql_injection",
    "sql injection": "sql_injection",
    "sql注入": "sql_injection",
    "blind sqli": "sql_injection",
    "blind injection": "sql_injection",
    "injection vulnerability": "sql_injection",
    "injection": "sql_injection",
    "sql_injection": "sql_injection",
    # XSS
    "xss": "cross_site_scripting",
    "cross-site scripting": "cross_site_scripting",
    "reflected xss": "cross_site_scripting",
    "stored xss": "cross_site_scripting",
    "cross site scripting": "cross_site_scripting",
    "cross_site_scripting": "cross_site_scripting",
    "跨站脚本": "cross_site_scripting",
    # SSRF
    "ssrf": "server_side_request_forgery",
    "server-side request forgery": "server_side_request_forgery",
    "server side request forgery": "server_side_request_forgery",
    "server_side_request_forgery": "server_side_request_forgery",
    "服务端请求伪造": "server_side_request_forgery",
    # RCE
    "rce": "remote_code_execution",
    "command execution": "remote_code_execution",
    "remote code execution": "remote_code_execution",
    "command injection": "remote_code_execution",
    "remote_code_execution": "remote_code_execution",
    "命令执行": "remote_code_execution",
    # LFI / file inclusion
    "lfi": "local_file_inclusion",
    "file inclusion": "local_file_inclusion",
    "rfi": "local_file_inclusion",
    "path traversal": "local_file_inclusion",
    "file inclusion/traversal": "local_file_inclusion",
    "local file inclusion": "local_file_inclusion",
    "local_file_inclusion": "local_file_inclusion",
    "文件包含": "local_file_inclusion",
    # IDOR / broken access
    "idor": "insecure_direct_object_reference",
    "broken access control": "insecure_direct_object_reference",
    "horizontal privilege escalation": "insecure_direct_object_reference",
    "vertical privilege escalation": "insecure_direct_object_reference",
    "insecure direct object reference": "insecure_direct_object_reference",
    "insecure_direct_object_reference": "insecure_direct_object_reference",
    "越权": "insecure_direct_object_reference",
    # CSRF
    "csrf": "cross_site_request_forgery",
    "cross-site request forgery": "cross_site_request_forgery",
    "cross site request forgery": "cross_site_request_forgery",
    # Auth bypass
    "auth bypass": "auth_bypass",
    "authentication bypass": "auth_bypass",
    "unauthorized": "auth_bypass",
    "unauthorized access": "auth_bypass",
    "unauthenticated": "auth_bypass",
    "no auth required": "auth_bypass",
    "403 auth block": "auth_bypass",
    "potential authorization bypass": "auth_bypass",
    # Information disclosure
    "info disclosure": "info_disclosure",
    "information disclosure": "info_disclosure",
    "data leak": "info_disclosure",
    "sensitive information disclosure": "info_disclosure",
    "sensitive dir/file disclosure": "info_disclosure",
}


def normalize_vuln_type(vuln_type: str) -> str:
    """Normalize a vuln type, mapping common aliases to canonical names.

    Args:
        vuln_type: Raw vuln-type string (any case / spacing).

    Returns:
        The normalized type; if no alias matches, the lowercased,
        whitespace-collapsed original value.
    """
    if not vuln_type:
        return ""
    key = re.sub(r"\s+", " ", vuln_type.strip().lower())
    if key in _VULN_TYPE_ALIASES:
        return _VULN_TYPE_ALIASES[key]
    # Try swapping underscores/spaces before matching
    underscore = key.replace(" ", "_")
    if underscore in _VULN_TYPE_ALIASES:
        return _VULN_TYPE_ALIASES[underscore]
    spaced = key.replace("_", " ")
    if spaced in _VULN_TYPE_ALIASES:
        return _VULN_TYPE_ALIASES[spaced]
    return underscore


# ── Text normalization and similarity ───────────────────────────────────

_URL_RE = re.compile(r'https?://[^\s<>"\')\]]+', re.IGNORECASE)
_TOKEN_RE = re.compile(r"[a-z0-9]+", re.IGNORECASE)
# Punctuation boundary tags (e.g. [auto], [confirmed]) should be stripped before
# tokenizing so they do not pollute the word set.
_NOISE_TAGS = ("[auto]", "[confirmed]", "[unverified]", "[自动]", "[已确认]", "[未验证]")


def _normalize_url_path(url: str) -> str:
    """Normalize a URL: drop scheme, drop trailing slash, keep host+path."""
    try:
        parts = urlsplit(url)
    except ValueError:
        return url.lower()
    host = (parts.hostname or "").lower()
    path = parts.path or ""
    if len(path) > 1:
        path = path.rstrip("/")
    return f"{host}{path}"


def normalize_text(text: str) -> str:
    """Normalize text: lowercase, collapse whitespace, normalize embedded URL paths.

    Args:
        text: Any free text (description/evidence/title).

    Returns:
        The normalized text.
    """
    if not text:
        return ""
    result = text
    for tag in _NOISE_TAGS:
        result = result.replace(tag, " ")
    # Replace embedded URLs with their normalized host+path form
    result = _URL_RE.sub(lambda m: _normalize_url_path(m.group(0)), result)
    result = result.lower()
    result = re.sub(r"\s+", " ", result).strip()
    return result


def _tokenize(text: str) -> set[str]:
    """Split normalized text into a word set."""
    return set(_TOKEN_RE.findall(text))


def text_similarity(a: str, b: str) -> float:
    """Word-set Jaccard similarity.

    Args:
        a: Text A.
        b: Text B.

    Returns:
        Similarity in [0.0, 1.0]. Returns 1.0 when both are empty; 0.0 when only one is empty.
    """
    na, nb = normalize_text(a), normalize_text(b)
    if not na and not nb:
        return 1.0
    if not na or not nb:
        return 0.0
    ta, tb = _tokenize(na), _tokenize(nb)
    if not ta and not tb:
        return 1.0
    if not ta or not tb:
        return 0.0
    inter = len(ta & tb)
    union = len(ta | tb)
    return inter / union if union else 0.0


def url_similarity(a: str, b: str) -> float:
    """Compare host / path / query-parameter similarity of two URLs.

    Weights: host 0.3 + path 0.4 + query-parameter-name set 0.3.
    Non-URL strings fall back to Jaccard text similarity on the raw text.

    Args:
        a: URL or location string A.
        b: URL or location string B.

    Returns:
        Similarity in [0.0, 1.0].
    """
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0

    pa, pb = urlsplit(a.strip()), urlsplit(b.strip())
    # If neither looks like a URL (no scheme, no netloc, no path separator), compare as text
    if not (pa.scheme or pa.netloc) and not (pb.scheme or pb.netloc):
        return text_similarity(a, b)

    # host comparison
    ha, hb = (pa.hostname or "").lower(), (pb.hostname or "").lower()
    if not ha and not hb:
        host_sim = 1.0
    elif not ha or not hb:
        host_sim = 0.0
    else:
        host_sim = 1.0 if ha == hb else 0.0

    # path comparison: Jaccard over "/"-split segments
    seg_a = {s for s in pa.path.split("/") if s}
    seg_b = {s for s in pb.path.split("/") if s}
    if not seg_a and not seg_b:
        path_sim = 1.0
    elif not seg_a or not seg_b:
        path_sim = 0.0
    else:
        path_sim = len(seg_a & seg_b) / len(seg_a | seg_b)

    # query-parameter-name set comparison (ignore concrete values, so different pages/IDs count as the same endpoint)
    qa = set(parse_qs(pa.query).keys())
    qb = set(parse_qs(pb.query).keys())
    if not qa and not qb:
        query_sim = 1.0
    elif not qa or not qb:
        query_sim = 0.0
    else:
        query_sim = len(qa & qb) / len(qa | qb)

    return host_sim * 0.3 + path_sim * 0.4 + query_sim * 0.3


# ── Combined finding similarity ─────────────────────────────────────────

_LOCATION_RE = re.compile(r'(?:https?://[^\s<>"\')\]]+)|(?:/[\w%&=?\-./]+)')


def _extract_location(finding: "VulnerabilityFinding") -> str:
    """Extract the first URL or path from a finding's evidence / description as its location."""
    for field in (finding.evidence or "", finding.description or ""):
        if not field:
            continue
        m = _LOCATION_RE.search(field)
        if m:
            return m.group(0)
    return ""


def _vuln_type_similarity(a: str, b: str) -> float:
    """Vuln-type similarity: exact match 1.0, normalized match 0.8, otherwise 0.0."""
    ra, rb = (a or "").strip().lower(), (b or "").strip().lower()
    if ra and rb and ra == rb:
        return 1.0
    na, nb = normalize_vuln_type(a), normalize_vuln_type(b)
    if na and nb and na == nb:
        return 0.8
    return 0.0


def finding_similarity(a: "VulnerabilityFinding", b: "VulnerabilityFinding") -> float:
    """Combined similarity of two vulnerability findings.

    Dimension weights:
        - vuln_type:    0.3 (exact match 1.0 / normalized match 0.8)
        - location/URL: 0.4 (extracted from evidence/description, then url_similarity)
        - description:  0.3 (text Jaccard of title + description)

    Args:
        a: Finding A.
        b: Finding B.

    Returns:
        Combined similarity in [0.0, 1.0].
    """
    type_sim = _vuln_type_similarity(a.vuln_type, b.vuln_type)

    loc_a, loc_b = _extract_location(a), _extract_location(b)
    if not loc_a and not loc_b:
        # Neither has an explicit location — this dimension is not comparable, treat as neutral (no bonus or penalty)
        loc_sim = 0.5
    else:
        loc_sim = url_similarity(loc_a, loc_b)

    desc_a = f"{a.title} {a.description}".strip()
    desc_b = f"{b.title} {b.description}".strip()
    desc_sim = text_similarity(desc_a, desc_b)

    return type_sim * 0.3 + loc_sim * 0.4 + desc_sim * 0.3


# ── Evidence-strength comparison and dedup ──────────────────────────────

_EVIDENCE_LEVEL_RANK = {"L1": 1, "L2": 2, "L3": 3, "L4": 4}
_LIFECYCLE_RANK = {
    "rejected": 0,
    "candidate": 1,
    "pending_verification": 2,
    "needs_manual_review": 3,
    "verified": 4,
}


def _evidence_strength(finding: "VulnerabilityFinding") -> tuple:
    """Compute a finding's evidence strength, used to decide which to keep on a duplicate.

    Sort key (larger = stronger):
        1. Verified first (verified=True)
        2. Lifecycle rank
        3. Evidence level L1-L4
        4. Evidence text length (more detailed evidence)
    """
    return (
        1 if finding.verified else 0,
        _LIFECYCLE_RANK.get(finding.lifecycle_status, 1),
        _EVIDENCE_LEVEL_RANK.get(finding.evidence_level, 1),
        len(finding.evidence or ""),
    )


def deduplicate_findings(
    findings: list["VulnerabilityFinding"], threshold: float = 0.75
) -> list["VulnerabilityFinding"]:
    """Semantically deduplicate a list of findings, keeping the better-evidenced one.

    Iterate over findings, comparing each new finding against the already-kept ones;
    a similarity above the threshold is treated as a duplicate, keeping the one with
    stronger evidence.

    Args:
        findings: The raw list of findings.
        threshold: Similarity threshold, default 0.75.

    Returns:
        The deduplicated list, preserving first-seen relative order.
    """
    kept: list["VulnerabilityFinding"] = []
    for cand in findings:
        dup_index: Optional[int] = None
        for idx, existing in enumerate(kept):
            if finding_similarity(cand, existing) >= threshold:
                dup_index = idx
                break
        if dup_index is None:
            kept.append(cand)
            continue
        # Duplicate hit: keep the one with stronger evidence
        if _evidence_strength(cand) > _evidence_strength(kept[dup_index]):
            kept[dup_index] = cand
    return kept
