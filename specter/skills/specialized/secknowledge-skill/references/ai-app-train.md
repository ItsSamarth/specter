# AI Application Security - Training Phase

> Source: AISS NSFOCUS Large Model Security Intelligence Chain Community | Split from ai-app-security.md
> Phase: Training phase (GAARM.0034-0036 third-party components/plugins/insecure code)

## Training Phase

### LLMs Application Insecure Output Handling

> Risk ID: GAARM.0035.003
> Lifecycle: Training phase

**Attack Overview**

This risk refers to a security risk that arises when downstream components accept the output of a large language model (LLM) without proper review. The model's downstream components include Agents with various functions; when output handling is lacking, an attacker can abuse the Agent through the model to carry out an attack. For example, an attacker can input specific text to induce the LLM to output a response containing sensitive information and thereby steal user data, or directly output an unexpected attack payload, causing downstream vulnerabilities such as RCE or SSRF.

**Attack Cases**

Case
Description




Case 1
CVE-2023-29374 is an arbitrary code execution vulnerability in Langchain. Programs using Langchain version 0.0.131 and earlier that call the Langchain LLMMathChain chain have a security risk involving arbitrary command execution, which may lead to leakage of sensitive information such as the OpenAI key, and to the Langchain server being controlled.


Case 2
Auto-GPT has a path traversal vulnerability in versions prior to v0.4.3. This vulnerability allows arbitrary code on the host running Auto-GPT to be executed outside the docker environment. An attacker can exploit it to launch targeted attacks against a target, harming the security of the site's systems.

**Attack Risks**

Sensitive information leakage: the LLM sometimes does not sanitize JavaScript in its responses. In such cases, an attacker may use a carefully crafted prompt to cause the LLM to return a JavaScript payload; when the victim's browser parses the payload, it is attacked, leading to sensitive information leakage such as conversation history disclosure.
Arbitrary code execution: an attacker can execute arbitrary code through the vulnerability. This may allow the attacker to perform malicious operations on the server, such as planting a backdoor, extracting sensitive data, or disrupting the service.
Targeting.

**Mitigations**

Mitigation
Description




Zero trust framework
In this framework, every request to access a resource is treated as coming from an untrusted network; the system inspects, authenticates, and verifies it to provide system security.


Sandbox environment
Attempt to use a sandbox environment to execute code to ensure greater system security. For example, executing code only inside a dedicated, ephemeral Docker container can significantly limit the potential impact of malicious code.

**References**

https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf
https://cloud.baidu.com/article/3253170
https://www.akto.io/blog/insecure-output-handling-in-llms-insights
https://journal.hexmos.com/insecure-output-handling/
https://systemweakness.com/new-prompt-injection-attack-on-chatgpt-web-version-ef717492c5c2

---
### LLMs Application Traditional Vulnerability Risk

> Risk ID: GAARM.0035.002
> Lifecycle: Training phase

**Attack Overview**

Traditional application security vulnerabilities exist not only in traditional software systems but may also exist in LLM applications. For example, common API interface attacks, account takeover, code execution, and so on — traditional risk vulnerabilities still exist in LLMs. Therefore, during the training phase, security best practices must be strictly followed to ensure the system has sufficient protection against traditional risks; otherwise it may lead to a series of dangers such as service disruption, account takeover, and data tampering.

**Attack Cases**

Case
Description




Case 1
This case reported signs of ChatGPT being subjected to a DDoS (distributed denial of service) attack, where an external attacker attempted to overload and crash the network or server by repeatedly sending Ping requests.


Case 2
The ChatGPT-Next-Web application has an SSRF vulnerability (CVE-2023-49785), which can be used to probe intranet network resources.

**Attack Risks**

Service disruption: a denial-of-service (DoS) attack or resource exhaustion causes the LLM application to be unable to respond to user requests, affecting business continuity.
System control: a remote code execution or script execution vulnerability may allow an attacker to take over the server, plant malware, or perform destructive operations.

**Mitigations**

Mitigation
Description




Harden API security
Ensure all API interfaces undergo strict authentication and authorization control, restricting access privileges.


Principle of least privilege
Restrict or disable unnecessary command-execution functionality in the LLM application to reduce the potential attack surface.


Regular security assessment
Regularly scan the LLM application for security vulnerabilities and promptly patch any discovered security issues.

**References**

https://sec.cafe/handbook/security_research/ai_security/llm_security/attack/

---
### LLMs Plugins: Insecure Input Handling

> Risk ID: GAARM.0035.001
> Lifecycle: Training phase

**Attack Overview**

This risk refers to insecure input handling in LLM plugins introducing risk into the large model. For example, a plugin may accept free-text input from the model without validation or type checking to handle context-size limits, allowing a potential attacker to craft a malicious request to send to the plugin, which may lead to various undesirable behaviors, even including remote code execution.

**Attack Cases**

Case
Description




Case 1
The PALChain in LangChain was found to have a code-execution risk.

