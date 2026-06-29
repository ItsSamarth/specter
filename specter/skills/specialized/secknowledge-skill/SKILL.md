---
name: secknowledge-skill
description: |
  Web+AI security testing knowledge base. Combines WooYun 88,636 cases + Xianzhī L1-L4 methodology + GAARM 150 risks
  + OWASP Top 10 (LLM/ASI/WSTG).
  TRIGGER when the task is hands-on security testing: penetration testing, vulnerability research/exploitation, red-team exercises, security audits (SAST/DAST),
  CTF challenges, AI/LLM security testing (Prompt injection/jailbreaking/MCP/Agent/sandbox escape). The user has provided an explicit test target
  (URL/code/model/Agent architecture) and the intent is "test/audit/find vulns/exploit".
  DO NOT trigger:
  - Security concept discussions ("what is XSS", "how does SQL injection work") → ordinary Q&A
  - Non-security code review / debug / performance optimization → code-audit-skill or other
  - Fixing syntax errors / business logic bugs → ordinary programming assistance
  - Pure white-box code audit (full project directory / Source-Sink taint analysis) → code-audit-skill
  - CVE number lookups for documentation only → WebSearch
  Boundary note: CTF short code snippets + exploitation ideas → this Skill; full project directory + system white-box audit → code-audit-skill
---

# Web and AI Security Testing Knowledge Base

> Knowledge sources: WooYun 88,636 vulnerabilities × Xianzhī 5,600+ documents × GAARM 150 AI risks × OWASP
> Architecture: SKILL.md (routing) → references/ (loaded per scenario)

## Specter Integration Notes

- This Skill is integrated from `Pa55w0rd/secknowledge-skill` and used in Specter as the `secknowledge-skill` specialized skill; upstream declared MIT License.
- For CTF/SRC scenarios, first load `references/specter-ctf-src-routing.md` to determine the entry point, then load `web-*`, `ai-*`, `testing-methodology.md`, or `gaarm-risk-matrix.md` by vulnerability type.
- Works alongside existing Specter skills: CTF single-challenge techniques should be combined with `ctf-web`/`ctf-crypto`/`ctf-misc`; SRC and real-world vulnerability hunting should use this Skill's methodology, case mapping, risk matrix, and evidence constraints.
- Output preserves upstream authorization boundaries, citation annotations, and the "assumed/confirmed" distinction; payloads, CVEs, GAARM/OWASP numbers that cannot be corroborated from a reference must be explicitly labeled as unchecked.

## Trigger Conditions

**Trigger conditions (AND combination)**:
1. User intent is to **execute** security testing (pentest/vuln-hunting/exploitation/audit) — not discussion/learning
2. A **concrete target** is provided: URL, interface, code snippet, model/Agent architecture, MCP config — not abstract questions
3. Task **involves one of the following domains**:
   - Web: SQL injection / XSS / command execution / privilege escalation / file upload / SSRF / deserialization / XXE / GraphQL / HTTP smuggling
   - AI: Prompt injection / jailbreaking / MCP poisoning / Agent abuse / RAG poisoning / sandbox escape / model extraction
   - Bypass: WAF / content filter / Guard Rails bypass

**Do NOT trigger** (any one hit routes elsewhere):
- Conceptual explanations: "what is…", "how does … work", "how to defend against …" → ordinary Q&A
- Non-security code review: "review code quality", "optimize performance" → ordinary code review
- Business bugs: syntax errors, null pointers, business logic errors (non-security logic) → ordinary debug
- **Deep white-box code audit** (Source-Sink taint propagation, AST analysis) → code-audit-skill
- CVE documentation lookups, tool documentation → WebSearch/Context7

**Ambiguity handling**: When target and intent are unclear, ask first: "What is the target? Do you want a penetration test / code audit / or to understand the concept?"

## Behavioral Rules (valid for the entire session, not relaxed by conversation length)

