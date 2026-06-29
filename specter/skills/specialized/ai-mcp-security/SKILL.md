---
name: ai-mcp-security
description: AI and MCP security assessment — prompt injection, tool abuse, MCP trust boundaries, agent privilege escape, data leakage, model risk, GAARM risk matrix
---

# AI and MCP Security Assessment Skill

Use this Skill when the target includes an LLM, agent, MCP tools, Skills, RAG, Memory, Plugin, or model-serving components.

**Prerequisite**: If the AI surface is only a presentation layer and the real blocker is still a client-side signature or encryption protocol, return to the `client-reverse` Skill first.

## Scenario Routing

| Risk type | Preferred reference |
|---------|---------|
| Prompt injection / indirect injection / CoT interference | `references/ai-app-security.md` |
| Tool abuse / MCP poisoning / Skills supply chain | `references/04-ai-and-mcp-security-integrated.md` MCP chapter |
| Privilege escape / role boundary breach / credential abuse | `references/ai-identity-security.md` |
| Data leakage / prompt leakage / model inversion | `references/ai-data-security.md` |
| Container escape / CI-CD / sandbox failure | `references/ai-baseline-security.md` |
| Model risk / adversarial samples / backdoors | `references/ai-model-security.md` |
| Impact classification and coverage assessment | `references/gaarm-risk-matrix.md` |

## Testing Workflow

### 1. Application-Layer Attacks
- Direct prompt injection
- Indirect injection (via external data sources)
- CoT interference and instruction override
- Agent abuse (unauthorized operations)
- Code execution breakout
- Memory poisoning

### 2. MCP and Agent Risks
- Tool description poisoning
- Instruction override
- Hidden instruction injection
- Unauthorized resource access
- Skills/Rules supply chain issues

### 3. Identity and Authorization
- Action abuse
- Role escape
- Privilege drift
- Cloud credential abuse

### 4. Data and Privacy
- Prompt leakage
- Sensitive data exposure
- Training data issues
- Model inversion
- API data theft

### 5. Baseline and Deployment
- CI/CD flaws
- Container escape
- Vector database security
- Sandbox failure
- Environment isolation flaws
- Model-serving flaws

## Reference Documents

- `references/04-ai-and-mcp-security-integrated.md` — AI and MCP security integrated reference
- `references/ai-app-security.md` — AI application security
- `references/ai-identity-security.md` — AI identity security
- `references/ai-data-security.md` — AI data security
- `references/ai-baseline-security.md` — AI baseline security
- `references/ai-model-security.md` — AI model security
- `references/gaarm-risk-matrix.md` — GAARM risk matrix