**Attack Risks**

Unauthorized request execution: an attacker can directly exploit an LLM application vulnerability or, by manipulating the input prompt, make the LLM application perform unexpected requests and access or operate restricted resources.
Sensitive information leakage: accessing restricted resources through the LLM may lead to unauthorized acquisition and leakage of sensitive information.

**Mitigations**

Mitigation
Description




Input validation and filtering
Implement strict input validation and sanitization policies to ensure all input data is inspected and cleaned before being processed by the LLM.


Principle of least privilege
Follow the principle of least privilege, providing the LLM only the minimum access necessary to complete its task and avoiding over-authorization.

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/SSRF.html
https://www.horizon3.ai/attack-research/attack-blogs/nextchat-an-ai-chatbot-that-lets-you-talk-to-anyone-you-want-to/
https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf

---
### LLMs Plugins: Excessive Business Agency

> Risk ID: GAARM.0036
> Lifecycle: Training phase

**Attack Overview**

LLM-based systems are usually granted a degree of business agency by developers — that is, the ability to interact with other systems and perform operations in response to prompts. Excessive agency is a design-and-development-phase security risk that causes destructive operations to be performed when the LLM produces unexpected/ambiguous output; the root cause is usually too much functionality or too much autonomy. Excessive agency can lead to a range of impacts on confidentiality, integrity, and availability, depending on which systems the LLM application can interact with. For example, granting the LLM system excessive autonomy causes the LLM, when the application or plugin fails to independently verify and approve high-impact operations, to allow a plugin that can delete user documents to perform the deletion without any confirmation from the user.

**Attack Cases**

Case
Description




Case 1
This video demonstrates how to illegally reset a user's password by exploiting an excessive-agency vulnerability.

**Attack Risks**

Sensitive information leakage: excessive business agency may leak sensitive information and privacy when the LLM is maliciously manipulated.

**Mitigations**

Mitigation
Description




Principle of least privilege
Restrict the plugins/tools the LLM agent is allowed to call to only the minimum functionality required. For example, if the LLM-based system does not need the ability to fetch URL content, then such a plugin should not be provided to the LLM agent.


Avoid open-ended functionality
Where possible, avoid open-ended functionality (e.g., running shell commands, fetching URLs, etc.) and use plugins/tools with finer-grained functionality. For example, an LLM-based application may need to write certain output to a file. If a plugin that runs shell functionality is used to achieve this, the scope of undesired operations becomes very large (any other shell command could be executed). A safer alternative is to build a file-writing plugin that supports only that specific functionality.

**References**

https://genai.owasp.org/wp-content/uploads/2024/05/OWASP-Top-10-for-LLM-Applications-v1_1_Chinese.pdf

---
### RAG Development Framework Vulnerabilities

> Risk ID: GAARM.0034.002
> Lifecycle: Training phase

**Attack Overview**

RAG (Retrieval-Augmented Generation) is a framework that combines information retrieval and generation, used in the development of large language models (LLMs) to enhance the model's generation capability. Because the RAG framework relies on the retrieval module to obtain information from external data sources, if the retrieval module's source data is inaccurate or unreliable, the generated answers may contain incorrect or misleading information; and the various Agents introduced by the framework itself may also have related security risks. The security risks associated with the RAG framework are mainly concentrated in the RAG generation module, information retrieval module, integration plugins, and external interfaces. Due to insecure RAG design, security vulnerabilities may be introduced into the LLM application. For example, if the design of the RAG retrieval module allows the server to make unrestricted requests, it may lead to exploitation of an SSRF vulnerability.

**Attack Cases**

Case
Description




Case 1
Due to the SSRF in the LangChain framework and the RCE vulnerability in PALChain, security risks were introduced to LLM applications using the framework.

**Attack Risks**

Information leakage: an attacker may access sensitive files or system configuration files through a path traversal vulnerability, leaking internal system information.
System control: if system files contain sensitive configuration information or scripts, an attacker may further use this information to control the system.
Command execution: Agents in the framework such as data expression evaluation and the Python interpreter may be exploited to cause RCE attacks.

**Mitigations**

Mitigation
Description




Input validation
Strictly validate and sanitize all user input to prevent path traversal attacks.


Permission management
Set appropriate file permissions to prevent unauthorized file access.


Updates and patching
Ensure the application and related dependencies are at the latest version and promptly apply security patches to fix known vulnerabilities.

**References**

https://www.wehelpwin.com/article/5063
https://medium.com/nfactor-technologies/rag-poisoning-an-emerging-threat-in-ai-systems-660f9ff279f9
https://ironcorelabs.com/security-risks-rag/

---
### Insecure Code Practices

> Risk ID: GAARM.0035
> Lifecycle: Training phase

**Attack Overview**

Insecure code practices refer to security issues caused by design flaws during the development of LLM applications based on large-model integration frameworks. The code logic adopted during LLM application development may introduce security risks, bringing exploitable security vulnerabilities into the LLM application. The security vulnerabilities may include two major categories:

