# AI Application Security - Deployment Phase

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-app-security.md
> Phase: Deployment phase (GAARM.0037-0038, 0049 API management / source code poisoning / theft)

## Deployment Phase

### LLMs Application API Mismanagement

> Risk number: GAARM.0049
> Lifecycle: Deployment phase

**Attack Overview**

LLMs application API mismanagement refers to the situation where sensitive API components such as Tools, Agents, and Chains within the LLM integration framework environment are not properly managed and configured in relation to the LLM environment. Because large language models typically need to interact with multiple APIs to execute tasks, if those APIs are not properly managed — e.g., incorrect access permissions or insufficient security controls — attackers can exploit these vulnerabilities to obtain sensitive information or execute malicious behavior, achieving unauthorized access, code execution exploitation, and other attacks.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Two main exploitation techniques targeting LLMs APIs are described below |

**Attack Risks**

Data leakage: Attackers may obtain sensitive data, including personally identifiable information, trade secrets, etc.
Service disruption: Malicious code execution or unauthorized access may cause service interruptions or performance degradation.
Legal and compliance risk: Security vulnerabilities may trigger lawsuits and compliance issues.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Principle of least privilege | Follow the principle of least privilege; provide LLMs only with the minimum access required to complete their tasks, avoiding over-delegation of authority |
| Input/output validation | Thoroughly validate all input sent through APIs to prevent injection attacks |
| Monitoring and logging | Monitor and log new-paradigm API activity in the AI era to quickly detect and respond to suspicious behavior |

---
### LLMs Application Source Code Poisoning

> Risk number: GAARM.0038
> Lifecycle: Training phase

**Attack Overview**

Source code may contain vulnerabilities during the review process. Attackers inject malicious code into the source code of LLMs applications, use vulnerability-hidden code to evade inspection, or poison the source code of third-party open-source or commercial components. This causes security issues during the application's training or execution and affects downstream model application business developers who use these components.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attackers can upload malicious code to open-source websites to manipulate models, affecting fields such as investment, trading, and news |

**Attack Risks**

Backdoor insertion: By injecting backdoor code into training data, attackers can control or manipulate model outputs during inference, leading to unauthorized access or data manipulation.
Supply chain attacks: By injecting malicious code into open-source code, attackers can affect the entire supply chain using that code.
Disinformation propagation: Attackers can use this technique to modify content — such as movie reviews or news reports — to spread false information or propaganda.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Detect deviations from original code | Identify and intercept anomalous behavior caused by malicious code modifications |
| Input validation and filtering | Perform strict input validation and cleaning before code is fed to the model |

**References**

https://drive.google.com/file/d/1CTVcliUblX35cWfB49Xjhf8xk-fM3QH1/edit?pli=1

---
### LLMs Application Source Code Theft

> Risk number: GAARM.0037
> Lifecycle: Training phase

**Attack Overview**

This risk refers to improper storage of model or LLM source code, or a deployment environment with security risks, which may allow unauthorized parties to attack the relevant deployment environment and steal LLM application source code, thereby damaging the enterprise's technical competitive advantage.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Meta's 65-billion-parameter language model was leaked |
| Case 2 | Large amounts of GPT-4 model architecture, training costs, datasets, and other information were leaked |

**Attack Risks**

Loss of technical advantage: Competitors may copy or modify leaked source code, weakening the enterprise's technical competitive edge.
Cybersecurity threat: Attackers can use leaked source code to design targeted cyber attacks, e.g., exploiting disclosed vulnerabilities for system intrusion.
Phishing risk: Leaked source code may be used to create more convincing phishing emails that mimic internal enterprise applications, increasing the risk of users being deceived.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Code encryption protection | Use strong encryption algorithms to encrypt LLM application source code, preventing unauthorized access and leakage |
| Access control | Restrict access to LLM application source code, ensuring only authorized personnel can view or modify the code |
| Model monitoring | Monitor model usage to ensure it is not used for malicious purposes |

**References**

https://analyticsindiamag.com/metas-llama-leaked-to-the-public-thanks-to-4chan/
https://knightcolumbia.org/blog/the-llama-is-out-of-the-bag-should-we-expect-a-tidal-wave-of-disinformation

---
