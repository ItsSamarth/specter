# AI Application Security - Application Phase - Agent and CoT Attacks

> Source: AISS NSFOCUS Large Model Security Intelligence Chain Community | Split from ai-app-app.md
> Risk category: Agent/CoT (GAARM.0041.x Agent exploitation and SSRF/RCE / 0042.x CoT injection and chain-of-thought interference / 0047 environment injection / 0056.001 query injection / 0060 unexpected code execution)

---

### CoT Injection Attack

> Risk ID: GAARM.0042
> Lifecycle: Application phase

**Attack Overview**

CoT (Chain of Thought) effectively improves the reasoning and problem-solving ability of LLMs by prompting them to think through a series of key steps to solve a problem. The ReAct (Reason + Act) technical framework implements CoT reasoning, and by leveraging Agent scheduling it gives LLMs the ability to interact with the external world, seamlessly connecting to various external systems and performing complex tasks.
In a CoT application, the user provides a natural-language question and the AI model generates a series of reasoning steps to answer it. This involves three core steps: Thought, Act, and Observation (Obs). The AI model loops through these three steps to reason about and solve various complex problems. Because the whole process is more open and flexible than traditional code logic and lacks a strict flow-control structure, an attacker can use a CoT injection attack to bypass specific reasoning steps and induce the AI model to perform unintended actions, such as: business-function risks (arbitrary user transfers, etc.) and technical-function risks (SSRF, RCE, etc.). There are currently two main approaches to CoT injection attacks:

Chain-of-thought interference injection: by observing the CoT scheduling process, the attacker crafts malicious input to deceive the model into believing it has already obtained an Agent's result; by forging the Agent's result, the attacker interferes with the CoT execution process.
Chain-of-thought manipulation injection: by observing the CoT scheduling process, the attacker directly — or by using adversarial attack techniques — crafts malicious input to manipulate the CoT process, causing the model to skip the preset CoT process and directly schedule a sensitive Agent.

**Attack Cases**

Case
Description




Case 1
This case mainly demonstrates how a ReAct-framework-based LLM application can be abused via its CoT chain-of-thought process to maliciously exploit Agents.


Case 2
This research found that by combining jailbreak prompts with CoT prompts, CoT can be used to bypass the LLM's ethical restrictions, causing the model to generate private information.


Case 3
An open-source CTF challenge for query injection attacks under the ReAct framework.

**Attack Risks**

In LLM applications that use information retrieval systems, an attacker can poison the information retrieval database so that malicious text fragments are injected into the query sent to the LLM, thereby affecting the final output and causing a series of risks such as user privacy leakage and malicious code execution.
In LLM applications for refund business systems, an attacker can interfere with the refund CoT process so that an order that originally did not meet the refund conditions can be refunded normally; or directly maliciously manipulate the refund-operation Agent so that the actual refund amount does not match the expected refund amount, causing financial loss to the enterprise.

**Mitigations**

Mitigation
Description




Strict permission control
Enforce strict privilege controls to ensure that LLMs can only access the necessary content and Agents, thereby minimizing potential vulnerability points.


LLMs Agent scheduling control
For Agents that perform sensitive operations, implement strict external automated or manual permission-verification mechanisms, preventing the LLM from directly holding the corresponding usage privileges.


Prompt content hardening
Adopt solutions such as OpenAI Chat Markup Language (ChatML) to attempt to isolate the genuine user prompt from other content.

**References**

http://youtube.com/watch?v=7ZA0Z1R-MjQ
http://youtube.com/watch?v=KksYizcLFH0

---
### SSRF Environment Simulation Probing

> Risk ID: GAARM.0041.001
> Lifecycle: Application phase

**Attack Overview**

SSRF usually arises because the server provides functionality to fetch data from other server applications without filtering or restricting the target address. If an SSRF vulnerability exists in an LLM application, an attacker can exploit it to make internal network requests and access restricted resources inside the application. In addition, some LLMs may have built-in Agents with network-access capabilities used to perform operations such as external information queries. An attacker can leverage an SSRF vulnerability in the LLM application API, or an Agent within the LLM that has network-access capabilities, to make unexpected requests or access restricted resources (such as internal services, APIs, or data stores), and then access the model's internal systems, increasing the risk of leaking data such as model information, internal services, and sensitive data.

