---
name: web-security-advanced
description: Advanced web security testing — injection attack families, protocol security, authentication and logic vulnerabilities, file and deployment security, modern web attack surfaces, with complete playbooks
---

# Advanced Web Security Testing Skill

Use this Skill when the target is a web application, API, gateway, or browser-facing service and systematic vulnerability testing is required.

**Prerequisite**: If requests are still client-controlled and replay is unstable, use the `client-reverse` Skill first.

## CTF Scene Routing

> When the target is a CTF challenge (known to have a flag, needs to bypass specific filters), prefer the `ctf-web` Skill for specific bypass values and payloads:

| CTF Scene | Route to ctf-web | Reference Doc |
|-----------|-----------------|--------------|
| PHP weak comparison / type bypass | `ctf-web` | `references/php-bypass-cheatsheet.md` |
| Command injection space bypass | `ctf-web` | `references/command-injection-bypass.md` |
| eval echo / blind RCE | `ctf-web` | `references/eval-and-rce-techniques.md` |
| PHP code audit | `ctf-web` | `references/php-code-audit-checklist.md` |
| SSTI injection chains | `ctf-web` | `references/ssti-injection-chains.md` |
| Deserialization exploit chains | `ctf-web` | `references/deserialization-playbook.md` |
| File upload → RCE | `ctf-web` | `references/file-upload-to-rce.md` |

**This Skill focuses on pentest methodology**; for CTF-specific bypass values and payload templates, refer to `ctf-web`.

## Scene Routing

| Attack Surface Type | Preferred Reference |
|--------------------|---------------------|
| Parameter injection (SQLi/XSS/command exec/SSTI/XXE) | `references/web-injection.md` |
| Protocol security (CORS/GraphQL/WebSocket/OAuth/request smuggling) | `references/web-modern-protocols.md` |
| Auth and logic (IDOR/privilege escalation/payment/password reset/auth bypass) | `references/web-logic-auth.md` |
| File and infrastructure (upload/traversal/inclusion/deployment/cache/CDN/cloud) | `references/web-file-infra.md` |
| Deployment security | `references/web-deployment-security.md` |

## Testing Workflow

### 1. Input Validation Testing
- SQL injection: boolean/time-based/error-based/union/stacked
- XSS: reflected/stored/DOM/CSP bypass
- Command injection: separator bypass, encoding bypass
- SSTI: template engine identification + RCE chains
- XXE: entity injection, OOB data exfiltration
- Deserialization: Java/PHP/Python chains

### 2. Authentication and Session Testing
- Default credentials, brute force
- Session management flaws (fixation/hijacking/insecure cookies)
- JWT security (algorithm tampering/key brute force/none algorithm)
- OAuth/OIDC misconfiguration
- MFA bypass

### 3. Logic Vulnerability Testing
- Privilege escalation (horizontal/vertical)
- Business logic bypass (payment/coupon/voting)
- Race conditions
- IDOR (insecure direct object references)

### 4. Protocol Security Testing
- CORS misconfiguration
- GraphQL introspection/injection
- WebSocket authentication and injection
- HTTP request smuggling
- SSRF (internal network probing/cloud metadata)

### 5. File and Deployment Security
- File upload bypass
- Path traversal
- LFI/RFI
- CDN/cache poisoning
- Supply chain attacks
- Cloud security misconfiguration

## Reference Documents

- `references/03-web-security-integrated.md` — Web security integrated reference
- `references/web-injection.md` — Injection attack detailed reference
- `references/web-modern-protocols.md` — Modern protocol security
- `references/web-logic-auth.md` — Authentication and logic vulnerabilities
- `references/web-file-infra.md` — File and infrastructure security
- `references/web-deployment-security.md` — Deployment security
- `references/web-ai-attack-map.md` — Web and AI attack mapping
- `references/web-playbook-*.md` — Domain-specific playbooks (23 total)
