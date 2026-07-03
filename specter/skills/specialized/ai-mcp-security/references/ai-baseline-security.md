# AI Foundation Security

> Source: AISS NSFOCUS Large Model Security Intelligence Chain Community
> Entry Count: 19

---

## Application Phase

### LLMs Denial of Service & Resource Exhaustion

> Risk ID: GAARM.0008
> Lifecycle: Application Phase

**Attack Overview**

Attackers may attack machine learning systems by sending large volumes of requests to slow down ML services or cause service outages. Because LLM systems require substantial dedicated computing resources, attackers can deliberately craft inputs that require large amounts of wasteful computation to exhaust LLM system resources, degrading the quality of service for LLMs and other users, and potentially incurring high resource costs. Due to the resource-intensive nature of LLMs and the unpredictability of user inputs, the severity of this vulnerability can easily be amplified.

**Attack Cases**

Case
Description




Case 1
Perform Prompt injection into an agent, tricking it into repeatedly calling LLM and SerpAPI, rapidly increasing costs.


Case 2
Due to an accidental leak of a Sourcegraph site administrator access token, which was exploited to impersonate users and gain access to the system administration console, leading to a significant increase in API usage and the leak of large amounts of user data.


Case 3
Use Prompt injection to make MathGPT leak its API key, causing denial of service.


Case 4
When LLM is applied for decision-making in power systems, a DOS attack could cause delays and errors in decisions, ultimately affecting the stable operation of the power system.

**Attack Risks**

Resource Exhaustion Attack: Attackers may send large numbers of requests to occupy the model's computing resources, making the service unavailable, degrading user experience, and potentially causing service interruptions.
Data Leakage and Abuse: The attack process may cause the model to abnormally leak sensitive information such as API tokens, and attackers may conduct unauthorized access.

**Mitigation Measures**

Mitigation Method
Description




API Rate Limiting
Enforce API rate limits, restricting the number of requests that individual users or IP addresses can make within a specific time period


Limit Execution Count
Limit the number of queued operations and the total number of operations in the system responding to LLM


Real-time Monitoring and Alerting
Continuously monitor hardware resource utilization to identify abnormal spikes or patterns that may indicate a denial-of-service attack

**参考**

https://atlas.mitre.org/techniques/AML.T0029
https://owasp.org/www-project-top-10-for-large-language-model-applications/assets/PDF/OWASP-Top-10-for-LLMs-2023-v05.pdf
https://www.cnblogs.com/LittleHann/p/17596696.html

---
### Code Interpreter Execution Escape

> Risk ID: GAARM.0007.001
> Lifecycle: Application Phase

**Attack Overview**

This risk refers to attackers exploiting the functionality of code interpreters such as GPT-4, using their code parsing and code generation capabilities to progressively construct and conceal malicious code through multiple session context interactions, using Unicode characters and encoding obfuscation to hide malicious code. This allows the malicious code to bypass the model application's code security inspection mechanisms, complete sandbox escape, and gain access to the system. Such malicious code is highly stealthy and difficult to detect; once the sandbox isolation is breached, attackers can control the entire system, steal data, plant backdoors, and more.

**Attack Cases**

Case
Description




Case 1
During GPT-4 code execution, malicious code was hidden and bypassed through multiple session context interactions and encoding methods, ultimately triggered via a string, bypassing GPT-4's security checks and executing the `cat /etc/issue` command to successfully obtain the Linux distribution of the target environment.

**Attack Risks**

Data Leakage Risk: Attackers can extract sensitive data from LLM applications or their connected systems.
System Integrity Risk: Attackers can perform unauthorized operations, modify system settings or files, and even plant malicious code, thereby damaging the system.
Privilege Escalation Risk: Once an attacker successfully escapes the sandbox, they may gain access with higher privileges than they originally possessed.

**Mitigation Measures**

Mitigation Method
Description




Rigorous Sandbox Environment Testing
Conduct rigorous testing and validation of sandbox environments to ensure their security


Input/Output Validation
Filter out unsafe Prompts to maximize system security


Access Control
Implement strict access controls and privilege separation in LLM applications and their sandbox environments, ensuring only authorized entities can access sensitive resources and restricting the execution of privileged operations

**参考**

https://blog.securelayer7.net/owasp-top10-for-large-language-models/
https://www.mufeedvh.com/llm-security/#2-sandboxing-extended-llms
https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_Sandboxing.html

---
### Container Runtime Risks

> Risk ID: GAARM.0004 (inferred from AISS classification)
> Lifecycle: Deployment Phase

**Attack Overview**

LLM applications developed on integrated frameworks typically combine K8S clusters and container environments to build and isolate the runtime environments for various Agents. Attackers craft prompts to indirectly execute attacks against the container runtime environment through the model's Agents, achieving container escape and container privilege escalation within the container environment.

**Attack Cases**

Case
Description




Case 1
Wiz obtained model container runtime environment permissions by uploading a malicious model to Hugging Face.

**Attack Risks**

Breaking container isolation: Attackers attempt to breach the container's isolated environment by exploiting container vulnerabilities or configuration flaws to gain access to the host machine.
Image content tampering: Attackers may tamper with model image content and plant malicious code.
Data leakage: Attackers may obtain sensitive data, such as file system information on the host machine.
Service disruption: Attackers may disrupt services on the host machine, causing service unavailability.
Lateral movement: Attackers may use escaped containers as a pivot point to further attack other systems in the internal network.
Persistent control: Attackers may install backdoors on the host machine to achieve long-term control.

