# 08 Rapid Checklists And Payloads

This file is the rapid operator-reference layer of the final skill system.
Use it only after routing is clear. It is meant for fast lookup, not for replacing methodology or workflow selection.

## Use This File For

- Quickly recalling what to look at first for a specific vulnerability type or blockage point
- Quickly filtering payload families, bypass directions, and validation order
- Quickly confirming common test cards for AI, MCP, containers, WebSocket, JWT, files, authentication, SSRF, etc.
- Quickly moving from “I know what to test” to “which category of validation to start with first”

## Do Not Use This File For

- Replacing `00-usage-and-routing.md` for scenario routing
- Replacing `01-unified-methodology.md` for methodology decisions
- Jumping directly into blind payload testing before a request is captured and replay is stable

## Fast Routing Cards

### Web injection or output execution

- Start with `03-web-security-integrated.md`
- If validating input points, prioritize splitting into `SQLi`, `XSS`, `command execution`, `SSTI`, `XXE`
- If the request is client-constructed, go back to `02-client-api-reverse-and-burp.md` first

### Auth, logic, token, or state bugs

- Start with `03-web-security-integrated.md`
- Focus first on confirming object identifiers, role boundaries, reset flows, payment amounts, and ordering dependencies
- If a token or signature comes from the client, stabilize replay before testing

### Browser-side sign, anti-bot, or WebSocket handshake

- Start with `browser-js-signing-workflow.md`
- Then proceed stage-by-stage into `browser-locate-and-request-chain.md`, `browser-recover-and-shell-reduction.md`, `browser-runtime-fit-and-risk.md`, `browser-validation-and-handoff.md`
- Switch back to `03-web-security-integrated.md` once replay is stable

### Android runtime, packet visibility, or sign recovery

- Start with `android-external-url-runtime-first-workflow.md`
- If advancing via UI state is needed, continue with `android-ui-driven-observation-and-packet-loop.md`
- Only enter `android-signing-and-crypto-workflow.md` when packets cannot be captured, are opaque, or replay is blocked

### AI, agent, or MCP exposure

- Start with `04-ai-and-mcp-security-integrated.md`
- Focus first on distinguishing `prompt injection`, `tool abuse`, `MCP trust boundary`, `memory/state poisoning`, `output approval gaps`
- When a quick lookup of common test semantics is needed, see the AI/MCP cards below

### Intranet, host, or AD work

- Start with `06-intranet-and-host-operations-integrated.md`
- When unsure about tools, also consult `05-tools-and-operations-integrated.md`

## Web Rapid Cards

### SQL injection

- Quick validation: `'`, `"`, `)`, boolean difference, time difference, error difference
- First confirm injection location: query, body, JSON, header, cookie, WebSocket message
- Check whether input is affected by client-side signing or encryption; if so, restore the request lifecycle first
- Common bypass directions: inline comments, whitespace variation, keyword case folding, alternate encodings, parameter pollution

### XSS

- Quick classification: reflected, stored, DOM
- First confirm context: HTML body, attribute, JS string, URL, template
- Common starter families: event handlers, SVG, tag breaking, JS context breaking
- If output goes through a client-side rendering framework, also check DOM sinks and CSP behavior

### Command execution

- Quick validation: timing, DNS or HTTP OOB, harmless command echo
- First identify whether the execution point is a system shell, template helper, language runtime, or worker sidecar
- Common bypass directions: separators, whitespace bypass, variable concatenation, Base64 or hex decode chains

### File and SSRF

- For file issues, first classify: upload, traversal/download, inclusion, parser confusion
- For SSRF, first classify: raw fetch, image proxy, webhook, PDF render, URL preview, cloud metadata reachability
- Common bypass directions: encoding layers, mixed path separators, alternate IP formats, redirect chaining, protocol pivot

### Modern protocols

- WebSocket: first confirm handshake auth, Origin validation, message-level auth, room boundaries
- JWT: first confirm algorithm handling, signature validation, dynamic key paths like `kid` or `jku`
- OAuth/OIDC: first confirm redirect URI, state, PKCE, account binding
- Request smuggling: first confirm proxy chain and frontend/backend parsing differences

## AI And MCP Rapid Cards

### Prompt injection

- Quick classification: direct, indirect, retrieval-borne, tool-description-borne, memory-borne
- First confirm which boundary the injection enters: model prompt, retrieval context, tool metadata, tool output, persisted memory
- Common bypass directions: role play, instruction override, encoding, multilingual phrasing, hidden text, long-context dilution

### Tool abuse and MCP trust boundary

- First confirm whether tool descriptions are read with high model trust
- First confirm whether tool parameters, resource paths, and tool outputs will be re-interpreted
- Quick checks: unauthorized resource reads, prompt override in description, hidden instructions, cross-tool request rewriting

### Agent memory and state poisoning

- First confirm whether memory is explicit storage or implicit history summarization
- First check whether malicious goals, role preferences, or external instructions can be written to persistent state
- Watch for cross-turn behavior drift, approval bypass, and silent exfiltration

### Model or data leakage

- Quick checks: system prompt extraction, tool inventory exposure, API or secret leakage, training-data style continuation, RAG source disclosure
- First distinguish between direct disclosure and inference-style leakage

## Container And Sandbox Rapid Cards

### Environment triage

- First confirm whether inside a container, sandbox, restricted shell, or agent execution sandbox
- First check capabilities, namespace, mount, socket, and metadata reachability
- If only validating isolation boundaries, do not attempt destructive actions first

### Escape paths

- Common directions: exposed Docker socket, writable host mounts, privileged container, cgroup abuse, `/proc` traversal, kernel CVE, cloud metadata pivots
- Do minimal information gathering first, then decide whether to continue

### Persistence or staged foothold

- First confirm authorization boundaries and test objectives
- Prioritize validating “whether persistence is possible” rather than expanding directly
- Common locations: shell rc files, scheduled tasks, service startup, workspace poisoning, SSH keys

## Payload Family Hints

Use families, not copied full lists, unless the current task specifically needs detail from a deeper source.

- SQLi: boolean, time, error, union, second-order
- XSS: reflected, stored, DOM, mutation-based, CSP-aware
- Command execution: separator-based, subshell, whitespace-bypass, encoded launcher, OOB validation
- File bugs: upload extension variants, MIME mismatch, parser confusion, traversal encodings
- SSRF: alternate IP encodings, redirect pivot, protocol pivot, metadata paths
- AI injection: direct override, indirect document-borne, description poisoning, memory poisoning, encoded or multilingual prompts
- Escape and shell: environment triage, breakout path validation, persistence validation, callback channel selection

## Escalation Rule

- If the route is still unclear, go back to `00-usage-and-routing.md`.
- If packet visibility or replay is blocked, go back to `02-client-api-reverse-and-burp.md` or the matching browser or Android workflow.
- If you need exact original payload wording or exhaustive raw examples, open `references/payloads.md`.


