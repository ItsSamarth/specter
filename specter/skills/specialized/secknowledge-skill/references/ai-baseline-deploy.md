# AI Foundation Security - Deployment Phase

> Source: AISS NSFOCUS Large Model Security Intelligence Community | Split from ai-baseline-security.md
> Phase: Deployment phase (container vulnerabilities / cloud platform / supply chain)

## Deployment Phase

### CI&CD Pipeline Attacks

> Risk ID: GAARM.0004
> Lifecycle: Deployment phase

**Attack Overview**

Throughout the full lifecycle of large model development, the CI/CD pipeline is responsible for pushing the model from the development environment to the production environment, automatically deploying the LLM, and handling subsequent updates and maintenance. CI&CD pipeline attacks refer to attacks where, during the process of the CI/CD pushing the model to production, due to vulnerabilities in the CI/CD infrastructure or unreliable third-party tools, an attacker can exploit these security vulnerabilities to attack the CI/CD pipeline—for example by submitting malicious code or poisoning dependency packages—leading to serious consequences such as the model being illegally tampered with or sensitive information being leaked.

Large model development lifecycle CI/CD pipeline

**Attack Cases**

Case
Description




Case 1
Obtain the credentials of developers or operations personnel through phishing, then submit malicious code into the CI/CD pipeline.


Case 2
Exploit server vulnerabilities, such as vulnerabilities in CI/CD infrastructure like Gitlab and Jenkins, to carry out attacks.


Case 3
Attack third-party tools and application dependencies, for example by poisoning dependency packages or forging dependency package names to upload malicious packages to a public central repository.

**Attack Risks**

Virtual environment poisoning: The virtual environment or container in the continuous integration environment is compromised, and the attacker may tamper with dependencies or runtime configurations in the environment to affect the results of model training and deployment.
Build and deployment pipeline tampering: The attacker may attempt to modify the automated build and deployment pipeline to insert malicious code or operations during the model deployment process.
Sensitive information leakage: Sensitive information (such as access credentials, configuration files, keys, etc.) is stored in the CI/CD environment; once obtained by an attacker, it may lead to sensitive information leakage and privacy risks.
Denial-of-service attacks: The attacker may attempt to use a denial-of-service (DoS) attack to render the CI/CD system inoperable, causing the model development and deployment process to be interrupted or delayed.
Unauthorized model access: When the model deployment process is attacked, the attacker may obtain unauthorized access through vulnerabilities, thereby illegally operating or tampering with the model.

**Mitigations**

Mitigation
Description




Strengthen access control and permission management
Restrict access to the CI/CD system and related environments, ensuring that only authorized personnel can access critical resources


Security updates and audits
Regularly update and audit model deployment software to fix vulnerabilities and enhance security


Strengthen monitoring and logging
Detect abnormal activity and attack behavior in a timely manner, and take responsive measures promptly to reduce potential security risks and losses

**Reference**

https://github.com/knownsec/KCon/blob/master/2023/CICD%E6%94%BB%E5%87%BB%E5%9C%BA%E6%99%AF.pdf

---
### Cloud Platform Multi-Tenant Isolation Failure

> Risk ID: GAARM.0003.001
> Lifecycle: Deployment phase

**Attack Overview**

In a multi-tenant cloud platform architecture, each tenant should have an independent operating environment and data storage, ensuring mutual isolation of user behavior and data. Isolation failure may be caused by design flaws, misconfigurations, etc. As high-value compute services become widespread, attackers may use this to break through tenant boundaries, access and tamper with the data of other tenants, and even execute malicious operations, thereby leaving the data and resources of different tenants (users or organizations) inadequately protected and causing a series of security problems.

**Attack Cases**

Case
Description




Case 1
This article studies "whether AI models run in an isolated environment." Wiz used the IMDS metadata service in AWS to complete Amazon EKS privilege escalation and then take over the entire cluster service, performing lateral movement within the EKS cluster and further enabling cross-tenant access leading to sensitive data leakage

**Attack Risks**