1. ❗ **All Payloads/CVE numbers/risk numbers must cite specific sections from reference files** — self-check before each output. Anything not in the reference must be labeled "UNABLE TO CITE" — fabrication is prohibited.
2. ❗ **Distinguish "vulnerability hypothesis" from "vulnerability confirmed"** — potential risks inferred from methodology → label `Hypothetical (needs verification)`; backed by clear evidence → label `Confirmed (evidence: …)`. Conflation is prohibited.
3. ❗ **Authorization boundary** — before outputting any exploitation steps, confirm this is a CTF / authorized pentest / personal environment. Without authorization context, output analysis only — do not output fully weaponized payloads.

## Hallucination Protection and Citation

| Content type | Correct output | Prohibited output |
|---------|---------|---------|
| CVE number | Cite specific reference file and section, or label "UNABLE TO CITE — recommend WebSearch for verification" | Fabricate CVE-YYYY-NNNN |
| Payload | Cite from `references/web-*.md` or `references/ai-*.md` payload sections | Write payloads from memory |
| GAARM risk number | Cite from `references/gaarm-risk-matrix.md` | Invent numbers |
| OWASP entries | LLM01-10 / ASI01-10 / WSTG-* cite `testing-methodology.md §10.x` | Rewrite entry meanings |
| Tools/commands | Only those appearing in references, or explicitly labeled "general command (not verified in reference)" | Fabricate tool parameters |
| No search results | "UNABLE TO ASSESS: reference does not cover this scenario, recommend WebSearch" | Use experience-based guesses as conclusions |

**Citation levels**:
- `[Cited]` — from a specific section of a reference file (must include file:section)
- `⚠️ General knowledge` — not verified in this Skill's references, advisory only
- `💡 Suggestion` — methodological reasoning, not a factual claim

## Output Constraints

Prohibited output:
- Opening phrases: "Let me analyze…" / "First we need to…" / "Based on your needs…"
- Tool call descriptions: "I will use the Read tool to read XX"
- Restatement of known information (URL, target type the user just provided)
- Payloads or CVE numbers without source citations
- Complete weaponized chains in unauthorized scenarios

Output limits:
- Single reply ≤ 3 levels of recommendations (avoid information overload)
- Payload examples ≤ 5 per vulnerability type (full list in references)
- Use tables/quick-reference format, avoid long narrative paragraphs

## Tool Priority (used by this Skill internally)

| Operation | Primary | Downgrade condition | Downgrade tool |
|------|------|---------|---------|
| Read reference | Read | Read fails | Bash cat |
| Search keywords/CVE | Grep (within reference) | 2 consecutive misses | WebSearch |
| Code audit target | Delegate to code-audit-skill | — | — |

Single timeout ≠ unavailable; must retry once before downgrading.

## Usage Workflow

**Dependency chain constraint (spanning all three steps, mandatory)**:
- Step 2 input == Step 1's "located reference list" — no new files may be added
- Step 3 citation set ⊆ Step 2's "loaded list" — re-searching references in Step 3 is prohibited
- Citation counts in Step 3 Checkpoint must be traceable to sources in Step 2 Checkpoint

**Step 1: Target classification + reference location**
- Determine: Web / AI / Web+AI hybrid / container sandbox
- Locate: Find the corresponding reference files using the "scenario navigation index", record as list `L1`

Failure fallback:
- Insufficient target info to classify → trigger ambiguity clarification question, do not guess; defaulting to "Web+AI hybrid" is not allowed
- Scenario navigation index does not cover the scenario → label "UNABLE TO CITE: scenario {X} not in index", list `L1` is empty, Step 3 can only output methodology-level suggestions

✅ Checkpoint: `Step 1 complete: target type={X}, |L1| == scenario navigation index matches = {N}`

**Step 2: Load Step 1 references on demand (lazy loading)**
- Input: list `L1` from Step 1; record loaded set as `L2`, must satisfy `L2 ⊆ L1`
- Load 1 file at a time, single load ≤ 1000 tokens; references exceeding the budget (e.g. `ai-identity-app.md` 906 lines, `ai-data-app.md` 903 lines) must use Read offset/limit or Grep to locate before reading
- Loading files not in `L1` in this step is prohibited

