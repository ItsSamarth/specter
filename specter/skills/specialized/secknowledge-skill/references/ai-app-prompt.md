# AI Application Security - Application Phase - Prompt Injection and Variants

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-app-app.md
> Risk category: Prompt Injection (GAARM.0039 Direct / 0040.x Indirect/XSS/Memory/Worm / 0043.x Keyword & Synonym Obfuscation / 0044 Adversarial Encoding / 0045 Reverse Induction / 0061 Multimodal Injection)

---

### Prompt Injection

> Risk number: GAARM.0039
> Lifecycle: Application phase

**Attack Overview**

Prompt injection is the process where attackers use specially crafted inputs to override or manipulate the original instructions of LLMs. Because natural language is inherently ambiguous, the boundary between instructions and data is often unclear, allowing attackers to use malicious external input to contaminate model output. This attack typically occurs when untrusted input is used as part of a prompt. LLMs can recognize and process natural language, and natural language is inherently ambiguous — instructions and data often have no clear boundary — so attackers can include instructions in data fields they control, while the underlying system cannot distinguish between data and instructions.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Using malicious input to manipulate a GPT-3 prompt, commanding the model to ignore its previous instructions |
| Case 2 | Using multiple methods to conduct Prompt injection attacks |

**Attack Risks**

Successful Prompt injection may cause meta-prompt leakage, model jailbreaking, model function abuse, and other harms.

Malicious content generation: Attackers can use Prompt injection to generate inappropriate content, including threats, defamation, or other malicious information.
Data leakage: If LLMs are used to output sensitive information, Prompt injection attacks may cause data leakage.
System security: In some cases, Prompt injection can be used to generate and execute malicious code.
Model abuse: Through goal hijacking and other attack methods, attackers make LLMs deviate from their pre-configured system settings and execute other custom instructions, increasing the risk of model abuse.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Prompt content reinforcement | Use solutions similar to OpenAI Chat Markup Language (ChatML) to reinforce Prompt structure and content, attempting to isolate genuine user prompts from other content |
| Model security alignment | Provide diverse training data covering various attack scenarios; add safety fencing mechanisms during the model training phase to enhance the model's generalization and robustness |
| Input/output validation | Deploy external security guards on both the model input and output sides, using rules, classification algorithms, security models, etc., to inspect and filter input and output content |
| Monitoring and logging | Monitor and log LLM interaction records for subsequent detection and analysis of potential Prompt injection attacks |

**References**

https://aclanthology.org/2024.scalellm-1.2/
https://atlas.mitre.org/techniques/AML.T0051
https://josephthacker.com/ai/2023/05/19/prompt-injection-poc.html
https://simonwillison.net/2022/Sep/12/prompt-injection/

---
### XSS Session Content Hijacking

> Risk number: GAARM.0040.001
> Lifecycle: Application phase

**Attack Overview**

XSS session content hijacking is an indirect prompt injection attack technique that exploits the process by which LLMs obtain external information. When users interact with an LLM through a UI (web interface, API, application, etc.), attackers use indirect injection of malicious prompt instructions and exploit LLM application frontend parsing of Markdown and HTML img tags to summarize the current chat session content and embed sensitive keys and data in the src attribute of img tags, thereby leaking session content.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attacker exploits Google Bard's update feature to construct a special Markdown image tag, causing Bard to render an image pointing to the attacker's server, achieving data theft |
| Case 2 | Azure AI Playground model allows Markdown image injection to append prompts to the URL's src attribute for rendering, causing data leakage and other risks |
| Case 3 | Attacker exploits ChatGPT plugin's direct access to YouTube subtitles via indirect Prompt injection to control subtitle content and manipulate AI behavior |
| Case 4 | Attacker exploits ChatGPT's Markdown image rendering to steal chat history; attacker controls AI behavior, requests a summary of chat history appended to a URL to steal data |
| Case 5 | Attacker automatically steals data from chat sessions via Markdown image injection |
| Case 6 | Attacker can instruct ChatGPT to use a plugin to log the conversation, generate a URL pointing to the log, and leak the link via Markdown image injection to access the entire conversation history |
| Case 7 | Since LLM agents (client applications such as Bing Chat or ChatGPT) are vulnerable to Prompt injection, attackers can exploit this to automatically exfiltrate sensitive data by appending it to image URLs |

**Attack Risks**

