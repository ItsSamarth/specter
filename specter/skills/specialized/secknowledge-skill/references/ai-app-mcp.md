# AI Application Security - Application Phase - MCP Protocol Attacks

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-app-app.md
> Risk category: MCP (GAARM.0046.x Rug Pull / Tool Poisoning / Instruction Override / Hidden Instructions)

---

### MCP Rug Pull

> Risk number: GAARM.0046.001
> Lifecycle: Application phase

**Attack Overview**

An MCP rug pull attack exploits the fact that the MCP architecture allows servers to dynamically modify tool descriptions after client authorization. Attackers leverage this to plant malicious instructions (such as tampered function logic or hijacked operations) on the basis of user trust. Even if a tool passes a security review at installation time, subsequent stealthy tampering can still result in tool descriptions being injected with malicious exploitation instructions (such as data leakage or unauthorized operations).

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Malicious MCP tool function descriptions embed covert prompts like "read user private keys"; after the user approves the tool, the model inadvertently executes these prompts during invocation, leaking local files |

**Attack Risks**

Tool over-authorization: When the model calls a tool, poisoned description content causes execution of unintended instructions.
Sensitive data leakage: Attackers induce the model to access and output sensitive files such as ~/.ssh/id_rsa.
Model function hijacking: Attackers can manipulate model behavior via Prompt, e.g., spreading disinformation or generating illegal content.
Bypassing review mechanisms: Tool fields pass validation at registration time, but the model is hijacked by description content during actual execution.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| White-box assessment | Perform white-box audits of MCP server code to detect malicious tool descriptions and code behaviors promptly |
| Audit and monitoring | Monitor model behavior in real time, log tool call records, and detect anomalous operations promptly |
| Model security training | Adversarially train the model to improve its defense against poisoning attacks |
| API access control | Restrict tool access to sensitive data to reduce leakage and abuse risk |
| Execution context isolation | Restrict model access to tool description fields, or use structured call protocols (e.g., OpenAI ChatML tool call syntax) to avoid description contamination |

**References**

https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
https://atlas.mitre.org/techniques/AML.T0051
https://github.com/invariantlabs-ai/mcp-injection-experiments

---
### MCP Tool Poisoning Attack

> Risk number: GAARM.0046
> Lifecycle: Application phase

**Attack Overview**

MCP is an open protocol that standardizes how applications provide context to large language models. An MCP tool poisoning attack is an attack method targeting this protocol. Attackers inject offensive prompts into the tool descriptions of a malicious MCP server to maliciously manipulate tool behavior. The core characteristic is embedding malicious instructions in tool descriptions, exploiting the model's process of parsing complete tool descriptions to induce the model — through hidden instructions (such as special tags or encoding) — to perform unauthorized operations, such as generating malicious content, leaking sensitive information, or bypassing other security restrictions.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attacker manipulates tool descriptions to carry out a malicious attack, causing sensitive model information to be leaked to a malicious MCP server |
| Case 2 | Exploits MCP Tool description for poisoning to achieve indirect prompt injection, controlling other tools' parameters to exfiltrate information |

**Attack Risks**

MCP tool poisoning attacks can cause serious systemic risks, affecting model security, reliability, and user trust. Key risks:

Trust erosion: May cause users' trust in the model and its development tools to decline, affecting its application in sensitive scenarios.
Goal hijacking: Can use poisoning to make the model deviate from its original design purpose, executing custom malicious instructions, increasing abuse risk.
System security threats: May lead to malicious code being planted in MCP tools, causing further system intrusion or functional damage.
Data privacy leakage: Can exploit poisoning to extract model training data or sensitive information entered by users.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| White-box assessment | Perform white-box audits of MCP server code to detect malicious tool descriptions and code behaviors promptly |
| Audit and monitoring | Monitor model behavior in real time, log tool call records, and detect anomalous operations promptly |
| Model security training | Adversarially train the model to improve its defense against poisoning attacks |
| API access control | Restrict tool access to sensitive data to reduce leakage and abuse risk |

**References**