The LLM application service has traditional vulnerabilities, such as an externally facing Chat system service having risks like unauthorized viewing of others' conversation records;
New-style Tools, Agents, and Chains in the LLM integration framework contain security risks, allowing an attacker to indirectly exploit the related vulnerabilities through the LLM;

**Attack Cases**

Case
Description




Case 1
The PALChain in LangChain was found to have a code-execution risk.


Case 2
Multiple high-severity RCE vulnerabilities were discovered in LangChain.

**Attack Risks**

Insecure coding practices: the LLM may follow insecure coding practices when generating code, resulting in generated code that contains security vulnerabilities.
Unauthorized request execution: an attacker can directly exploit an LLM application vulnerability or, by manipulating the input prompt, make the LLM application perform unexpected requests and access or operate restricted resources.

**Mitigations**

Mitigation
Description




Automated detection and assessment
Use static analysis tools to detect insecure patterns in the code to improve code security.


Principle of least privilege
Follow the principle of least privilege, providing the LLM only the minimum access necessary to complete its task and avoiding excessive agency authorization.


Input validation and filtering
Implement strict input validation and sanitization policies to ensure all input data is inspected and cleaned before being processed by the LLM.

**References**

https://arxiv.org/html/2312.04724v1

---
### Data Processing Component Vulnerabilities

> Risk ID: GAARM.0034.001
> Lifecycle: Training phase

**Attack Overview**

In the development of artificial intelligence (AI) models, the security of datasets is an important aspect that cannot be ignored. Platforms such as Hugging Face and GitHub may contain datasets with malicious backdoors, and these datasets can threaten the security of AI models through the characteristics or vulnerabilities of LLM data processing components. When developers use these contaminated datasets for model training, malicious code hidden in the dataset may be executed, leading to a series of security issues such as leakage or tampering of the AI model, dataset, and code.

**Attack Cases**

Case
Description




Case 1
Hugging Face's datasets component was found to have insecure characteristics; loading a malicious dataset with this component may lead to risks such as command execution.

**Attack Risks**

System compromise: a malicious script crafted by the attacker can connect to the attacker's server and execute system commands, thereby controlling the victim's server.
Data leakage: a malicious script can steal sensitive data on the server such as training data and model code, leading to leakage of intellectual property and user privacy.
Model parameter tampering: the parameters of the large model may be maliciously tampered with, affecting the model's accuracy and reliability.

**Mitigations**

Mitigation
Description




Trusted sources for training/fine-tuning datasets
Ensure the source dataset is trustworthy, check whether the dataset scripts contain malicious Python code, and be cautious about using datasets flagged as a security risk on Hugging Face.


Supply-chain security protection for large-model components
Continuously follow the latest supply-chain security developments and recommendations in areas such as large-model native security, foundational security, and large-model-enabled R&D security.

**References**

https://security.tencent.com/index.php/blog/msg/209

---
### Third-Party Component Vulnerabilities

> Risk ID: GAARM.0034
> Lifecycle: Training phase

**Attack Overview**

This attack refers to LLM application developers potentially using third-party commercial or open-source library components during the model training phase. These third-party components may contain malicious code, component vulnerabilities, etc., which may lead to development machines and servers being compromised — a supply-chain security risk in the AI context.

**Attack Cases**

Case
Description




Case 1
The Redis database Python client redis-py uses an asynchronous interface; canceling a command may cause user business data to be read in a corrupted order (CVE-2023-28858).


Case 2
TorchServe can lead to unauthorized server access and achieve remote code execution on vulnerable instances.


Case 3
Hugging Face's datasets component has a vulnerability allowing attacks via malicious datasets, which may lead to user devices being compromised and large-model parameters being stolen or tampered with.


Case 4
This paper studies the impact of backdoor attacks on pre-trained models. An attacker can plant a backdoor to manipulate the model's recommendation results, thereby achieving malicious marketing or other purposes.


Case 5
ChatGPT-Next-Web has SSRF and reflected XSS vulnerabilities.

**Attack Risks**

Supply-chain backdoor poisoning attack: when an AI developer uses a third-party open-source library to load a dataset, if the dataset has been planted with malicious code, the PC or server may be attacked.
Model parameter leakage or tampering: leading to model parameters being stolen or tampered with, affecting the model's security and reliability.

**Mitigations**

Mitigation
Description




Supply-chain security protection for large-model components
For known security vulnerabilities, such as TorchServe's CVE-2023-43654, promptly update to a secure version.


Trusted sources for training/fine-tuning datasets
Ensure the dataset source is trustworthy, check whether the dataset scripts contain malicious Python code, and avoid using datasets flagged as a security risk on Hugging Face.


Strictly control the introduction of open-source components
Establish an internal open-source governance system, strictly control the introduction of open-source components, and use tools to achieve automated monitoring and tracking.

**References**

https://hiddenlayer.com/research/insane-in-the-supply-chain/

---

---