**Mitigation Measures**

Mitigation Method
Description




Regular Audits
Regularly scan container images and dependency components to ensure there are no security vulnerabilities.


Resource Limits and Access Isolation
Implement resource limits and isolation policies to prevent individual containers from consuming excessive resources and affecting other machines in the cluster.


Principle of Least Privilege
Avoid running privileged containers with --privileged mode; grant only the minimum set of permissions required by the container.


Input/Output Validation
Ensure the security of prompts and results on the model's input/output side, and intercept suspicious attack behaviors.

**参考**

https://mp.weixin.qq.com/s/tf4ljSJ0Ue0YniojWhYMKg
https://www.wiz.io/blog/wiz-and-hugging-face-address-risks-to-ai-infrastructure

---
### Container Cluster Environment Reconnaissance

> Risk ID: GAARM.0006
> Lifecycle: Application Phase

**Attack Overview**

This risk refers to attackers exploiting security issues in third-party cloud providers or self-built K8S clusters in model deployment environments, such as system permission controls, misconfigurations, cluster security vulnerabilities, and third-party integration plugins. Attackers target Agents and other functions in LLM integrated applications, leveraging the interaction of these functions with the business deployment environment to carry out attacks against the model's business application system. After successfully penetrating the deployment environment, risks such as sensitive data leakage and backdoor implantation may occur.

**Attack Cases**

Case
Description




Case 1
Wiz obtained model runtime environment permissions by uploading a malicious model to Hugging Face, then further exploited EKS cluster misconfigurations to achieve privilege escalation.

**Attack Risks**

Resource exhaustion attack: Unrestricted access to resources may become an attack vector; attackers may consume large amounts of resources, affecting normal system operation.
Privileged mode execution risk: Containers running in privileged mode may increase the risk of the system being compromised.
Unauthorized cluster access: If security measures are not implemented or the cluster has incorrect configurations, attackers may gain full access to the entire cluster.

**Mitigation Measures**

Mitigation Method
Description




Regular Audits
Regularly scan container images and dependency components to ensure there are no security vulnerabilities


Resource Limits and Access Isolation
Implement resource limits and isolation policies to prevent individual containers from consuming excessive resources; restrict access to resources through secrets and specific permission roles created in Kubernetes


Control Network Traffic
Use Kubernetes network policies to control inbound and outbound network traffic between Pods, reducing potential lateral movement within the cluster

**参考**

https://pradiptabanerjee.medium.com/confidential-containers-for-large-language-models-42477436345a


https://www.run.ai/guides/kubernetes-architecture/securing-your-ai-ml-kubernetes-environment

---
### Container Cluster Environment Attack

> Risk ID: GAARM.0007
> Lifecycle: Application Phase

**Attack Overview**

LLM applications developed on integrated frameworks typically integrate various functional Agents, which are deployed in container environments within Kubernetes clusters. Attackers can craft prompts to indirectly induce LLM Agents to execute commands that probe the container, thereby achieving reconnaissance and collection of cluster environment information as a prerequisite for subsequent attacks. After completing reconnaissance and collecting the relevant information, attackers can specifically search for and exploit vulnerabilities and configuration issues in the cluster to further penetrate and attack the entire container cluster.

**Attack Cases**

Case
Description




Case 1
During GPT-4 code execution, malicious code was hidden and bypassed through multiple session context interactions and encoding methods, ultimately triggered via a string, bypassing GPT-4's security checks, executing the `cat /etc/issue` command, and successfully obtaining the target environment's Linux distribution and cluster environment variable information.

**Attack Risks**

Cluster environment information leakage: By crafting specific prompts, attackers may induce the AI model to execute unauthorized commands, thereby leaking information about the container's internal architecture or security configuration.
Cluster security configuration leakage: Attackers can obtain cluster security configuration details through reconnaissance, which may reduce cluster security and increase the risk of being compromised.

**Mitigation Measures**

Mitigation Method
Description




Implement Strict Access Controls
Ensure all services and ports are rigorously reviewed, authorize only necessary access, and reduce the potential attack surface.


Input/Output Validation
Ensure the security of prompts and results on the model's input/output side, and intercept suspicious attack behaviors.

**参考**

https://mp.weixin.qq.com/s/Ry1PoZLfPvw6Lj8bz14mgw

---
## Deployment Phase

### CI/CD Pipeline Attack

> Risk ID: GAARM.0004
> Lifecycle: Deployment Phase

**Attack Overview**

Throughout the full lifecycle of large model development, the CI/CD pipeline is responsible for pushing models from the development environment to the production environment, automating the deployment of LLM large models, and handling subsequent updates and maintenance. A CI/CD pipeline attack refers to a scenario where, during the process of CI/CD pushing a model to the production environment, attackers exploit security vulnerabilities in the CI/CD infrastructure, unreliable third-party tools, etc., to attack the CI/CD pipeline — for example by submitting malicious code or poisoning dependency packages — leading to serious consequences such as illegal model tampering and sensitive information leakage.

  

LLM development lifecycle CI/CD pipeline

**Attack Cases**

Case
Description




Case 1
Obtain developer or operations personnel credentials through phishing, then submit malicious code into the CI/CD pipeline.


Case 2
Exploit server vulnerabilities, such as vulnerabilities in CI/CD infrastructure like GitLab and Jenkins.