**Attack Cases**

Case
Description




Case 1
The ChatGPT-Next-Web application has an SSRF vulnerability (CVE-2023-49785), which can be used to probe intranet network resources.

**Attack Risks**

Accessing internal resources: an attacker can use the SSRF vulnerability to send requests and obtain sensitive information in the internal network.
Attack traffic proxying: by exploiting the SSRF vulnerability, an attacker can send malicious requests to attack internal systems, services, or resources.
Data leakage: an attacker may use this risk to obtain sensitive data, such as cloud-platform access keys.

**Mitigations**

Mitigation
Description




LLMs API scheduling control and sandbox isolation
Implement appropriate sandboxing mechanisms to isolate the LLM and limit its access to network resources, internal services, and APIs. By enforcing strict access controls, organizations can minimize the possibility of unauthorized interactions and mitigate the impact of SSRF vulnerabilities.


LLMs periodic security assessment and review
Conduct regular audits and reviews of network and application security settings to identify and address any misconfigurations, ensuring that internal resources are not inadvertently exposed to the LLM and strengthening the overall security posture.


Input/output validation
Implement robust input validation and processing techniques to ensure prompts are thoroughly inspected and filtered. This helps prevent malicious or unexpected prompts from triggering unauthorized requests, thereby reducing the risk of SSRF attacks.


Monitoring and logging
Implement comprehensive monitoring and logging mechanisms to track LLM interactions. By closely monitoring the LLM's activity and logging relevant information, organizations can detect and analyze potential SSRF vulnerabilities, enabling timely detection and remediation.

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/SSRF.html

---
### Code Execution Injection

> Risk ID: GAARM.0041.002
> Lifecycle: Application phase

**Attack Overview**

Under the ReAct framework, LLMs can interact with external systems, and an external code-interpreter Agent can be used to provide LLMs with code-execution capability, enabling needs such as automated chart drawing and complex code computation during business application processes. An attacker constructs malicious input prompts to manipulate the LLM into executing a predetermined reasoning process, causing the LLM to schedule the code-execution Agent to run malicious code, commands, and other operations on the underlying system, thereby attacking and exploiting the LLM's base runtime environment. The main causes of this attack are:

Failure to effectively detect, validate, or restrict user input, allowing an attacker to carry out unauthorized malicious code-execution operations.
Insufficient sandboxing or insufficient capability restriction of the LLM, causing it to interact with the underlying system in unexpected ways.
Unintentionally exposing system-level functions or interfaces to the LLM.

**Attack Cases**

Case
Description




Case 1
After GPT-4's new features were launched, the Python code interpreter was found to apparently have a sandbox-escape vulnerability.

**Attack Risks**

Code execution risk: an attacker can execute arbitrary Python code, which may lead to server compromise, data leakage, or other malicious behavior.
System privilege control: if the CodeExecutor lacks appropriate security measures, the executed code combined with attack techniques such as container escape may obtain elevated system privileges.
Persistent access control: an attacker may use this opportunity to establish a long-term access channel for continuous attacks.

**Mitigations**

Mitigation
Description




Input validation
Implement strict input detection and restriction processes to prevent malicious or unexpected prompts from being processed by the LLM.


Principle of least privilege
Ensure proper sandboxing and restrict the LLM's capabilities to limit its ability to interact with the underlying system, avoiding operations that could cause system-level impact.


Monitoring and logging
Log all operations performed through the LLM and conduct real-time monitoring to quickly detect and respond to suspicious activity.

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Unauthorized_Code_Execution.html
https://www.calvin-risk.com/blog/decoding-llm-risks-a-comprehensive-look-at-unauthorized-code-execution

---
### Application Agent Exploitation

> Risk ID: GAARM.0041
> Lifecycle: Application phase

