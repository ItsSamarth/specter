# AI Baseline Security - Application Phase

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-baseline-security.md
> Phase: Application phase (container escape/denial of service/code execution escape)

## Application Phase

### LLMs Denial of Service & Resource Exhaustion

> Risk number: GAARM.0008
> Lifecycle: Application phase

**Attack Overview**

Attackers may attack machine learning systems by sending large volumes of requests to slow down ML services or cause service shutdown. Because LLM systems require substantial dedicated computing resources, attackers can deliberately craft inputs that require excessive useless computation to consume LLM system resources, degrading service quality for LLMs and other users, potentially incurring high resource costs. Due to the resource-intensive nature of LLMs and the unpredictability of user inputs, the impact of this vulnerability can be greatly amplified.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Conducting Prompt injection in an Agent to trick it into repeatedly calling LLM and SerpAPI, rapidly increasing costs |
| Case 2 | Due to accidental leakage of a Sourcegraph site administrator access token, which was exploited to impersonate users and gain access to the system administration console, resulting in significantly increased API usage and leakage of large amounts of user data |
| Case 3 | Using Prompt injection to cause MathGPT to leak an API key, resulting in denial of service |
| Case 4 | Applying LLMs to decision-making in power systems; if a DoS attack occurs, it may cause delays and errors in decision-making, ultimately affecting the stable operation of the power system |

**Attack Risks**

Resource exhaustion attacks: Attackers may send large volumes of requests to monopolize the model's computing resources, making the service unavailable, impacting user experience, and potentially causing service interruption.
Data leakage and abuse: The attack process may cause the model to abnormally leak API tokens and other sensitive information, and attackers may conduct unauthorized access.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| API rate limiting | Enforce API rate limits, restricting the number of requests that individual users or IP addresses can make within a specific time period |
| Limit execution count | Limit the number of queued operations and the total number of operations in systems that respond to LLM |
| Real-time monitoring and alerting | Continuously monitor hardware resource utilization to identify abnormal spikes or patterns that may indicate denial-of-service attacks |

**References**

https://atlas.mitre.org/techniques/AML.T0029
https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-2023-v05.pdf
https://www.cnblogs.com/LittleHann/p/17596696.html

---
### Code Parser Execution Escape

> Risk number: GAARM.0007.001
> Lifecycle: Application phase

**Attack Overview**

This risk refers to attackers exploiting the functionality of code parsers such as GPT-4, using their code parsing and code generation capabilities, through multiple conversational context interactions to progressively construct and conceal malicious code, using Unicode characters and encoding obfuscation and other methods to hide malicious code, thereby bypassing code security checks in model applications, completing sandbox escape, and gaining access to the system. Such malicious code is highly concealed and difficult to detect; once sandbox isolation is breached, attackers can control the entire system, steal data, plant backdoors, etc.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | During GPT-4 code execution, malicious code was hidden and bypassed through multiple conversational context interactions and encoding methods, ultimately triggered via string execution, bypassing GPT-4's security checks, executing the `cat /etc/issue` command, and successfully obtaining the Linux distribution of the target environment |

**Attack Risks**

Data leakage risk: Attackers can extract sensitive data from LLM applications or their connected systems.
System integrity risk: Attackers can perform unauthorized operations, modify system settings or files, and even plant malicious code, causing damage to the system.
Privilege escalation risk: Once attackers successfully escape the sandbox, they may gain higher-privilege access than they originally had.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Rigorous testing of isolated environments | Conduct rigorous testing and validation of sandbox environments to ensure their security |
| Input/output validation | Filter out unsafe Prompts to maximize system security |
| Access control | Implement strict access control and privilege separation in LLM applications and their sandbox environments, ensuring only authorized entities can access sensitive resources, and restricting the execution of privileged operations |

**References**

https://blog.securelayer7.net/owasp-top10-for-large-language-models/
https://www.mufeedvh.com/llm-security/#2-sandboxing-extended-llms
https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_Sandboxing.html

---
### Container Runtime Risk

> Risk number: GAARM.0004 (inferred from AISS classification)
> Lifecycle: Deployment phase

**Attack Overview**

LLM applications developed based on integrated frameworks typically combine K8s clusters and container environments to set up and isolate the running environments for various Agents. Attackers craft specific prompts to indirectly execute attacks against the container runtime environment through the model's Agent, achieving container escape and container privilege escalation in containerized environments.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Wiz obtained container runtime environment permissions for a model by uploading a malicious model to Hugging Face |