Failure fallback:
- Read fails → retry once → still fails, use Bash cat → both fail → label "UNABLE TO ASSESS: file unreadable", remove from `L2`, proceeding to Step 3 without this is not allowed
- Grep has no hits → label "UNABLE TO CITE: {keyword} not found in {file}"
- Reference file does not exist → label broken link + add to pending reference list, do not fabricate content

✅ Checkpoint: `Step 2 complete: |L2| == |L1| - unreadable file count = {M}, total {X} tokens`

**Step 3: Output test ideas by methodology (L1→L4)**
- Input: loaded set `L2` from Step 2; all citations in this step must ⊆ `L2`
- L1 attack surface identification → L2 hypothesis building → L3 deep exploitation → L4 defense reverse-engineering
- Each conclusion must cite a specific section/line from a file in `L2`; no basis → label "UNABLE TO CITE" and stop that hypothesis thread
- Re-searching is prohibited: if a new reference is needed in this step → return to Step 1 for relocation, do not Read/Grep directly

✅ Checkpoint: `Step 3 complete: N hypotheses output, of which Cited M + UNABLE TO CITE K == N (equality check)`

**End-to-end cross-validation**:
- [ ] All files cited in Step 3 ∈ Step 2's `L2` (grep-verified)
- [ ] Cited count + UNABLE TO CITE count == total hypothesis count

## Scenario Navigation Index

> Each row points to the corresponding reference. Detailed payloads/cases/methodology are all in the references; this SKILL.md does not expand them.

### Core Methodology

| Scenario | reference |
|------|----------|
| L1-L4 thinking pyramid + WooYun vulnerability formula + GAARM mapping | `references/testing-methodology.md` |
| OWASP Top 10 mapping (LLM/ASI/WSTG) | `testing-methodology.md §10.1-10.3` |
| GAARM 150 risk numbers | `references/gaarm-risk-matrix.md` |

### Web Security (by vulnerability type)

| Scenario | reference |
|------|----------|
| SQL Injection (incl. SQLMap quick reference) | `references/web-sqli.md` |
| XSS Cross-Site Scripting | `references/web-xss.md` |
| Command Execution (RCE) | `references/web-rce.md` |
| XXE (XML External Entity) | `references/web-xxe.md` |
| Deserialization vulnerabilities | `references/web-deser.md` |
| File Upload (incl. webshell evasion) | `references/web-upload.md` |
| Path Traversal / File Inclusion | `references/web-traversal.md` |
| Information Disclosure (.git / backup / error messages) | `references/web-leak.md` |
| SSRF / server misconfiguration / CMS+URL appendix | `references/web-ssrf-misc.md` |
| Privilege escalation / payment / password reset / session / API auth | `references/web-logic-auth.md` |
| CORS / GraphQL / HTTP smuggling / WebSocket / OAuth | `references/web-modern-protocols.md` |
| Supply chain / cloud config / container / CI/CD / framework CVE | `references/web-deployment-security.md` |

### AI/LLM Security (by GAARM phase)

| Security domain | Application phase | Deployment phase | Training phase |
|--------|---------|---------|---------|
| **AI Application** (application phase broken down by risk category below) | See breakdown table below | `ai-app-deploy.md` | `ai-app-train.md` |
| **AI Model** (application phase broken down by risk category below) | See breakdown table below | `ai-model-deploy.md` | `ai-model-train.md` |
| **AI Data** (Prompt leakage/theft/inference) | `ai-data-app.md` | `ai-data-deploy.md` | `ai-data-train.md` |
| **AI Identity** (role escape/Agent impersonation) | `ai-identity-app.md` | `ai-identity-deploy.md` | `ai-identity-train.md` |
| **AI Baseline** (container/sandbox/supply chain) | `ai-baseline-app.md` | `ai-baseline-deploy.md` | `ai-baseline-train.md` |