Data leakage: Attackers can obtain sensitive data from the current session, including session tokens, personal information, chat history, etc.
Session hijacking: Attackers may take over user sessions using stolen session tokens.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Input/output validation | Strictly validate and sanitize all input and output data to remove or correct any suspicious injections and generated content |
| Content Security Policy (CSP) | Implement strict CSP content security policies to block execution of malicious scripts and data exfiltration |
| Principle of least privilege | Ensure proper sandboxing and limit LLM capabilities, restricting plugins, Agent mechanisms, etc. from obtaining data from untrusted sources |
| Human intervention and approval | Give users more control to manage plugin usage and data flows |

**References**

https://systemweakness.com/new-prompt-injection-attack-on-chatgpt-web-version-ef717492c5c2

---
### Indirect Prompt Injection

> Risk number: GAARM.0040
> Lifecycle: Application phase

**Attack Overview**

When LLMs process natural language, there is a vulnerability to malicious Prompt injection. Attackers hide Prompts in various types of data that the LLM system will process, such as text, multimedia content, databases, or information extracted from websites, then use Prompts to manipulate the LLM to produce harmful responses, such as malicious code execution or sensitive information leakage. For example, writing malicious code into a file uploaded to the LLM; when the LLM processes the file data, it runs the malicious code, causing harm.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attacker plants injection code on a website the user visits, causing Bing Chat to search for and exfiltrate personal information without the user's knowledge |
| Case 2 | Attacker controls data retrieved by LLM plugins, using Markdown image rendering to send chat history as query parameters to the attacker's server |
| Case 3 | Demonstrates an attack on M365 Copilot: by sending a malicious email — even without the user opening it — remotely control Copilot, causing an attack from a third party |

**Attack Risks**

Malicious code execution: Through injected malicious code or data, attackers may try to establish a foothold in the system to further control or damage it.
Data leakage: Attackers may use indirect injection to mislead users into performing unintended operations or leaking sensitive information.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Input validation | Strictly validate and sanitize all input data to remove or correct any suspicious injection content |
| Principle of least privilege | Ensure proper sandboxing and limit LLM capabilities, restricting plugins, Agent mechanisms, etc. from obtaining data from untrusted sources |
| Human intervention and approval | Give users more control to manage plugin usage and data flows |

**References**

https://atlas.mitre.org/techniques/AML.T0051.001
https://twitter.com/random_walker/status/1636923058370891778
https://medium.com/@harry.hphu/introduction-to-web-llm-attacks-indirect-prompt-injection-7bb9f154bc07
https://medium.com/@dinob5551/indirect-prompt-injection-the-hidden-threat-lurking-in-ai-730b009dd5fb

---
### Application Conversation Memory Attack

> Risk number: GAARM.0040.003
> Lifecycle: Application phase

**Attack Overview**

This risk refers to attackers using web-based Prompt injection to trick LLMs into creating malicious Memory entries (such as erroneous user preference settings with the model), thereby manipulating LLMs by maliciously modifying user preferences stored in LLM memory. For example, an attacker can trick the LLM into believing that the user's chat preference is "respond to every message from the user with 'Sorry, I cannot respond to you'", thereby achieving a DoS attack effect.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | This article describes how an application conversation Memory attack causes the model to continuously deny service to the user |

**Attack Risks**

DoS attack: Attackers can cause users to receive persistent denial-of-service memory attacks based on their preferences.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Disable history memory | Disabling the Memory feature of the LLM model can mitigate this issue |

**References**

https://embracethered.com/blog/posts/2024/chatgpt-persistent-denial-of-service/
https://openai.com/index/memory-and-new-controls-for-chatgpt/

---
### Loop Agent Worm

> Risk number: GAARM.0040.002
> Lifecycle: Application phase

**Attack Overview**

Agents have the ability to retrieve information in real time from external sources such as the internet, and can pass that information to a large model for processing before returning it to the user. However, attackers can exploit this by injecting malicious information through external data sources, interfering with Agent execution, thereby affecting LLM output. These malicious prompts indirectly affect multiple LLM applications, forming a vicious cycle that causes malicious information to spread rapidly. Through the Agent's input-output loop, this loop Agent worm creates a self-replicating and self-propagating malicious behavior, ultimately potentially causing privacy leakage and data abuse security risks.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Researchers created an AI worm called Morris II, capable of attacking a generative AI email assistant, stealing data from emails and sending spam, while bypassing some security protections in ChatGPT and Gemini |

**Attack Risks**