Case 3
Attack third-party tools and application dependencies, such as poisoning dependency packages or uploading malicious packages with spoofed dependency names to open-source central repositories.

**Attack Risks**

Virtual environment contamination: Virtual environments or containers in the continuous integration environment are attacked; attackers may tamper with dependencies or runtime configurations in the environment to affect model training and deployment outcomes.
Build and deployment pipeline tampering: Attackers may attempt to modify automated build and deployment pipelines to insert malicious code or operations during the model deployment process.
Sensitive information leakage: CI/CD environments store sensitive information (such as access credentials, configuration files, keys, etc.); once obtained by attackers, this may lead to sensitive information leakage and privacy risks.
Denial-of-service attack: Attackers may attempt to render CI/CD systems inoperable through denial-of-service (DoS) attacks, causing interruptions or delays in the model development and deployment process.
Unauthorized model access: When the model deployment process is attacked, attackers may gain unauthorized access through vulnerabilities, enabling illegal operations or tampering with the model.

**Mitigation Measures**

Mitigation Method
Description




Strengthen Access Controls and Permission Management
Restrict access to CI/CD systems and related environments, ensuring only authorized personnel can access critical resources.


Security Updates and Audits
Regularly update and audit model deployment software to fix vulnerabilities and enhance security.


Strengthen Monitoring and Logging
Promptly detect anomalous activities and attack behaviors, and take timely response measures to reduce potential security risks and losses.

**参考**

https://github.com/knownsec/KCon/blob/master/2023/CICD%E6%94%BB%E5%87%BB%E5%9C%BA%E6%99%AF.pdf

---
### Cloud Platform Multi-Tenant Isolation Failure

> Risk ID: GAARM.0003.001
> Lifecycle: Deployment Phase

**Attack Overview**

In cloud platforms with multi-tenant architectures, each tenant should have an independent operating environment and data storage to ensure mutual isolation of user behavior and data. Isolation failures may be caused by design flaws, misconfigurations, etc. As high-value computing services become more prevalent, attackers may exploit this to breach tenant boundaries, access and tamper with other tenants' data, or even execute malicious operations, leading to a series of security issues where data and resources across different tenants (users or organizations) cannot be effectively protected.

**Attack Cases**

Case
Description




Case 1
This research investigated “whether AI models run in isolated environments.” Wiz exploited the AWS IMDS metadata service to complete Amazon EKS privilege escalation and take over the entire cluster service, performing lateral movement within the EKS cluster, enabling further cross-tenant access and sensitive data leakage.

**Attack Risks**

Data leakage: Multi-tenant isolation failures may cause data confusion or leakage between tenants, which may include sensitive information or personally identifiable information.
Reduced trust: Security incidents may undermine user trust in cloud service providers.

**Mitigation Measures**

Mitigation Method
Description




Strengthen Access Controls
Strengthen access control for system resources through permission management mechanisms such as Access Control Lists (ACLs) and Role-Based Access Control (RBAC).


Resource Monitoring
Monitor resource usage to promptly detect anomalous behaviors such as resource contention or abuse.

**参考**

https://xie.infoq.cn/article/536a3e7e776eb32b38d1a9747
https://www.helloaliyun.com/tutorial/1039.html
https://support.huaweicloud.com/usermanual-gaussdbformysql/gaussdbformysql_05_0347.html

---
### Cloud Platform Security Vulnerabilities

> Risk ID: GAARM.005
> Lifecycle: Deployment Phase

**Attack Overview**

Due to their high computing demands, large model applications typically rely on cloud platform environments to complete training and inference tasks, making cloud platform security critical to large model security. However, security risks arising from technical flaws, vulnerabilities, lack of multi-factor authentication, and other issues in cloud platforms allow attackers to exploit these security problems to maliciously attack large models deployed in the cloud — for example, reading sensitive data or illegally stealing and using account credentials — causing a series of losses to the platform including but not limited to data leakage, service interruption, and malicious code execution. These attacks not only affect the security of large models but may also threaten other users of the cloud service.

**Attack Cases**

Case
Description




Case 1
A CSRF vulnerability was discovered in the Amazon SageMaker Notebook service; attackers could exploit the vulnerability to read sensitive data and execute arbitrary operations in customer environments.


Case 2
Due to security vulnerabilities in Laravel versions (CVE-2021-3129), attackers used AWS credentials stolen from Laravel to illegally probe cloud-hosted model services accessible with those credentials; victims suffered losses of over $46,000 per day.

**Attack Risks**

Data leakage: Cloud application security vulnerabilities and insecure APIs may cause sensitive information to be accessed or exposed by unauthorized third parties, creating serious privacy and compliance issues.
Unauthorized access to model applications: Cloud platform security vulnerabilities may expose user-deployed model applications to the risk of unauthorized access.

**Mitigation Measures**

Mitigation Method
Description




Strict Access Controls
Ensure only authenticated and authorized users can access API endpoints.


Principle of Least Privilege
Implement the principle of least privilege, ensuring users and processes only have the minimum access permissions necessary to complete their tasks.

**参考**

https://developer.aliyun.com/article/1430094

---
### 利用不安全系统配置

> 风险编号: GAARM.0003
> 生命周期: 部署阶段

**攻击概述**

该风险是指模型部署所在的基础设施环境下，攻击者针对ML模型部署系统、部署集群环境、部署容器环境、镜像推送管理环境等存在一系列的不安全系统配置，实施针对模型基座环境的各种攻击行为。


