---
name: rapid-checklist
description: Pentest quick reference and Payloads — fast Payload families, bypass reminders, verification order, common test cards, suitable for quick lookup once the test direction is known
---

# Pentest Quick Reference and Payload Skill

**Use only after the route is already clear**. This Skill is for quick lookup; it does not replace methodology or workflow selection.

## Use Cases

- Quickly recall what to look at first for a given vulnerability class or blocker
- Quickly filter Payload families, bypass directions, and verification order
- Quickly confirm common test cards for AI, MCP, containers, WebSocket, JWT, files, authentication, SSRF, etc.
- Move from "I know what to test" to "which class of verification do I start with"

## When Not Applicable

- Replacing scenario triage → use `pentest-flow`
- Replacing methodology decisions → use the corresponding specialized Skill
- Blind testing when the request was not captured or replay is not stable → use `client-reverse` first

## CTF Quick Reference

> For CTF challenges, prefer the `ctf-web` / `ctf-crypto` / `ctf-misc` Skills; the following are quick cards:

| Scenario | Quick Location |
|------|---------|
| PHP loose comparison → MD5 values starting with 0e | `ctf-web` → `php-bypass-cheatsheet.md` |
| Command injection space bypass → ${IFS}/$IFS$9/< | `ctf-web` → `command-injection-bypass.md` |
| eval with no echo → write file / DNS exfiltration | `ctf-web` → `eval-and-rce-techniques.md` |
| RSA small exponent → cube root / Coppersmith | `ctf-crypto` → `rsa-attacks-cheatsheet.md` |
| Python Jail → `__import__`/func_globals | `ctf-misc` → `python-jail-escape.md` |
| Encoding chain → base64→hex→ROT13 multi-layer | `ctf-misc` → `encoding-chain-reference.md` |

## Quick Routing Cards

### Web Injection / Output Execution
- SQLi → `'`, `"`, `)`, boolean difference, time difference, error difference
- XSS → `<script>`, `<img onerror>`, `javascript:`, DOM sink
- Command injection → `;id`, `|id`, `` `id` ``, `$(id)`
- SSTI → `{{7*7}}`, `${7*7}`, `<%= 7*7 %>`, template engine fingerprint
- XXE → `<!ENTITY>`, parameter entity, OOB exfiltration

### Authentication / Logic / Token
- JWT → none algorithm, algorithm tampering, key brute force, jku/x5u injection
- CSRF → missing Token, predictable Token, Referer validation flaw
- IDOR → modify ID parameter, batch enumeration
- Payment logic → amount tampering, negative numbers, race condition

### Browser Signing / Anti-scraping
- Use `client-reverse` first for stable replay
- Phases: locate → recover → runtime → validation

### Android Runtime / Signature Recovery
- Use the `client-reverse` runtime-first path first
- Only reverse engineer when packets cannot be captured / are encrypted / cannot be replayed

### AI / MCP
- Prompt injection → direct/indirect/CoT interference
- Tool abuse → MCP poisoning / instruction override
- Identity escape → role boundary violation / privilege drift

### Intranet / AD
- Use `intranet-pentest-advanced` first
- When unsure about tools, supplement with `pentest-tools`

## Reference Documents

- `references/08-rapid-checklists-and-payloads.md` — Quick reference and Payload integrated reference
- `references/payloads.md` — Detailed Payload collection
- `references/testing-methodology.md` — Testing methodology