**Attack Overview**

LLM application APIs fall mainly into two application scenarios, so the API exploitation risk centers on the following two scenarios:


An LLM application platform provides service capabilities externally based on an API;

An attacker exploits API security risks present in the API interfaces of large models (such as OpenAI's GPT series) to carry out the attack, collecting information about the API interface to look for vulnerabilities, and based on the discovered vulnerabilities crafting malicious API requests in an attempt to bypass authentication or inject malicious code. For example: accessing or performing higher-privileged operations in an unauthorized manner, or executing malicious code commands by exploiting vulnerabilities in the externally exposed API interface.


LLMs Agent scheduling and third-party application integration use APIs to connect relevant capabilities to the model;

An attacker leverages the model's API-access capability for accessing sensitive information or operations and, based on the API access privileges, indirectly crafts malicious prompts to make the model perform dangerous operations, such as accessing sensitive information or tampering with system configurations. Because the model itself has the ability to operate and call the API and holds the corresponding access privileges, malicious operations may bypass normal security controls and launch actual malicious attacks. This attack may lead to risks such as privilege escalation and unauthorized access to others' information.

**Attack Cases**

Case
Description




Case 1
A normal user account could originally only use the GPT-3.5 model, but through a specific API address, the attacker could gain unauthorized access to the GPT-4 model.


Case 2
The attacker used the API to directly execute commands on the system and delete files.


Case 3
Building multiple LLM API application scenarios, the attacker maliciously abuses API functionality based on the LLM to achieve attacks such as command execution and account deletion.


Case 4
Stable Diffusion provides an API interface that allows developers to programmatically call the model to generate images. The attacker exploited this by crafting malicious text prompts and then, through Stable Diffusion's API interface, made the model generate illegal or extremist image content.

**Attack Risks**

Data leakage: an attacker may obtain sensitive data such as user information and passwords.
Service disruption: malicious operations may cause service disruption, such as deleting user records or database entries.
Loss of trust: inaccurate or sensitive information generated by the LLM may damage the trust of users and the organization.
Legal liability: due to inappropriate content generated by the LLM, the organization may face legal liability.

**Mitigations**

Mitigation
Description




LLMs API scheduling control
Restrict the APIs and data that the LLM can access to minimize the potential harm when exploited.


Input/output validation
Carefully sanitize user input to prevent malicious prompts from being injected into the LLM.


Monitoring and logging
Log all operations performed through the LLM and conduct real-time monitoring to quickly detect and respond to suspicious activity.


Human-in-the-loop approval
Give users more control so they can manage plugin usage and the flow of data.

**References**

https://portswigger.net/web-security/llm-attacks

---
### Chain-of-Thought Interference Injection

> Risk ID: GAARM.0042.001
> Lifecycle: Application phase

**Attack Overview**

This risk is a sub-risk of the CoT injection attack. By observing the CoT scheduling process, the attacker crafts malicious input to deceive the model into believing it has already obtained a correct agent result; by forging the agent result, the attacker interferes with the CoT.

**Attack Cases**

Case
Description




Case 1
This case demonstrates interference with the CoT, deceiving the model by crafting input to achieve an illegitimate goal.

**Attack Risks**

Interference injection: by crafting malicious input, the attacker interferes with the LLM and thereby performs non-compliant operations.

**Mitigations**

Mitigation
Description




Strict permission control
Ensure the LLM can only access essential content, minimizing potential points of violation.


Add human oversight
Add a layer of verification as a safeguard against unexpected LLM behavior.


Set clear trust boundaries
Treat the LLM as untrusted, always maintain external control in decision-making, and stay vigilant about potentially untrustworthy LLM responses.

**References**

https://labs.withsecure.com/publications/llm-agent-prompt-injection

---
### Chain-of-Thought Manipulation Injection

> Risk ID: GAARM.0042.002
> Lifecycle: Application phase

**Attack Overview**

This risk is a sub-risk of the CoT injection attack. By observing the CoT scheduling process, the attacker crafts malicious input to make the model skip the preset CoT process and directly schedule a sensitive Agent. For example, skipping a preset verification step allows the user to directly perform operations that should only be executable after verification.

**Attack Cases**

Case
Description




Case 1
This case demonstrates direct manipulation of the CoT: by crafting input to deceive the model, the model skipped a verification step that should have been performed and refunded a large sum to the user without review.


Case 2
The attacker combined multiple adversarial attack techniques: after bypassing the previous prompt rules via a role-escape attack, they used CoT manipulation injection to successfully call the approveTransfer function and complete the transfer operation.

**Attack Risks**

Manipulation injection: by crafting malicious input, the attacker controls the LLM and thereby performs non-compliant operations.

**Mitigations**

Mitigation
Description




Strict permission control
Ensure the LLM can only access essential content, minimizing potential points of violation.


Add human oversight
Add a layer of verification as a safeguard against unexpected LLM behavior.


Set clear trust boundaries
Treat the LLM as untrusted, always maintain external control in decision-making, and stay vigilant about potentially untrustworthy LLM responses.

**References**

https://labs.withsecure.com/publications/llm-agent-prompt-injection

---
### Query Injection Attack

> Risk ID: GAARM.0056.001
> Lifecycle: Application phase

**Attack Overview**

This risk is a sub-technique of the CoT injection attack. Query injection attacks are mainly used to exploit the data-query Agent in a CoT application to leak arbitrary data. In a CoT application, the user provides a natural-language question and the AI model generates a series of reasoning steps to answer it. The attacker can inject malicious SQL code into the question in an attempt to bypass the model's security checks and directly access the backend database. When a CoT chain-of-thought application externally connects to an attached database such as a traditional database, a vector database, or a knowledge graph, an Agent is needed to query and obtain external data. The attacker can interfere with or manipulate the CoT process; for example, when querying external data, the model mistakenly treats the user-supplied statement as external data, causing arbitrary data to be queried and obtained.

**Attack Cases**

Case
Description




Case 1
An open-source CTF challenge for query injection attacks under the ReAct framework.

**Attack Risks**

In LLM applications that use information retrieval systems, an attacker can poison the information retrieval database so that malicious text fragments are injected into the query sent to the LLM, thereby affecting the final output and causing a series of risks such as user privacy leakage and malicious code execution.

**Mitigations**

Mitigation
Description




Strict permission control
Enforce strict privilege controls to ensure that LLMs can only access the necessary content and Agents, thereby minimizing potential vulnerability points.


LLMs Agent scheduling control
For Agents that perform sensitive operations, implement strict external automated or manual permission-verification mechanisms, preventing the LLM from directly holding the corresponding usage privileges.


Prompt content hardening
Adopt solutions such as OpenAI Chat Markup Language (ChatML) to attempt to isolate the genuine user prompt from other content.

**References**

http://youtube.com/watch?v=7ZA0Z1R-MjQ
http://youtube.com/watch?v=KksYizcLFH0

---
### Environment Injection Attack

> Risk ID: GAARM.0047
> Lifecycle: Application phase

**Attack Overview**

An environment injection attack refers to an attacker using the indirect prompt injection approach to embed malicious instructions into external web pages, interfaces, emails, and other environments. When the AI Agent processes the external content, it executes the embedded instructions as if they were user instructions, leading to data leakage or achieving the goal of controlling the model or stealing data. The attacker may, by tampering with environment variables, modifying dependency libraries, or poisoning configuration files, induce the model to generate erroneous output, leak sensitive information, or perform unauthorized operations.

**Attack Cases**

Case
Description




Case 1
The attacker created a malicious issue containing a prompt injection in a public repository. When a user sent a routine request to Claude, the AI fetched the public-repository issue and triggered the malicious instruction, which then pulled private-repository data into the context and created a PR in the public repository containing the private data, causing data leakage.

**Attack Risks**

Environment injection attacks can pose serious threats to the model development and deployment ecosystem. The main risks are:

Malicious output generation: an attacker can use environment injection to induce the model to generate false information or harmful content, misleading users or triggering a crisis of trust.
Data leakage: by tampering with the environment configuration, an attacker may obtain sensitive information such as training datasets, user prompts, or API keys.
System integrity compromise: malicious injection may corrupt the development environment, affecting the stability of model training or deployment, and may even plant backdoor programs.
Supply chain attack: by poisoning third-party dependency libraries or toolchains, an attacker can affect multiple model development projects, creating widespread security hazards.
Crisis of trust: a successful attack may weaken users' trust in the model and its development environment, limiting its application in high-security scenarios.

**Mitigations**

Mitigation
Description




Environment configuration validation
Strictly validate all environment variables, configuration files, and dependency libraries, using hash verification to ensure their integrity and prevent unauthorized modification.


Dependency management
Use trusted dependency sources (such as the official PyPI mirror), and regularly check the versions and signatures of dependency packages to prevent supply chain attacks.


Environment isolation
Completely isolate development, testing, and production environments, restrict external input's access to the core environment, and reduce the attack surface.


Security monitoring and auditing
Implement real-time monitoring, log environment configuration and dependency change logs, and conduct regular security audits to detect potential injection behavior.


Principle of least privilege
Implement least-privilege control over API access and file operations in the environment, and use cryptographic signatures to verify the source of configurations and prevent malicious tampering.

**References**

https://mp.weixin.qq.com/s/9JwADiu9t3kqcfqnRMC2zQ
https://finance.sina.com.cn/tech/digi/2025-06-01/doc-ineypqvh0855918.shtml
https://zhuanlan.zhihu.com/p/1900540531131523166

---
### Unexpected Code Execution

> Risk ID: GAARM.0060
> Lifecycle: Application phase

**Attack Overview**

Unexpected code execution refers to an agent, during task execution, performing code operations beyond the expected scope or that are unauthorized, due to causes such as prompt injection, tool misuse, or logic flaws. The core of this risk is that the agent lacks effective control over code-execution boundaries and may, through dynamic code generation, toolchain invocation, script execution, and similar means, execute malicious, dangerous, or unintended code, leading to serious consequences such as system compromise, data tampering, sensitive information leakage, or service disruption.

**Attack Cases**

Case
Description




Case 1
The vulnerability originated from the form node not validating the Content-Type during processing, allowing an attacker to specify an arbitrary local sensitive file path, ultimately forging an administrator identity through information disclosure and executing malicious workflow commands.


Case 2
This case demonstrates an AI red team using prompt injection to induce a multimodal model with desktop-operation capabilities to download and execute a malicious program, ultimately establishing a C2 communication channel and achieving unexpected code execution and remote control, turning the host system into a "zombie host."


Case 3
This case demonstrates manipulating ChatGPT's long-term memory (Memory) mechanism via prompt injection to plant covert instruction logic defined by the attacker, causing the model to continuously communicate with a remote C2 and execute instructions in subsequent conversations, forming model-level "zombification control" and unexpected behavior execution.

**Attack Risks**

System compromise: malicious code execution leads to full control of the system.
Data destruction: executing destructive operations leads to data loss or tampering.
Privilege escalation: obtaining higher system privileges through code execution.
Backdoor planting: planting a persistent backdoor in the system.
Service disruption: executing malicious code makes the service unavailable.
Lateral movement: using code execution to attack other systems.

**Mitigations**

Mitigation
Description




Code execution sandbox
Restrict code execution to a securely isolated environment, use container or virtual-machine isolation, and limit access to the file system, network, and system calls.


Code review and validation
Implement static code security analysis, build a code security rule base, and dynamically detect malicious code patterns.


Permission control
Implement the principle of least privilege, restrict the permission scope of code-execution tools, and establish a code-execution approval mechanism.


Input validation and filtering
Strictly validate code-generation input, filter dangerous functions and operations, and detect potential malicious intent.

**References**

n8n remote code execution vulnerability
ZombAIs: From Prompt Injection to C2 with Claude Computer Use
AI Domination: Remote Controlling ChatGPT ZombAI Instances

---