Data leakage: Multi-tenant isolation failure may lead to confusion or leakage of data between tenants, which may include sensitive information or personally identifiable information.
Reduced trust: A security incident may weaken users' trust in the cloud service provider.

**Mitigations**

Mitigation
Description




Strengthen access control
Strengthen access control over system resources through permission control mechanisms such as access control lists (ACLs) and role-based access control (RBAC)


Resource monitoring
Monitor resource usage to detect abnormal behavior in a timely manner, such as resource preemption or abuse

**Reference**

https://xie.infoq.cn/article/536a3e7e776eb32b38d1a9747
https://www.helloaliyun.com/tutorial/1039.html
https://support.huaweicloud.com/usermanual-gaussdbformysql/gaussdbformysql_05_0347.html

---
### Cloud Platform Security Vulnerabilities

> Risk ID: GAARM.005
> Lifecycle: Deployment phase

**Attack Overview**

Due to the high demand for compute, large model applications usually need to rely on a cloud platform environment to complete training and inference tasks, so the security of the cloud platform is crucial to the security of the large model. However, due to security risks caused by the cloud platform's technical flaws, technical vulnerabilities, lack of multi-factor authentication, and other reasons, attackers can exploit these security issues to maliciously attack large models deployed on the cloud—for example reading sensitive data, or illegally stealing and using account credentials—causing a series of losses to the platform, including but not limited to data leakage, service interruption, and malicious code execution. These attacks not only affect the security of the large model but may also threaten other users of the cloud service.

**Attack Cases**

Case
Description




Case 1
A CSRF vulnerability was found in the Amazon SageMaker Notebook service; attackers may exploit the vulnerability to read sensitive data and perform arbitrary operations in the customer environment


Case 2
Because the system based on the Laravel version (CVE-2021-3129) had security risks and was vulnerable, an attacker used AWS credentials stolen from Laravel to illegally probe the cloud-hosted model services usable with those credentials, causing the victim to lose more than $46,000 per day

**Attack Risks**

Data leakage: Due to reasons such as cloud application security vulnerabilities and insecure APIs, sensitive information may be accessed or exposed by unauthorized third parties, causing serious privacy and compliance problems.
Unauthorized access to model applications: Cloud platform security vulnerabilities may lead to the risk of unauthorized access to model applications deployed by users.

**Mitigations**

Mitigation
Description




Strict access control
Ensure that only authenticated and authorized users can access API endpoints


Principle of least privilege
Implement the principle of least privilege, ensuring that users and processes only have the access permissions necessary to complete their tasks

**Reference**

https://developer.aliyun.com/article/1430094

---
### Exploiting Insecure System Configurations

> Risk ID: GAARM.0003
> Lifecycle: Deployment phase

**Attack Overview**

This risk refers to attacks against the model foundation environment carried out by an attacker exploiting a series of insecure system configurations in the ML model deployment system, deployment cluster environment, deployment container environment, image push management environment, and other parts of the infrastructure environment in which the model is deployed.


Unauthorized access: Misconfiguration may lead to exposure of sensitive ports or weakened authentication mechanisms, allowing unauthorized users to access system resources;


Container security risks: Insecure container configurations may include unnecessary privileges, sensitive file mounts, or container escape vulnerabilities;


Cluster security risks: In clusters such as Kubernetes, improper RBAC configuration may lead to privilege escalation or lateral movement attacks;


Image security risks: Insecure system configurations cause risks such as image leakage during transfer, management, deployment, and other stages;


Environment isolation risks: Misconfiguration may cause isolation failure, allowing attackers to access or affect other containers or the host machine;

**Attack Cases**

Case
Description




Case 1
ShadowRay: the first known attack campaign actively exploiting AI workloads in the wild

**Attack Risks**

Malicious operations: If the system is misconfigured, attackers may exploit these vulnerabilities to gain access to the system and then perform malicious operations.
Data leakage: Attackers may obtain sensitive data, such as file system information on the host machine or secrets within the cluster.
Service interruption: Attackers may disrupt the host machine or cluster service, causing service unavailability.
Lateral movement: Attackers may use an escaped container or a privilege-escalated node as a pivot to further attack other systems on the internal network.
Persistent control: Attackers may install a backdoor on the host machine or in the cluster to achieve long-term control.