未授权访问：配置不当可能导致敏感端口暴露或认证机制弱化，使得未授权用户能够访问系统资源；


容器安全风险：不安全的容器配置可能包括不必要的权限、敏感文件挂载、或容器逃逸漏洞；


集群安全风险：在Kubernetes等集群中，不当的RBAC配置可能导致权限提升或横向移动攻击；


镜像安全风险：不安全的系统配置导致镜像在传递、管理、部署等阶段出现泄露等风险；


环境隔离风险：配置错误可能导致隔离失效，使得攻击者能够访问或影响其他容器或宿主机；

**攻击案例**

案例
描述




案例一
ShadowRay：首个已知的针对在野外被积极利用的 AI 工作负载的攻击活动

**攻击风险**

恶意操作：如果系统配置不当，攻击者可能会利用这些漏洞获取对系统的访问权限，进而进行恶意操作。
数据泄露：攻击者可能获取敏感数据，如宿主机上的文件系统信息或集群内的secrets。
服务中断：攻击者可能破坏宿主机或集群服务，导致服务不可用。
横向移动：攻击者可能利用逃逸的容器或提权的节点作为跳板，进一步攻击内网中的其他系统。
持久性控制：攻击者可能在宿主机或集群中安装后门，实现长期控制。

**缓解措施**

缓解方式
描述




最小权限原则
确保容器和集群组件仅拥有完成其任务所必需的最小权限


确保安全的系统配置
避免使用特权容器，合理配置RBAC，限制APIServer的访问，避免不必要的风险暴露


定期更新与补丁管理
及时更新容器和集群组件，应用安全补丁，减少漏洞利用的风险

**参考**

https://pradiptabanerjee.medium.com/confidential-containers-for-large-language-models-42477436345a

---
### 向量数据库漏洞

> 风险编号: GAARM.0005 (子风险-1，父风险: 部署环境组件供应链漏洞)
> 生命周期: 部署阶段

**攻击概述**

RAG应用开发过程中，会将本地各类文档数据可以通过 Text 类划分为长度更短的段落，并利用 embedding 模型将文本内容进行向量化，最终存入向量数据库。向量数据库在RAG应用架构中扮演着重要角色，尤其是在处理高维数据和执行近似最近邻（ANN）查询时。由于向量数据库的重要性，如果它存在漏洞，攻击者可以利用其漏洞来获取未授权的数据访问、篡改数据、执行恶意代码或发起其他攻击，以此达到敏感信息获取、远程操控恶意代码等目的，带来数据方面的损失。

**攻击案例**

案例
描述




案例一
利用Qdrant向量数据库API实现路径穿越后的文件上传，导致出现远程代码执行风险


案例二
anything-llm存在CVE-2024-0551漏洞，未授权的攻击者可以通过漏洞下载数据库中的文件


案例三
本研究提出了针对 RAG 增强 LLMs 的新攻击方式，通过向其知识数据库中注入单个恶意文档来危害受害者的 RAG 系统，从而引发多种针对生成模型的恶意攻击。

**攻击风险**

数据篡改：攻击者利用向量数据库漏洞对嵌入向量进行篡改，导致数据库中的数据被篡改，进而影响数据的完整性。
用户隐私侵犯：向量数据库中可能存储个人身份等敏感信息，一旦被攻击者获取，将严重侵犯用户隐私。

**缓解措施**

缓解方式
描述




定期更新补丁
随时了解来自向量数据库提供商的最新补丁，定期更新数据库软件可确保针对已知漏洞的防护


数据备份
定期备份数据，确保在数据被篡改时可以快速恢复


监控和日志
实施实时监控和日志记录，以便及时发现和响应可疑活动

**参考**

https://ironcorelabs.com/security-risks-rag/

---
### 容器&&集群系统漏洞

> 风险编号: GAARM.0005 (子风险-2，父风险: 部署环境组件供应链漏洞)
> 生命周期: 部署阶段

**攻击概述**

大模型部署环境下的容器和集群系统漏洞风险主要涉及在大模型部署和运行环境中，容器技术及集群管理系统可能存在的安全问题。攻击者可以利用这些漏洞来执行恶意代码、窃取数据、干扰服务运行等，造成隐私信息泄露问题，从而对大模型的安全性和稳定性造成威胁。

**攻击案例**

案例
描述




案例一
OPENAI使用的Docker镜像版本存在CVE-2023-28432漏洞，利用该漏洞可获取密钥等信息

**攻击风险**

容器逃逸：攻击者可能通过容器内的漏洞实现容器逃逸，获取主机或其他容器的权限。
集群风险扩散：单个容器的漏洞可能导致整个集群的风险扩散。

**缓解措施**

。



缓解方式
描述




及时更新相关组件
定期更新Kubernetes及其相关组件（如Docker、containerd等）到最新版本，以修复已知的安全漏洞


严格的访问控制
实施严格的访问控制策略，限制容器之间和容器与集群外部的通信

**参考**

https://www.securityweek.com/chatgpt-data-breach-confirmed-as-security-firm-warns-of-vulnerable-component-exploitation/

---
### 模型部署服务漏洞

> 风险编号: GAARM.0004.001
> 生命周期: 部署阶段

**攻击概述**