**Attack Risks**

Breaking container isolation: Attackers exploit container vulnerabilities or configuration flaws, attempting to breach the container's isolated environment and gain access to the host machine.
Image content tampering: Attackers may tamper with model image content, planting malicious code.
Data leakage: Attackers may obtain sensitive data, such as file system information on the host machine.
Service interruption: Attackers may disrupt services on the host machine, causing service unavailability.
Lateral movement: Attackers may use the escaped container as a pivot to further attack other systems in the internal network.
Persistent control: Attackers may install backdoors on the host machine to achieve long-term control.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Regular audits | Regularly scan container images and dependency components to ensure there are no security vulnerabilities |
| Resource limits and access isolation | Implement resource limits and isolation policies to prevent individual containers from consuming excessive resources and affecting other machines in the cluster |
| Principle of least privilege | Avoid running privileged containers with --privileged mode; only grant containers the minimum required set of permissions |
| Input/output validation | Ensure the security of prompts and results on the model input and output sides, and intercept suspicious attack behaviors |

**References**

https://mp.weixin.qq.com/s/tf4ljSJ0Ue0YniojWhYMKg
https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure

---
### Container Cluster Environment Reconnaissance

> Risk number: GAARM.0006
> Lifecycle: Application phase

**Attack Overview**

This risk refers to attackers exploiting security issues in third-party cloud providers or self-built K8s clusters used in model deployment environments, such as system permission control issues, misconfigurations, security vulnerabilities in the cluster itself, or third-party integration plugins. Attacks target features such as Agents in LLM integrated applications, using these features' interactions with business deployment environments to conduct attacks on model business application systems. Successful penetration into the deployment environment can lead to sensitive data leakage, backdoor program implantation, and other risks.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Wiz obtained model runtime environment permissions by uploading a malicious model to Hugging Face, then further exploited EKS cluster misconfigurations to achieve privilege escalation |

**Attack Risks**

Resource exhaustion attacks: Unrestricted access to resources may become an attack vector, with attackers consuming large amounts of resources and affecting the normal operation of the system.
Privileged mode operation risk: Containers running in privileged mode may increase the risk of system compromise.
Unauthorized cluster access: If security measures are not implemented or the cluster has incorrect configurations, attackers may gain complete access to the entire cluster.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Regular audits | Regularly scan container images and dependency components to ensure there are no security vulnerabilities |
| Resource limits and access isolation | Implement resource limits and isolation policies to prevent individual containers from consuming excessive resources; restrict access to resources through secrets and specific permission roles created in Kubernetes |
| Control network traffic | Use Kubernetes network policies to control inbound and outbound network traffic between Pods, reducing potential lateral movement within the cluster |

**References**

https://pradiptabanerjee.medium.com/confidential-containers-for-large-language-models-42477436345a


https://www.run.ai/guides/kubernetes-architecture/securing-your-ai-ml-kubernetes-environment

---
### Container Cluster Environment Attack

> Risk number: GAARM.0007
> Lifecycle: Application phase

**Attack Overview**

LLM applications developed based on integrated frameworks typically integrate various functional Agents, which are deployed in container environments within Kubernetes clusters. Attackers can craft specific prompts to indirectly induce LLM Agents to execute commands that probe the container, thereby achieving reconnaissance and collection of cluster environment information as a preliminary step for subsequent attacks. After completing reconnaissance and collecting the relevant information, attackers can specifically identify and exploit vulnerabilities and configuration issues in the cluster to further infiltrate and attack the entire container cluster.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | During GPT-4 code execution, malicious code was hidden and bypassed through multiple conversational context interactions and encoding methods, ultimately triggered via string execution, bypassing GPT-4's security checks, executing the `cat /etc/issue` command, and successfully obtaining information such as the Linux distribution of the target environment and cluster environment variables |

**Attack Risks**

Cluster environment information leakage: By crafting specific prompts, attackers may induce AI models to execute unauthorized commands, thereby leaking container internal architecture or security configuration information.
Cluster security configuration leakage: Attackers can obtain cluster security configuration details through reconnaissance, which may reduce the cluster's security level and increase the risk of compromise.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Implement strict access control | Ensure all services and ports are strictly reviewed, only authorizing necessary access to reduce the potential attack surface |
| Input/output validation | Ensure the security of prompts and results on the model input and output sides, and intercept suspicious attack behaviors |

**References**

https://mp.weixin.qq.com/s/Ry1PoZLfPvw6Lj8bz14mgw

---