**Mitigations**

Mitigation
Description




Principle of least privilege
Ensure that containers and cluster components only have the minimum privileges necessary to complete their tasks


Ensure secure system configuration
Avoid using privileged containers, configure RBAC reasonably, restrict access to the APIServer, and avoid unnecessary risk exposure


Regular updates and patch management
Update container and cluster components in a timely manner and apply security patches to reduce the risk of exploitation

**Reference**

https://pradiptabanerjee.medium.com/confidential-containers-for-large-language-models-42477436345a

---
### Vector Database Vulnerabilities

> Risk ID: GAARM.0005 (sub-risk 1, parent risk: Deployment environment component supply chain vulnerabilities)
> Lifecycle: Deployment phase

**Attack Overview**

During RAG application development, various local document data are divided by Text classes into shorter passages, the text content is vectorized using an embedding model, and finally stored in a vector database. The vector database plays an important role in the RAG application architecture, especially when processing high-dimensional data and executing approximate nearest neighbor (ANN) queries. Because of the importance of the vector database, if it has vulnerabilities, an attacker can exploit them to obtain unauthorized data access, tamper with data, execute malicious code, or launch other attacks, thereby achieving goals such as obtaining sensitive information and remotely manipulating malicious code, resulting in data-related losses.

**Attack Cases**

Case
Description




Case 1
Exploiting the Qdrant vector database API to achieve file upload after a path traversal, leading to a remote code execution risk


Case 2
anything-llm has the CVE-2024-0551 vulnerability, allowing an unauthorized attacker to download files from the database through the vulnerability


Case 3
This research proposes a new attack method targeting RAG-enhanced LLMs, compromising the victim's RAG system by injecting a single malicious document into its knowledge database, thereby triggering various malicious attacks against the generative model.

**Attack Risks**

Data tampering: Attackers exploit vector database vulnerabilities to tamper with embedding vectors, causing data in the database to be tampered with and thereby affecting data integrity.
User privacy violation: The vector database may store sensitive information such as personal identities; once obtained by an attacker, this would seriously violate user privacy.

**Mitigations**

Mitigation
Description




Regular patch updates
Stay informed of the latest patches from the vector database provider; regularly updating the database software ensures protection against known vulnerabilities


Data backup
Back up data regularly to ensure that data can be quickly restored if it is tampered with


Monitoring and logging
Implement real-time monitoring and logging to detect and respond to suspicious activity in a timely manner

**Reference**

https://ironcorelabs.com/security-risks-rag/

---
### Container && Cluster System Vulnerabilities

> Risk ID: GAARM.0005 (sub-risk 2, parent risk: Deployment environment component supply chain vulnerabilities)
> Lifecycle: Deployment phase

**Attack Overview**

Container and cluster system vulnerability risks in a large model deployment environment mainly involve the security problems that may exist in container technology and cluster management systems within the large model deployment and runtime environment. Attackers can exploit these vulnerabilities to execute malicious code, steal data, interfere with service operation, etc., causing privacy information leakage and thereby threatening the security and stability of the large model.

**Attack Cases**

Case
Description




Case 1
The Docker image version used by OpenAI has the CVE-2023-28432 vulnerability; exploiting this vulnerability can obtain information such as keys

**Attack Risks**

Container escape: Attackers may achieve container escape through vulnerabilities inside the container to gain privileges on the host or other containers.
Cluster risk propagation: A vulnerability in a single container may cause risk to propagate across the entire cluster.

**Mitigations**

Mitigation
Description




Update related components in a timely manner
Regularly update Kubernetes and its related components (such as Docker, containerd, etc.) to the latest versions to fix known security vulnerabilities


Strict access control
Implement strict access control policies to restrict communication between containers and between containers and the outside of the cluster

**Reference**