ML模型部署服务漏洞可能存在于模型的接口、支持库，或者与模型交互的应用程序中，例如通过特定漏洞进行窃取模型参数、篡改模型预测结果、直接控制托管模型的服务等。通过漏洞，攻击者可以进行对系统的攻击，例如读取任意文件、植入后门从而获取对系统的控制等。由于ML模型部署服务通常支持将模型以容器的形式，推送部署到本地、云平台ML托管服务、云端K8S集群等多种目标环境下，因此一旦ML模型部署服务被攻击，将会导致下游多个环境的控制权限存在被窃取的风险。

**攻击案例**

案例
描述




案例一
MLFlow中存在文件读取漏洞，攻击者可以读取目标服务器上的任意文件


案例二
BentoML中存在反序列化代码执行漏洞，攻击者可以通过发送单个POST请求触发漏洞利用

**攻击风险**

供应链攻击：如果部署工具的供应链被攻击者渗透，他们可能会在工具中植入后门，从而获得对整个系统的控制。
数据泄露：MLOps软件涉及多个模型训练与部署的关键阶段，一旦被控制会导致训练数据、模型参数等敏感信息的泄露。
模型篡改：模型的参数或逻辑可能被攻击者修改，导致错误的预测结果。

**缓解措施**

缓解方式
描述




安全更新与审计
定期更新和审计模型部署软件以修复漏洞并增强安全性


访问控制
实施严格的访问控制措施，确保只有授权用户能够访问和修改部署的模型


监控和日志
实施实时监控和日志记录，以便及时发现和响应可疑活动

**参考**

http://www.bimant.com/blog/top8-ml-model-deployment-tools/
https://mlflow.org/docs/latest/deployment/index.html

---
### 模型镜像污染

> 风险编号: GAARM.0004.002
> 生命周期: 部署阶段

**攻击概述**

该风险是指模型在完成训练微调阶段后，模型镜像即将发布到生产环境进行部署（自建环境、公有云或者第三方基础设施），在此发布过程中缺乏充分的安全防护措施，（诸如对于模型镜像传输过程中的加密签名等），通过镜像污染，攻击者可以控制受感染系统的运行，存在镜像文件被劫持篡改等风险，导致影响模型的决策过程，出现安全隐患。

  

模型镜像推送部署

**攻击案例**

案例
描述




案例一
攻击者通过控制CI/CD系统的镜像部署过程，在镜像中植入后门代码或者窃取敏感数据

**攻击风险**

命令执行：通过镜像污染，攻击者可以控制受感染系统的运行，执行任意命令。
模型决策影响：恶意的模型镜像污染，可能导致影响模型的决策过程，出现安全隐患。

**缓解措施**

缓解方式
描述




镜像签名
使用镜像签名和验证机制，确保镜像内容的完整性


可信硬件使用
基于机密容器等可信运行环境，确保动态运行数据的机密性、完整性以及安全性


镜像扫描
在部署前对容器镜像进行安全扫描，以检测和修复已知漏洞

**参考**

https://www.docker.com/blog/llm-docker-for-local-and-hugging-face-hosting/
https://collabnix.com/large-language-models-llms-and-docker-building-the-next-generation-web-application/
https://mp.weixin.qq.com/s/vIDHBLbA5iWoPlYTKHSZfw

---
### 环境隔离缺陷

> 风险编号: GAARM.0003.001
> 生命周期: 部署阶段

**攻击概述**

该风险是指在容器部署阶段，LLMs业务应用的运行环境和物理环境存在沙箱环境隔离的配置或者设计缺陷，容器或虚拟机等沙箱环境中的应用程序，可能存在逃逸沙箱环境，访问或操控沙箱外部资源的安全漏洞。因此攻击者即便被限制在容器内部，也可以利用错误配置（特权容器、错误文件挂载等）来绕过隔离，访问到容器外部的资源和敏感系统，进而利用执行体实现未授权访问或者其他的LLMs意外操作，带来诸如执行未授权命令等意外风险。

  

执行体环境隔离架构

由于LLMs需要通过执行体实现与外部环境的交互，使用集群环境下的Pod快速启动执行体实现特定的交互操作是常见的执行体环境隔离架构，在此过程中针对网络、文件、进程以及Pod存活时间等多种环境未做好隔离，导致出现意外风险。

**攻击案例**

案例
描述




案例一
Hugging Face模型运行环境由于未做好外网访问限制，导致攻击者可以获取到生产环境的shell控制权限

**攻击风险**

容器逃逸：不完善的环境隔离可能导致容器逃逸问题，使得攻击者能够从容器中获取对主机系统的控制权，甚至访问其他容器中的数据。
敏感数据库访问：攻击者通过精心构造的提示（prompts），指示LLM提取并泄露敏感数据库中的机密信息。
系统级操作：如果LLM被允许执行系统级操作，攻击者可能会操纵它在底层系统上执行未授权的命令。

**缓解措施**

缓解方式
描述




严格的访问控制
实施基于角色的访问控制（RBAC）策略，确保只有经过授权的人员才能访问运行环境


网络隔离
使用网络策略限制容器间、集群间以及外部访问权限，减少潜在的攻击面和风险


实施沙箱技术
使用适当的沙箱技术来隔离LLM环境，防止其与关键系统和资源交互

**参考**

https://cloud.baidu.com/article/621826
https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_Sandboxing.html

---
### 部署环境组件供应链漏洞

> 风险编号: GAARM.0005 (父风险，含子风险: 向量数据库漏洞、容器&&集群系统漏洞)
> 生命周期: 部署阶段

**攻击概述**