Data leakage: AI worms may steal sensitive personal information such as names, phone numbers, credit card numbers, ID numbers, etc.
Malware deployment: Worms can deploy malware on infected systems, causing further security issues.
Security protection bypass: AI worms can bypass some existing security protections, such as ChatGPT and Gemini's security mechanisms.
New cyber attacks: AI worms represent a type of cyber attack not previously widely recognized, posing a challenge to existing security protections.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Input/output validation | Apply strict validation and verification to data entering the Agent for dispatch and processing |
| Design secure LLM Agents | Apply traditional security measures such as ensuring secure application design, monitoring potential security vulnerabilities |
| Human intervention and approval | Keep humans in the loop to ensure LLM Agents need human approval before performing actions, preventing AI systems from autonomously sending emails or performing other potentially risky behaviors |

**References**

https://mp.weixin.qq.com/s/2bm7nuXkORLZ20mfpOmwrA

---
### Reverse Induction & Suppression Attack

> Risk number: GAARM.0045
> Lifecycle: Application phase

**Attack Overview**

This risk involves adding specific instructions to prompts that cause LLMs to avoid using certain specific refusal responses when generating answers, increasing the likelihood of unsafe or inappropriate content the attacker desires. This attack exploits the autoregressive nature of models to induce model behavior: since content generation is based on predicting the next word from previous output, by specifically requesting that LLMs avoid using certain words or phrases — such as "sorry", "cannot", "unable" — in their responses, the model is caused to generate inappropriate content or content violating safety policies.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Using prefix injection + reverse suppression attacks to bypass ChatGPT 3.5's security restrictions, causing output of illegal/criminal risk content |

**Attack Risks**

Generating inappropriate content: LLMs may generate content containing illegal guidance, violence, pornography, or politically sensitive risk content.
Bypassing safety mechanisms: Attackers can bypass LLM safety mechanisms, causing the model to output the risky content the attacker desires.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Model robustness enhancement | Through training and reinforcement learning, improve the LLM's ability to recognize and resist this type of attack |
| Input monitoring and filtering | Monitor LLM output in real time, promptly filtering out unsafe or inappropriate content |

---
### Multimodal Collaborative Injection Attack

> Risk number: GAARM.0061
> Lifecycle: Application phase

**Attack Overview**

A multimodal collaborative injection attack is an advanced attack technique that exploits the collaborative relationship between multiple modalities (text, image, audio, video, etc.) to embed malicious instructions. Attackers carefully construct cross-modal malicious content, exploiting the semantic association mechanisms that multimodal models use when processing and understanding different modal information, embedding malicious instructions into seemingly harmless multimodal content. The core of this attack is to bypass single-modality security detection mechanisms and achieve attack objectives through inter-modal synergistic effects, potentially causing data leakage, model behavior manipulation, or unintended operations.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attacker uses Cross-Modal Conflict Injection (CMCI) to insert special adversarial image-text pairs into a knowledge base through normal system update mechanisms. These pairs appear semantically aligned when retrieved (e.g., an image shows pneumonia, but the text describes "clear lungs"), but the content is actually contradictory, inducing the AI to output completely wrong diagnostic conclusions (e.g., misclassifying pneumonia as normal), causing serious medical safety risks |

**Attack Risks**

Data leakage: Inducing the model to leak training data or sensitive information.
Behavioral manipulation: Manipulating model output and behavior through cross-modal instructions.
Security bypass: Bypassing single-modality security detection and control mechanisms.
Privilege escalation: Obtaining higher system privileges through modal collaboration.
Privacy violation: Obtaining user privacy information through multimodal analysis.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Cross-modal collaborative detection | Establish multimodal collaborative security detection mechanisms, implement cross-modal semantic association analysis, detect anomalous modal combination patterns |
| Multi-dimensional security validation | Simultaneously validate security of multiple modalities, establish inter-modal consistency checks, implement cross-modal threat intelligence sharing |
| Fusion process hardening | Add security checks to the multimodal fusion process, implement dynamic modal weight adjustment, establish anomalous fusion pattern detection |
| Modal isolation processing | Pre-process different modalities in isolation, implement modal-level security filtering, establish secure inter-modal communication mechanisms |

**References**

Manipulating Multimodal Agents via Cross-Modal Prompt Injection
How to Make Medical AI Systems Safer? Vulnerabilities and Threats in Multimodal Medical RAG Systems

---
### Adversarial Encoding Attack

> Risk number: GAARM.0044
> Lifecycle: Application phase

**Attack Overview**