https://www.securityweek.com/chatgpt-data-breach-confirmed-as-security-firm-warns-of-vulnerable-component-exploitation/

---
### Model Deployment Service Vulnerabilities

> Risk ID: GAARM.0004.001
> Lifecycle: Deployment phase

**Attack Overview**

ML model deployment service vulnerabilities may exist in the model's interfaces, supporting libraries, or applications that interact with the model—for example, stealing model parameters through specific vulnerabilities, tampering with model prediction results, or directly controlling the service hosting the model. Through vulnerabilities, attackers can attack the system, for example by reading arbitrary files or implanting backdoors to gain control of the system. Because ML model deployment services usually support pushing and deploying models in container form to local environments, cloud platform ML hosting services, cloud K8S clusters, and various other target environments, once the ML model deployment service is attacked, the control privileges of multiple downstream environments are at risk of being stolen.

**Attack Cases**

Case
Description




Case 1
MLFlow has a file read vulnerability, allowing attackers to read arbitrary files on the target server


Case 2
BentoML has a deserialization code execution vulnerability, allowing attackers to trigger exploitation by sending a single POST request

**Attack Risks**

Supply chain attack: If the supply chain of the deployment tool is infiltrated by an attacker, they may implant a backdoor in the tool, thereby gaining control of the entire system.
Data leakage: MLOps software involves multiple critical stages of model training and deployment; once controlled, it can lead to the leakage of sensitive information such as training data and model parameters.
Model tampering: The model's parameters or logic may be modified by an attacker, leading to incorrect prediction results.

**Mitigations**

Mitigation
Description




Security updates and audits
Regularly update and audit model deployment software to fix vulnerabilities and enhance security


Access control
Implement strict access control measures to ensure that only authorized users can access and modify the deployed model


Monitoring and logging
Implement real-time monitoring and logging to detect and respond to suspicious activity in a timely manner

**Reference**

http://www.bimant.com/blog/top8-ml-model-deployment-tools/
https://mlflow.org/docs/latest/deployment/index.html

---
### Model Image Poisoning

> Risk ID: GAARM.0004.002
> Lifecycle: Deployment phase

**Attack Overview**

This risk refers to the situation where, after the model completes the training and fine-tuning phase, the model image is about to be released to the production environment for deployment (self-built environment, public cloud, or third-party infrastructure), and adequate security protection measures are lacking during this release process (such as encrypted signing during model image transfer). Through image poisoning, an attacker can control the operation of the infected system, creating risks such as the image file being hijacked and tampered with, thereby affecting the model's decision-making process and creating security hazards.

Model image push and deployment

**Attack Cases**

Case
Description




Case 1
The attacker controls the image deployment process of the CI/CD system to implant backdoor code in the image or steal sensitive data

**Attack Risks**

Command execution: Through image poisoning, the attacker can control the operation of the infected system and execute arbitrary commands.
Model decision impact: Malicious model image poisoning may affect the model's decision-making process and create security hazards.

**Mitigations**

Mitigation
Description




Image signing
Use image signing and verification mechanisms to ensure the integrity of image content


Trusted hardware use
Based on a trusted runtime environment such as confidential containers, ensure the confidentiality, integrity, and security of dynamic runtime data


Image scanning
Perform security scanning of container images before deployment to detect and fix known vulnerabilities

**Reference**

https://www.docker.com/blog/llm-docker-for-local-and-hugging-face-hosting/
https://collabnix.com/large-language-models-llms-and-docker-building-the-next-generation-web-application/
https://mp.weixin.qq.com/s/vIDHBLbA5iWoPlYTKHSZfw

---
### Environment Isolation Defects

> Risk ID: GAARM.0003.001
> Lifecycle: Deployment phase

**Attack Overview**

