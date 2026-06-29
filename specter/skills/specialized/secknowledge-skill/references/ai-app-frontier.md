# AI Application Security - Frontier Security Risks (2025-2026)

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-app-security.md
> Topic: AI Agent/MCP/Skills frontier risks (Claude Code CVE / Skills injection / Agent worms)

## Thirty-Five. AI Agent/MCP/Skills Frontier Security Risks (2025-2026)

> The following content is based on the latest security research from 2025-2026, covering OWASP Agentic AI Top 10 (ASI01-ASI10).

### MCP (Model Context Protocol) Security

#### 11 Classes of Emerging MCP Risks (Checkmarx/Invariant Labs/Trail of Bits 2025 Research)

| Risk Type | Description | Attack Scenario |
|----------|------|----------|
| Tool description poisoning | Embed hidden malicious instructions in tool descriptions | Model reads and follows hidden Prompt in description when calling the tool |
| Rug pull | Server dynamically modifies tool descriptions after client authorization | Passes initial security review; subsequent stealthy modification of function logic |
| Instruction override (Shadow Tool) | Malicious server's tool description hijacks trusted tool behavior | Modifies email-sending tool's recipient to attacker |
| ANSI/Unicode hidden instructions | Use terminal escape codes or invisible Unicode characters to hide instructions | Supply chain attack: model recommends downloading malicious package |
| Cross-server attack | Tool definition conflicts and hijacking between multiple MCP servers | Server A redefines Server B's tool names |
| Token/credential theft | Extract OAuth tokens and API keys stored by MCP server | Single-point breach gains credentials for all connected services |
| Server impersonation | Malicious MCP server impersonates legitimate service to log all queries | Data theft and behavioral monitoring |
| Schema manipulation | Dynamically modify tool input/output schema to bypass validation | Inject extra parameters or modify return values |
| Command injection | Inject OS commands through tool parameters | MCP server executes unfiltered shell commands |
| Context overflow | Construct oversized tool responses to exhaust model context window | Push out security instructions, reducing model judgment |
| Persistent poisoning | Contaminate conversation history through tool return values | Long-term impact on security of all subsequent interactions |

#### MCP Security Testing Methods

1. **Tool description audit**: Check whether all registered tool description fields contain hidden instructions (ANSI codes/Unicode/HTML comments)
2. **Dynamic behavior monitoring**: Compare initial registration vs. runtime tool descriptions for consistency
3. **Cross-server isolation**: Verify that tool names do not conflict in multi-server environments
4. **Credential storage audit**: Check OAuth Token/API Key storage method (plaintext vs. encrypted)
5. **Input validation testing**: Perform command injection/SQL injection testing on tool parameters
6. **Permission boundary testing**: Verify that tools cannot access resources outside their declared scope

### AI Agent Security (OWASP ASI01-ASI10 Supplement)

#### Clawdbot/Moltbot Real-World Case (January 2026)

AI Agent security incident with 4,500+ exposed instances discovered globally:
- **Root cause**: Reverse proxy misconfiguration caused localhost authentication to pass automatically
- **Impact**: API keys, service tokens, and WhatsApp session credentials were extracted
- **Lesson**: AI Agents concentrate high-privilege capabilities — shell execution, persistent state, autonomous task initiation — single-point exposure = complete takeover

#### Agent Tool Selection Attack (CATS Research)

- Tool pool treated as an uncontrolled repository; attackers can publish tools with misleading metadata
- Under adversarial attacks, Agent tool selection authentication accuracy drops 60%+
- After adaptive adversarial attacks, accuracy falls below 20%

#### ASI07: Multi-Agent Communication Security

| Attack vector | Description |
|----------|------|
| Message forgery | Agent A impersonates Agent B to send instructions |
| Trust delegation abuse | Low-privilege Agent exploits trust relationship of high-privilege Agent |
| Coordination hijacking | Manipulate task assignment and result aggregation between Agents |
| Man-in-the-middle attack | Intercept and tamper with inter-Agent communications |

#### ASI09: Human-Machine Trust Exploitation

- Over-reliance: Users execute AI output without verification
- Social engineering enhancement: AI-generated phishing content is more convincing
- Confirmation bias: Users tend to trust AI output that matches their expectations
- Automation bias: "AI must be right" mentality

#### ASI10: Malicious/Out-of-Control Agent

- Agent operates outside authorized parameters after compromise
- Goal drift in autonomous decision chains
- Lateral movement: infecting other Agents through inter-Agent communication

### Skills/Rules Supply Chain Security

#### Attack Surface

AI coding assistants (Claude Code/Cursor etc.) introduce a new supply chain attack surface through their Skills and Rules systems:

| Attack vector | Description | Impact |
|----------|------|------|
| Malicious skill injection | Community-shared skills contain embedded malicious Prompt instructions | AI executes hidden commands (e.g., data exfiltration) |
| Rules file tampering | Modify .cursorrules/.claude/RULES.md via PR | Long-term control over developer's AI behavior |
| SKILL.md poisoning | Reference files loaded by skill contain embedded indirect injection | AI executes malicious instructions when reading reference |
| Dependency chain attack | External MCP server that skill depends on is replaced | All users of that skill are affected |
| Build hook exploitation | Trigger malicious build operations through skill scripts/ | Code execution, key theft |

#### Claude Code Disclosed CVEs (2025-2026)

| CVE | Severity | Description |
|-----|--------|------|
| CVE-2025-54795 | High | echo command bypasses user approval for direct execution |
| GHSA-qxfv-fcpc-w36x | High | rg command injection bypasses approval Prompt |
| - | High | sed command validation bypass enables arbitrary file write |
| - | High | Commands executable before trust dialog is launched |
| - | Moderate | Malicious repo configuration leads to data leakage |

#### Defense Recommendations

- **Skill audit**: Review SKILL.md and all reference files before installing a skill
- **Signature verification**: Verify skill source and integrity (no official mechanism yet — manual review required)
- **Permission isolation**: Limit tools and file scope accessible to a skill
- **Rules protection**: Include .cursorrules and AGENTS.md in the code review process
- **MCP server allowlist**: Allow only trusted MCP servers to connect
- **Behavior monitoring**: Log all tool calls and file operations by AI assistants

### Agentic AI Comprehensive Security Testing Framework

Systematic testing workflow for AI Agent applications based on OWASP ASI01-ASI10:

1. **Target enumeration**: Identify all Agents, tools, MCP servers, and communication channels
2. **Authentication testing**: Agent identity verification, token management, permission boundaries (ASI03)
3. **Tool security**: Description audit, parameter injection, permission boundary violation (ASI02)
4. **Injection testing**: Direct/indirect Prompt injection, tool return value injection (ASI01)
5. **Supply chain audit**: MCP server source, skill integrity, dependency security (ASI04)
6. **Code execution**: Sandbox escape, command injection, file operations (ASI05)
7. **Memory security**: Context poisoning, persistent attacks, state corruption (ASI06)
8. **Communication security**: Inter-Agent authentication, message integrity, trust delegation (ASI07)
9. **Cascade testing**: Single-point failure propagation scope, fault isolation (ASI08)
10. **Trust testing**: Output validation mechanisms, human approval workflows (ASI09)
11. **Escape testing**: Agent behavior monitoring, anomaly detection, Kill Switch (ASI10)
