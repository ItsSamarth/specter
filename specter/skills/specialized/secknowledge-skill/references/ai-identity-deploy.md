# AI Identity Security - Deployment Phase

> Source: AISS NSFOCUS Large Model Security Smart-Chain Community | Split from ai-identity-security.md
> Phase: Deployment Phase (Unauthorized Access / Credential Abuse)

## Deployment Phase

### Exposure of Public-Facing Service API Keys

> Risk ID: GAARM.0049.001
> Lifecycle: Deployment Phase

**Attack Overview**

This risk refers to situations where service API access tokens (authentication credentials) are exposed through code, configuration files, or other means, potentially allowing attackers to illegally obtain access to the model deployment environment, leading to data leakage, model manipulation, and other security risks.

**Attack Cases**

Case | Description
--- | ---
Case 1 | AI cybersecurity startup Lasso discovered that more than 1,600 Hugging Face API tokens were leaked in code repositories, affecting accounts at hundreds of organizations.

**Attack Risks**

- Account leakage: leaked API tokens may lead to unauthorized access to company and organizational accounts.
- Data manipulation: attackers who control accounts can manipulate existing AI models, planting malicious code in them and affecting downstream users who depend on these foundation models.

**Mitigations**

Mitigation | Description
--- | ---
Strengthen authentication | Implement enhanced authentication measures such as multi-factor authentication to reduce the risk of API tokens being stolen.
Revoke leaked API tokens | For all API tokens that may have been leaked, immediately revoke and replace them.
Key management and rotation mechanism | Establish a secure key management and rotation mechanism, and regularly update API tokens.

**References**

- https://www.securityweek.com/major-organizations-using-hugging-face-ai-tools-put-at-risk-by-leaked-api-tokens/
- https://aws.amazon.com/cn/what-is/api-key/

---
### Unauthorized Access to Vector Databases

> Risk ID: GAARM.0050
> Lifecycle: Deployment Phase

**Attack Overview**

In the development of RAG applications, local documents of various types can be divided into shorter passages using the Text class, and the textual content is vectorized using embedding models and ultimately stored in a vector database. Attackers can tamper with and damage the model by gaining unauthorized access to the database, further affecting the RAG system to perform inaccurate or malicious retrieval. This may affect the output content of the RAG system, as well as introduce the risk of indirect prompt injection.

  

RAG Application Architecture

**Attack Cases**

Case | Description
--- | ---
Case 1 | anything-llm has CVE-2024-0551 vulnerability; unauthorized attackers can exploit the vulnerability to download files from the database.
Case 2 | This research proposes a new attack method against RAG-enhanced LLMs that compromises a victim's RAG system by injecting a single malicious document into its knowledge database, thereby triggering multiple types of malicious attacks against the generative model.

**Attack Risks**

- Vector database corruption: unauthorized modifications may corrupt the knowledge source, causing the RAG system to perform inaccurate or malicious retrieval.
- Information leakage: sensitive information stored in the vector database may be leaked.
- Indirect prompt injection risk: attacks on the availability of vector databases may affect RAG systems that rely on them.

**Mitigations**

Mitigation | Description
--- | ---
Data encryption | Encrypt the vector database storing all indexed and embedded data to protect data from potential leakage or unauthorized access.
Identity authentication and access control | Use robust user authentication and authorization mechanisms to ensure that only authorized personnel can access the database.
Backup and redundant storage | Regular backups ensure that the knowledge source can be restored in the event of data corruption or loss.
Security updates and audits | Regularly update and audit related vector database systems to fix vulnerabilities and enhance security.

**References**

https://medium.com/@nitishjoshi060291/llm-hallucinations-fix-it-with-vector-database-de04eee531da
https://cloudsecurityalliance.org/blog/2023/11/22/mitigating-security-risks-in-retrieval-augmented-generation-rag-llm-applications
https://www.cnblogs.com/LittleHann/p/17440063.html#_label3
https://dongnian.icu/llms/llms_article/9.%E6%A3%80%E7%B4%A2%E5%A2%9E%E5%BC%BALLM/index.html
https://cloudsecurityalliance.org/blog/2023/11/22/mitigating-security-risks-in-retrieval-augmented-generation-rag-llm-applications

---
### Unauthorized Access to Model Deployment Environment

> Risk ID: GAARM.0051
> Lifecycle: Deployment Phase

**Attack Overview**

This risk refers to situations where attackers exploit misconfiguration, known vulnerabilities, or the lack of appropriate authentication and authorization mechanisms in ML deployment platform services to achieve unauthorized access to the ML deployment environment and then engage in stealing sensitive data, abusing computing resources, damaging the integrity of AI models, or conducting other malicious activities.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Attackers exploited the unauthorized API access risk in the Ray framework to achieve remote code execution and gain control of the target enterprise's computing resources.

**Attack Risks**

- Sensitive information leakage: attackers may access and steal sensitive information such as training data, model parameters, and user data.
- Malicious operations: unauthorized access may lead to malicious manipulation of the model, causing its outputs to be misleading.
- Resource abuse: attackers may use computing resources in the ML deployment environment without authorization for cryptocurrency mining or other compute-intensive tasks.
- Model integrity damage: attackers may modify or contaminate the AI model's training process, causing the model's accuracy to decline or producing misleading results.
- Service interruption: attackers' actions may cause ML services to be interrupted, affecting business continuity.

**Mitigations**

Mitigation | Description
--- | ---
Strengthen identity authentication and access control | Implement access control and authentication mechanisms to prevent unauthorized access to the LLM deployment platform environment and its data; avoid using default authentication strategies of ML platform services.
Regular updates and patching | Timely update the ML platform and its dependent libraries to fix known vulnerabilities.
Model protection and secure deployment | Before deployment, perform security scanning and penetration testing on models; use encryption, digital signatures, and other technical means to protect the confidentiality and integrity of model parameters and training data.

**References**

https://www.leewayhertz.com/security-in-ai-development/

---
### Abuse of Deployment Environment Credentials

> Risk ID: GAARM.0049
> Lifecycle: Deployment Phase

**Attack Overview**

In the MLOps lifecycle process of large models, access credentials (such as keys or access tokens) are involved in multiple stages including code submission, building, testing, and deployment. The risk of abuse of deployment environment credentials refers to security vulnerabilities in the use of API keys or access tokens for accessing and deploying model services in the large model CI/CD (continuous integration/continuous deployment) pipeline. Attackers can exploit this risk through credential theft, malicious code injection, and similar means, causing sensitive information leakage, malicious code injection, or other security threats.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Credentials are hard-coded in code or configuration files; after an attacker gains access to a development machine, they use the credentials to achieve lateral movement.

**Attack Risks**

- Credential leakage: attackers obtain developer credentials through social engineering or other means, then use these credentials to access sensitive data in the CI/CD system or execute malicious operations.
- Malicious code injection: attackers use obtained credentials to submit commits containing malicious code to the code repository; this code is then executed during subsequent build and deployment processes.

**Mitigations**

Mitigation | Description
--- | ---
Strengthen identity authentication and password policies | Recommend that users follow appropriate password policies and implement two-factor authentication (2FA).
Code auditing and automated scanning | Before code submission and deployment, perform automated security scanning to detect the risk of hard-coded credentials and identify potential security issues.
Monitoring and alerting | Deploy monitoring systems to detect unusual access patterns or operations and issue timely alerts.

**References**

https://atmosphericthinking.medium.com/massive-leak-of-chatgpt-credentials-over-100-000-affected-db6cef3a18c5
https://blog.csdn.net/FreeBuf_/article/details/140870185?utm_relevant_index=7

---