部署环境供应链漏洞（Supply Chain Vulnerabilities in Deployment Environments）是指在软件供应链和部署过程中，从原材料（如库、依赖项、开发工具）到最终产品（如部署的软件）的环节存在的安全缺陷，可能导致系统被攻击或数据泄露的漏洞风险。供应链漏洞可以在软件部署时被利用，导致系统的安全性降低，数据泄露或服务中断。主要分为三类：


容器&&集群系统漏洞：容器技术及集群管理系统可能存在安全问题，攻击者可以利用这些漏洞来执行恶意代码、窃取数据、干扰服务运行等，造成隐私信息泄露问题，从而对大模型的安全性和稳定性造成威胁。


向量数据库漏洞：向量数据库如果存在漏洞，攻击者可以利用其漏洞来获取未授权的数据访问、篡改数据、执行恶意代码或发起其他攻击，以此达到敏感信息获取、远程操控恶意代码等目的，带来数据方面的损失。


云平台安全漏洞：如果云平台存在技术缺陷、技术漏洞、缺乏多重身份验证等原因导致的安全隐患，攻击者可以利用这些安全问题，对部署在云上的大模型进行恶意攻击，例如读取敏感数据、非法窃取并使用账号凭证等，给平台带来一系列损失，包括但不限于数据泄露、服务中断、恶意代码执行等。

**攻击案例**

具体见子风险

**攻击风险**

数据泄露：攻击者可能获取敏感数据，敏感信息被未授权的第三方访问或公开，会造成严重的隐私和合规性问题。
模型应用未授权访问：云平台安全漏洞可能导致用户部署的模型应用出现未授权访问的风险。
用户隐私侵犯：被存储的个人身份等敏感信息，一旦被攻击者获取，将严重侵犯用户隐私。

**缓解措施**

缓解方式
描述




最小权限原则
确保组件仅拥有完成其任务所必需的最小权限


定期更新与补丁管理
及时更新组件，应用安全补丁，减少漏洞利用的风险

---
## 训练阶段

### 模型开发工具漏洞

> 风险编号: GAARM.0001.001
> 生命周期: 训练阶段

**攻击概述**

模型开发训练涉及到数据预处理、特征工程、模型选择、训练、评估和部署等多个步骤。在这个过程中使用的工具如果存在安全漏洞，会导致整个机器学习流程面临风险。攻击者可以利用这些漏洞来篡改模型训练数据、窃取模型参数、或者在模型部署后执行特定的攻击，导致模型输出不准确、参数被窃取、传播恶意软件等严重安全后果。

**攻击案例**

案例
描述




案例一
Tensorflow存在代码执行漏洞，加载模型时存在代码执行风险


案例二
Pytorch存在代码执行漏洞，此漏洞能够在运行程序的用户上下文中在目标系统上执行远程代码，存在执行恶意代码的风险


案例三
本文档涵盖了 TensorFlow 的不同用例，概述了 TensorFlow 存在的安全漏洞的问题，其中不同的用例会带来不同的风险后果

**攻击风险**

供应链攻击：攻击者可通过植入恶意代码至ML开发用的合法软件包，实施依赖链攻击，从而在分发过程中传播恶意软件。
模型投毒：攻击者向训练数据中注入恶意数据，影响模型的决策过程，导致模型输出不准确或产生偏见。
知识产权损失：如果模型参数被窃取，攻击者可能复制或非法使用该模型。

**缓解措施**

缓解方式
描述




定期更新和打补丁
保持所有开发工具和库的最新版本，以利用最新的安全修复


安全的依赖链
审查依赖链，确保所有第三方库和包都来自可信的源

**参考**

https://www.secrss.com/articles/64006
https://huntr.com/bounties/a795bf93-c91e-4c79-aae8-f7d8bda92e2a

---
### 训练数据管理系统漏洞

> 风险编号: GAARM.0001.002
> 生命周期: 训练阶段

**攻击概述**

训练数据管理系统负责存储、处理、标注和提供数据，将准备好的数据交付给模型进行学习。当该系统存在供应链相关的安全漏洞，攻击者可以利用这些漏洞来篡改数据、窃取数据，甚至通过数据投毒影响模型的训练结果。

**攻击风险**

数据投毒攻击：攻击者可能会向训练数据中注入恶意数据，影响模型的决策过程，导致模型预测不准确或产生偏见。
模型窃取攻击：攻击者尝试通过询问模型来逆向工程并获得模型的参数或训练数据，从而窃取知识产权。
数据泄露：攻击者通过未授权访问获取敏感的训练数据。

**缓解措施**

缓解方式
描述




安全更新与审计
定期更新和审计训练数据管理系统以修复漏洞并增强安全性


监控和日志
实施实时监控和日志记录，以便及时发现和响应可疑活动

**参考**

https://doc.dataiku.com/dss/latest/concepts/homepage/index.html
https://www.secrss.com/articles/62742

---
### 训练环境安全风险

> 风险编号: GAARM.0001
> 生命周期: 训练阶段

**攻击概述**

该风险是指模型的训练与开发环境中使用的深度学习框架（如TensorFlow或PyTorch）和必要的依赖库等应用开发组件，如果引用的这些框架自身存在安全漏洞，对下游的LLMs应用造成供应链攻击，从而影响训练数据、ML模型和部署平台的完整性。

**攻击案例**

案例
描述