**AI Application - Application phase by risk category**:

| Risk category | GAARM number | reference |
|---------|----------|----------|
| Prompt injection and variants (direct/indirect/XSS/Memory/worm/obfuscation/encoding/reverse induction/multimodal) | GAARM.0039, 0040.x, 0043.x, 0044, 0045, 0061 | `ai-app-prompt.md` |
| MCP protocol attacks (rug pull/tool poisoning/instruction override/hidden instructions) | GAARM.0046.x | `ai-app-mcp.md` |
| Agent and CoT attacks (Agent exploitation/SSRF/RCE/CoT/query injection/environment injection) | GAARM.0041.x, 0042.x, 0047, 0056.001, 0060 | `ai-app-agent-cot.md` |

**AI Model - Application phase by risk category**:

| Risk category | GAARM number | reference |
|---------|----------|----------|
| Jailbreaking (DAN/Many-shot/adversarial suffix/concept activation) | GAARM.0027.x | `ai-model-jailbreak.md` |
| Hallucination (factual/cross-modal) | GAARM.0028.x, 0064 | `ai-model-hallucination.md` |
| Non-compliant content (bias/violence/political/false/inducement) | GAARM.0029.x | `ai-model-content.md` |
| Copyright and commercial violations | GAARM.0030.x | `ai-model-copyright.md` |
| Functional abuse and information forgery (image/audio/video/phishing) | GAARM.0031.x, 0033, 0062, 0063 | `ai-model-misuse.md` |
| Adversarial samples and model extraction | GAARM.0032.x | `ai-model-extraction.md` |

**Special references**:
- AI Agent / MCP / Skills 2025-2026 frontier risks → `references/ai-app-frontier.md`
- Container and sandbox escape practical methodology → `references/ai-baseline-escape.md`

### Payload Quick Reference (search by scenario in the main references)

| Scenario | reference |
|------|----------|
| SQL Injection Payload | `references/web-sqli.md` |
| XSS Payload | `references/web-xss.md` |
| RCE / Command Execution Payload | `references/web-rce.md` |
| Deserialization / XXE Payload | `references/web-deser.md` / `references/web-xxe.md` |
| File upload bypass / path traversal Payload | `references/web-upload.md` / `references/web-traversal.md` |
| SSRF Payload | `references/web-ssrf-misc.md` |
| Web modern protocol Payload (GraphQL/HTTP smuggling/WebSocket) | `references/web-modern-protocols.md` |
| Prompt injection Payload | `references/ai-app-prompt.md` |
| MCP poisoning Payload | `references/ai-app-mcp.md` |
| Agent / CoT injection Payload | `references/ai-app-agent-cot.md` |
| Jailbreak / adversarial suffix Payload | `references/ai-model-jailbreak.md` |
| Container escape / persistence / lateral movement | `references/ai-baseline-escape.md` |

## Zero-Result Handling

| Situation | Correct action |
|------|---------|
| Grep misses in reference | "UNABLE TO CITE: scenario {X} not covered in reference. Recommend WebSearch or add reference" |
| User-provided URL is unreachable | "UNABLE TO ASSESS: target unreachable" — do not guess vulnerabilities from URL structure |
| Execution needed but no authorization context | "Output analysis only, no weaponized chain. If authorized testing, please specify the authorization scope" |
| Reference partially matches user scenario | Cite the matched portion + explicitly label unmatched portions as "UNABLE TO CITE" |

## Routing to Other Skills

| User request | Correct route |
|---------|---------|
| Penetration test / red team / CTF / vulnerability hunting | **This Skill** |
| Java/JS deep white-box code audit (Source-Sink) | code-audit-skill |
| Mirawork platform-specific testing | mirawork-security-tester |
| WooYun historical vulnerability analysis methodology | wooyun-legacy |
| Xianzhī community research methodology | xianzhi-research |

---

*v2.0 | Knowledge sources: WooYun 88,636 × Xianzhī 5,600+ × GAARM 150 × OWASP LLM/ASI/WSTG*