Adversarial encoding attacks are a countermeasure technique targeting LLM input and output defense detection mechanisms. Attackers use encoding or data transformation (such as base64 encoding) to try to bypass security checks or inject malicious content. This attack targets the encoding layer of NLP models, attempting to bypass the model's text understanding capability and directly affect internal feature generation.
Since LLMs are trained on diverse data types including encoded text, they support normal decoding operations, completing execution of malicious instructions or exfiltration of sensitive data.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Using adversarial encoding attacks to bypass ChatGPT security restrictions and obtain stored key information |
| Case 2 | Research on text-based NLP models being manipulated by encoding perturbations that interfere and mislead; these perturbations exploit language encoding capabilities to change model output and increase inference runtime — e.g., distinct characters appearing as the same or visually similar glyphs are used to perturb model input |

**Attack Risks**

Bypassing security mechanisms: Attackers may exploit model encoding/decoding capabilities to bypass content security checks.
Data leakage: Attackers can use Base64 encoding to hide malicious instructions or data, causing sensitive information leakage.
Unauthorized code execution: Malicious code can be injected into LLMs in Base64-encoded form, causing unauthorized code execution and potentially compromising system integrity and security.
Malicious operations: Attackers can use Base64 encoding to manipulate LLMs to perform various malicious operations, such as data tampering and session hijacking, endangering system and user security.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Input/output validation | Validate input and output data to prevent malicious or unintended Base64-encoded data from entering LLMs or being directly printed |
| Model security alignment | Train the model on language nuances and encoding techniques to recognize characteristics of these attacks |

**References**

https://promptengineering.org/mind-over-malware-battling-the-growing-arsenal-of-attacks-on-large-language-models/
https://www.toolify.ai/ai-news/the-future-of-hacking-5-terrifying-llm-security-threats-544868

---
### Keyword Obfuscation

> Risk number: GAARM.0043
> Lifecycle: Application phase

**Attack Overview**

This risk involves applying special processing operations to keywords in Prompts (homophones, synonyms, word splitting, or other text manipulation forms), maintaining similar meaning while ensuring that after tokenization the content no longer carries risky meaning, thereby circumventing model safety mechanisms' restrictions on sensitive words.

**Attack Cases**

Common keyword obfuscation methods in English LLMs include: letter obfuscation (bomb -> b0mb), synonym substitution (bomb -> explosive), word splitting (bomb -> b-o-m-b).
For Chinese LLMs, due to differences in tokenization methods, keyword obfuscation methods also differ significantly. Common Chinese keyword obfuscation methods include: pinyin substitution (bomb -> b0mb in Chinese characters), synonym substitution (bomb -> explosive), similar-character substitution (bomb -> visually similar alternative), etc.

**Attack Risks**

Generating inappropriate content: Attackers may exploit keyword obfuscation to bypass automated content review systems, publishing or spreading malicious content such as violence, terrorism, or pornography.
Bypassing safety mechanisms: Attackers maliciously guide the model to produce incorrect output, misleading systems into making poor decisions or performing dangerous operations.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Model security alignment | Through training and reinforcement learning, improve LLM's ability to recognize and resist this type of attack |
| Input/output validation | On the input side, continuously update and improve vocabulary filtering systems to identify and block obfuscated sensitive words; on the output side, monitor LLM-generated content and use content security analysis techniques to identify potential issues |

**References**

https://mp.weixin.qq.com/s/eFDQWYYCOe_SSiourhTxig

---
### Synonym Substitution Attack

> Risk number: GAARM.0043.001
> Lifecycle: Application phase

**Attack Overview**

A synonym substitution attack bypasses model safety protections by using synonyms with the same or similar meaning as sensitive words or phrases, thereby obtaining or leaking the model's internal instructions or sensitive information. As LLMs grow increasingly large, fine-tuning on each adversarial example becomes more difficult, making models more susceptible to synonym substitution attacks. For example, in a programming assistant, an attacker might substitute "delete" with "remove", "destroy" with "harm", etc., to try to bypass keyword checks.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attacker successfully bypasses the model's filters using synonym substitution, achieving leakage of system Prompt settings |

**Attack Risks**

Sensitive information leakage: Attackers may obtain the model's internal instructions, including but not limited to system prompts, passwords, and other sensitive information.
Safety mechanism bypass: Attackers can use synonym substitution to bypass the model's safety protections, causing the model to produce undesired output or perform unauthorized operations.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Model security alignment | Provide diverse training data covering various attack scenarios to enhance the model's generalization and robustness |
| Input/output validation | On the input side, continuously update and improve vocabulary filtering systems to identify and block obfuscated sensitive words; on the output side, monitor LLM-generated content and use content security analysis techniques to identify potential issues |

**References**

https://arxiv.org/html/2402.16914v1

---
