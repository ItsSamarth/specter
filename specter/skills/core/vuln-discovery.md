---
name: vuln-discovery
description: Vulnerability discovery workflow — scan for vulnerabilities based on reconnaissance results
---

# Vulnerability Discovery Skill

Systematically discover security vulnerabilities present in the target based on reconnaissance results.

## Execution Steps

### 1. Known CVE Matching
- Search for corresponding CVEs based on identified service versions
- Prioritize Critical/High severity
- Record CVE ID, affected versions, and exploitation conditions

### 2. Web Vulnerability Scanning
- SQL injection detection
- XSS detection (reflected / stored / DOM-based)
- SSRF detection
- LFI/RFI detection
- Command injection detection
- File upload vulnerability detection

### 3. Configuration Flaw Detection
- Default credential testing
- Information disclosure detection
- Unauthorized access detection
- CORS configuration detection
- HTTPS configuration detection

### 4. Output
- Vulnerability list (type, severity, URL, parameter, verification method)