案例一
OpenAI提供的集成插件示例代码中包含了一个存在漏洞的MinIO docker镜像，该漏洞可能导致密钥和密码泄露；ChatGPT使用的Redis-py库存在漏洞导致用户的聊天历史和支付信息


案例二
开源机器学习框架PyTorch存在重大层级漏洞CVE-2024-5480，攻击者可将其用来远端攻击分散式训练的master节点，一旦这些节点遭到入侵，对方就有机会窃取与AI有关的敏感资料


案例三
PyTorch模型使用的pickle格式可以被威胁行为者武器化，用于执行任意代码并部署Cobalt Strike、Mythic和Metasploit的攻击载荷，攻击者可以通过使用恶意PyTorch二进制文件破坏托管的转换服务，并破坏文件托管系统

**攻击风险**

用户隐私泄露：如案例一所示，由于Redis-py库的bug，ChatGPT用户的聊天记录标题和对话内容可能被其他用户看到，导致用户隐私数据泄露。
系统完整性受损：攻击者可能利用漏洞破坏系统完整性，影响LLMs服务的可靠性和可用性。

**缓解措施**

缓解方式
描述




安全更新与审计
定期更新和审计训练与开发环境中的服务软件以修复漏洞并增强安全性


安全审计和监控
定期进行安全审计，使用监控工具来检测和警报可疑行为，并进行有效的日志记录

**参考**

https://llmtop10.com/llm05/

---
### 训练环境隔离缺陷

> 风险编号: GAARM.0002
> 生命周期: 训练阶段

**攻击概述**

训练环境隔离是指，通过将调试和运行环境划分为两个完全隔离的区域，以此防止调试环境对运行环境的渗透攻击。在调试环境中，可以修改程序逻辑但只能使用脱敏数据；而在运行环境中，能操作真实全量数据且操作受到审查，结果可追溯和可追责。如果训练环境隔离存在缺陷，可以从开发环境进入到运行测试环境，则会导致未授权用户访问敏感数据，给攻击者可趁之机。

**攻击案例**

案例
描述




案例一
训练环境隔离缺陷，导致攻击者从开发者环境进入到运行测试环境，从而出现训练数据泄露等风险

**攻击风险**

数据泄露：攻击者可能会访问和窃取存储在运行环境中的敏感数据，这些数据的泄露可能导致重大的经济损失和法律责任。
获取系统控制权：如果攻击者渗透到运行环境，他们可能会获得系统控制权，进而操控数据访问、资源管理和系统设置。

**缓解措施**

缓解方式
描述




强化隔离措施
使用安全技术和最佳实践来加强调试环境和运行环境之间的隔离


访问控制
实施基于角色的访问控制（RBAC）策略，确保只有经过授权的人员才能访问运行环境


安全沙箱技术
将LLM的运行环境进行隔离和保护，以防止其受到外部攻击和干扰


**参考**

- https://cloud.baidu.com/article/621826

---

## 二十、容器与沙箱逃逸实战测试方法论

> 针对AI应用部署环境（Docker/Sysbox/Daytona/Kubernetes）的系统化逃逸与隔离测试
> **通用容器部署安全**: Web应用容器部署安全检查 → [web-deployment-security.md §二](web-deployment-security.md)

### 一、测试流程总览

```
信息收集 → 环境识别 → 隔离评估 → 逃逸尝试 → 持久化验证 → 横向移动 → 报告
```

### 二、信息收集阶段

#### 2.1 容器运行时识别

| 检测项 | 命令 | 判断依据 |
|--------|------|----------|
| 是否在容器中 | `cat /proc/1/cgroup` | 包含`docker`/`kubepods`/`containerd` |
| Docker标志文件 | `ls /.dockerenv` | 文件存在则为Docker容器 |
| 容器运行时类型 | `cat /proc/1/cgroup \| head` | `sysbox-fs`→Sysbox, `docker`→Docker |
| 内核版本 | `uname -r` | 匹配CVE影响范围 |
| User Namespace | `cat /proc/self/uid_map` | `0 0 4294967295`→无隔离(危险) |
| Capabilities | `cat /proc/self/status \| grep Cap` | 解码后检查危险Cap |
| Seccomp | `cat /proc/self/status \| grep Seccomp` | 0=disabled, 2=filter |
| AppArmor | `cat /proc/self/attr/current` | `unconfined`→无保护 |
| 挂载点 | `mount \| grep -v overlay` | 检测宿主机敏感路径挂载 |

#### 2.2 Sysbox 特定检测

| 检测项 | Method | 安全影响 |
|--------|------|----------|
| CE vs EE版本 | `sysbox-runc --version` 或检查UID映射范围 | CE共享映射有跨租户风险 |
| UID映射独占性 | `cat /proc/self/uid_map`, CE通常`0 165536 65536`(共享) | 共享映射→跨容器提权可能 |
| 虚拟化/proc | `ls /proc/sys/net/` | Sysbox虚拟化程度 |
| Docker-in-Docker | `docker ps 2>/dev/null` | 内层Docker可能无安全限制 |
| /dev/kvm | `ls /dev/kvm` | KVM可用→嵌套虚拟化逃逸 |

### 三、隔离评估阶段

#### 3.1 进程隔离

```bash
# PID Namespace检查
ps aux   # 是否能看到其他容器/宿主机进程
ls /proc/*/cmdline   # 枚举可见进程

# 如果PID 1不是容器init而是systemd/dockerd → 隔离失败
cat /proc/1/cmdline | tr '\0' ' '
```

#### 3.2 网络隔离