This risk refers to configuration or design defects in the sandbox environment isolation between the runtime environment and the physical environment of LLM business applications during the container deployment phase. Applications in a sandbox environment such as a container or virtual machine may have security vulnerabilities allowing them to escape the sandbox environment and access or manipulate resources outside the sandbox. Therefore, even if an attacker is confined within the container, they can exploit misconfigurations (privileged containers, incorrect file mounts, etc.) to bypass isolation and access resources and sensitive systems outside the container, and then use the execution entity to achieve unauthorized access or other unintended LLM operations, bringing unexpected risks such as executing unauthorized commands.

Execution entity environment isolation architecture

Because LLMs need to interact with the external environment through an execution entity, using Pods in a cluster environment to quickly start an execution entity to perform specific interactive operations is a common execution entity environment isolation architecture. During this process, failure to properly isolate the network, files, processes, Pod survival time, and other aspects of the environment leads to unexpected risks.

**Attack Cases**

Case
Description




Case 1
Because the Hugging Face model runtime environment did not properly restrict external network access, attackers were able to obtain shell control privileges in the production environment

**Attack Risks**

Container escape: Imperfect environment isolation may lead to container escape, allowing attackers to gain control of the host system from within the container and even access data in other containers.
Sensitive database access: Attackers use carefully crafted prompts to instruct the LLM to extract and leak confidential information from sensitive databases.
System-level operations: If the LLM is allowed to perform system-level operations, attackers may manipulate it to execute unauthorized commands on the underlying system.

**Mitigations**

Mitigation
Description




Strict access control
Implement role-based access control (RBAC) policies to ensure that only authorized personnel can access the runtime environment


Network isolation
Use network policies to restrict inter-container, inter-cluster, and external access permissions, reducing the potential attack surface and risk


Implement sandboxing technology
Use appropriate sandboxing technology to isolate the LLM environment and prevent it from interacting with critical systems and resources

**Reference**

https://cloud.baidu.com/article/621826
https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_Sandboxing.html

---
### Deployment Environment Component Supply Chain Vulnerabilities

> Risk ID: GAARM.0005 (parent risk, includes sub-risks: Vector database vulnerabilities, Container && cluster system vulnerabilities)
> Lifecycle: Deployment phase

**Attack Overview**

Supply Chain Vulnerabilities in Deployment Environments refer to security defects existing in the links of the software supply chain and deployment process—from raw materials (such as libraries, dependencies, development tools) to the final product (such as deployed software)—that may lead to vulnerability risks of the system being attacked or data being leaked. Supply chain vulnerabilities can be exploited during software deployment, reducing the security of the system and causing data leakage or service interruption. They are mainly divided into three categories:


Container && cluster system vulnerabilities: Container technology and cluster management systems may have security problems, and attackers can exploit these vulnerabilities to execute malicious code, steal data, interfere with service operation, etc., causing privacy information leakage and thereby threatening the security and stability of the large model.


Vector database vulnerabilities: If a vector database has vulnerabilities, attackers can exploit them to obtain unauthorized data access, tamper with data, execute malicious code, or launch other attacks, thereby achieving goals such as obtaining sensitive information and remotely manipulating malicious code, resulting in data-related losses.


Cloud platform security vulnerabilities: If the cloud platform has security risks caused by technical flaws, technical vulnerabilities, lack of multi-factor authentication, and other reasons, attackers can exploit these security issues to maliciously attack large models deployed on the cloud—for example reading sensitive data, or illegally stealing and using account credentials—causing a series of losses to the platform, including but not limited to data leakage, service interruption, and malicious code execution.

**Attack Cases**

See sub-risks for details

**Attack Risks**

Data leakage: Attackers may obtain sensitive data; sensitive information accessed or exposed by unauthorized third parties causes serious privacy and compliance problems.
Unauthorized access to model applications: Cloud platform security vulnerabilities may lead to the risk of unauthorized access to model applications deployed by users.
User privacy violation: Once stored sensitive information such as personal identities is obtained by an attacker, it will seriously violate user privacy.

**Mitigations**

Mitigation
Description




Principle of least privilege
Ensure that components only have the minimum privileges necessary to complete their tasks


Regular updates and patch management
Update components in a timely manner and apply security patches to reduce the risk of exploitation

---