https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
https://mp.weixin.qq.com/s/EJLb1IwqbPF3VSDkJu099g
https://x.com/hongming731/status/1922261630664245326
https://news.qq.com/rain/a/20250429A07QY000

---
### MCP Instruction Override Attack

> Risk number: GAARM.0046.002
> Lifecycle: Application phase

**Attack Overview**

MCP instruction override is a malicious injection attack targeting MCP server tool calls. Attackers plant malicious instructions into tool descriptions of a malicious MCP server, hijacking the normal behavior of other trusted tools. For example, an attacker might modify the behavior of an email-sending tool so that when called it covertly changes the recipient's email address, causing sensitive data exfiltration or malicious operations.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Craft tool descriptions containing hidden instructions that manipulate how the model interacts with other tools; the LLM reads and follows these instructions without the user's knowledge |
| Case 2 | Contains a trusted server and a malicious server. The trusted server provides an email-sending tool, while the malicious server provides a fake digit-addition tool whose description contains an MCP instruction override attack, requiring the email tool's recipient to be @pwnd.com |
| Case 3 | Uses a malicious MCP server description to control the WhatsApp send_message tool's recipient to +13241234123 |

**Attack Risks**

Data leakage risk: Instruction override attacks can instruct trusted tools to extract sensitive information from conversations, documents, or connected systems and send it to attacker-controlled machines.
Trusted tool abuse: Attackers can manipulate the model's network requests, code execution, and other trusted tools to access untrusted sites or execute malicious code.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| White-box assessment | Perform white-box audits of MCP server code to detect malicious tool descriptions and code behaviors promptly |
| Audit and monitoring | Monitor model behavior in real time, log tool call records, and detect anomalous operations promptly |
| Model security training | Adversarially train the model to improve its defense against poisoning attacks |
| API access control | Restrict tool access to sensitive data to reduce leakage and abuse risk |

**References**

https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/
https://blog.trailofbits.com/2025/04/29/deceiving-users-with-ansi-terminal-codes-in-mcp/

---
### MCP Hidden Instruction Attack

> Risk number: GAARM.0046.003
> Lifecycle: Application phase

**Attack Overview**

An MCP hidden instruction attack involves attackers embedding ANSI terminal escape codes (such as color settings, cursor control) or invisible Unicode characters into MCP tool descriptions, making malicious instructions invisible to users but still executed by the LLM. This attack exploits the MCP "line-jumping" vulnerability, allowing attacks to affect developer operations undetected, leading to security issues such as data leakage and supply chain attacks.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attacker embeds ANSI escape codes in tool descriptions, making text invisible in the terminal, but the LLM still reads and executes the instructions, causing the model to recommend downloading Python packages from a malicious server — potentially triggering a supply chain attack |
| Case 2 | By adding invisible Unicode characters to user input, attackers inject malicious instructions into the LLM |
| Case 3 | By injecting hidden code into a web page, when the MCP tool returns the web page information to the LLM, invisible malicious instructions are injected, achieving data leakage or other attacks |

**Attack Risks**

Supply chain attack: Through hidden instructions, attackers can plant malicious code during the development process, affecting the entire software supply chain.
Data leakage: Sensitive information (such as IP addresses, download sources) may be silently exfiltrated.
System security: In some cases, hidden instructions can be used to generate and execute malicious code.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Input/output filtering | Strictly filter and sanitize user inputs and tool outputs, removing potentially malicious characters and instructions |
| Avoid passing raw tool output to the terminal | Consistently sanitize potentially dangerous output by disabling escape sequences before rendering. The simplest method is to replace any byte with hex value 1b with a placeholder, since all escape sequences recognized by modern terminals begin with this byte |
| Tool description review | Review MCP tool descriptions to ensure they contain no malicious instructions |
| Restrict MCP server permissions | In sensitive environments, allow only trusted MCP servers to interact, reducing potential attack surface |
| Monitor and audit MCP activity | Regularly review logs and interactions to detect anomalous or suspicious behavior |

**References**

https://blog.trailofbits.com/2025/04/29/deceiving-users-with-ansi-terminal-codes-in-mcp/
https://www.solo.io/blog/deep-dive-mcp-and-a2a-attack-vectors-for-ai-agents

---