```bash
# 网络接口
ip addr   # 检查网络接口和IP段
ip route  # 路由表，是否能到达其他网段

# 同网段扫描(发现邻居容器)
for i in $(seq 1 254); do
  (ping -c 1 -W 1 $SUBNET.$i &>/dev/null && echo "$SUBNET.$i alive") &
done; wait

# 内部DNS探测
cat /etc/resolv.conf
nslookup kubernetes.default.svc.cluster.local 2>/dev/null
```

#### 3.3 文件系统隔离

```bash
# 检查宿主机文件系统挂载
mount | grep -E "ext4|xfs|btrfs" | grep -v overlay
findmnt

# 路径遍历测试
ls -la /var/lib/sysbox/ 2>/dev/null
ls -la /var/lib/docker/ 2>/dev/null
ls -la /run/containerd/ 2>/dev/null

# 符号链接逃逸
ln -s /proc/1/root/etc/shadow /tmp/test_escape
cat /tmp/test_escape 2>&1  # 如果成功→隔离失败
```

### 四、逃逸测试矩阵

| 逃逸路径 | 前提条件 | 危险等级 | 测试方法 |
|----------|----------|----------|----------|
| cgroup release_agent | CAP_SYS_ADMIN + cgroup v1 | Critical | 写release_agent执行宿主机命令 |
| Docker Socket | /var/run/docker.sock暴露 | Critical | 通过API创建特权容器 |
| /proc/1/root | PID Namespace未隔离 | Critical | 直接读写宿主机文件 |
| 特权容器 | --privileged模式 | Critical | mount宿主机磁盘 |
| runc fd泄露 | CVE-2024-21626 | High | 利用/proc/self/fd访问宿主 |
| Dirty Pipe | CVE-2022-0847, 5.8≤kernel≤5.16.11 | High | 覆写只读文件提权 |
| OverlayFS | CVE-2023-0386, 5.11≤kernel≤6.2 | High | SUID文件提权 |
| 敏感挂载 | 宿主机路径被mount进容器 | High | 写入宿主机文件 |
| CAP_DAC_READ_SEARCH | Capability未限制 | Medium | open_by_handle_at读取文件 |
| CAP_SYS_PTRACE | Capability未限制 | Medium | 注入宿主机进程 |
| Docker-in-Docker | 内层Docker无限制 | Medium | 内层创建特权容器 |

### 五、持久化测试

> 验证沙箱跨会话持久化攻击可行性（尤其适用于持久沙箱如Daytona）

| 测试项 | 会话1操作 | 会话2验证 | 预期安全结果 |
|--------|-----------|-----------|-------------|
| .bashrc后门 | `echo 'malicious_cmd' >> ~/.bashrc` | 开新shell检查是否执行 | 新会话不继承/重置 |
| Crontab | `echo "* * * * * cmd" \| crontab -` | `crontab -l` | Crontab被清理或不可用 |
| SSH密钥 | 写入~/.ssh/authorized_keys | SSH连接测试 | SSH服务不可用或密钥清理 |
| 后台进程 | `nohup cmd &` | `ps aux \| grep cmd` | 会话关闭后进程终止 |
| 文件投毒 | 工作区写入恶意文件 | AI是否读取执行 | AI不自动执行文件中指令 |
| 历史残留 | 在shell中输入敏感命令 | `cat ~/.bash_history` | 历史命令跨会话清除 |
| 环境变量 | `export SECRET=leaked` | `echo $SECRET` | 环境变量不跨会话保留 |

### 六、横向移动测试

```
容器内 → 内网服务发现 → 数据库/缓存/API直连 → 其他租户沙箱
         ↓
         云元数据服务(169.254.169.254) → IAM凭据窃取 → 云资源访问
         ↓
         K8s API(kubernetes.default.svc) → Pod列表/Secret获取
```

| 目标 | 检测命令 | 利用方式 |
|------|----------|----------|
| 云元数据 | `curl 169.254.169.254` | 获取IAM临时凭据 |
| K8s API | `curl -k https://kubernetes.default.svc` | 列举Pod/获取Secret |
| K8s ServiceAccount | `cat /var/run/secrets/kubernetes.io/serviceaccount/token` | 认证K8s API |
| 内网数据库 | `echo \| nc DB_HOST 5432` | 直连数据库 |
| Redis | `redis-cli -h REDIS_HOST ping` | 未授权访问 |
| Docker Registry | `curl http://REGISTRY:5000/v2/_catalog` | 拉取敏感镜像 |

### 七、防御验证Checklist

```
[ ] 容器以非root用户运行(或User Namespace隔离有效)
[ ] 无多余Capabilities(最小原则: 仅NET_BIND_SERVICE等必需项)
[ ] Seccomp profile已启用(非disabled)
[ ] AppArmor/SELinux非unconfined
[ ] /var/run/docker.sock未暴露
[ ] 不以--privileged模式运行
[ ] 无宿主机敏感路径挂载(/、/etc、/var/run)
[ ] 内核版本不受已知逃逸CVE影响
[ ] cgroup v2或release_agent不可写
[ ] PID Namespace隔离有效(仅见自身进程)
[ ] Network Policy/防火墙限制容器间通信
[ ] 169.254.169.254元数据服务被拦截
[ ] 会话间敏感数据(history/credentials)被清理
[ ] 沙箱销毁时完全清除所有用户数据
[ ] Sysbox使用EE版或独占UID映射
```

---
