# AI Baseline Security - Training Phase

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-baseline-security.md
> Phase: Training phase (development tool vulnerabilities/environment isolation)

## Training Phase

### Model Development Tool Vulnerabilities

> Risk number: GAARM.0001.001
> Lifecycle: Training phase

**Attack Overview**

Model development and training involves multiple steps including data preprocessing, feature engineering, model selection, training, evaluation, and deployment. If the tools used in this process contain security vulnerabilities, the entire machine learning workflow faces risk. Attackers can exploit these vulnerabilities to tamper with model training data, steal model parameters, or execute specific attacks after the model is deployed, resulting in inaccurate model outputs, stolen parameters, spreading of malicious software, and other serious security consequences.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | TensorFlow contains a code execution vulnerability; there is a code execution risk when loading models |
| Case 2 | PyTorch contains a code execution vulnerability; this vulnerability can execute remote code on a target system within the context of the user running the program, posing a risk of executing malicious code |
| Case 3 | This document covers different TensorFlow use cases, outlining TensorFlow security vulnerability issues, where different use cases bring different risk consequences |

**Attack Risks**

Supply chain attacks: Attackers can plant malicious code in legitimate software packages used for ML development, implementing dependency chain attacks that spread malware during distribution.
Model poisoning: Attackers inject malicious data into training data, affecting the model's decision-making process, causing inaccurate model outputs or introducing bias.
Intellectual property loss: If model parameters are stolen, attackers may copy or illegally use the model.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Regular updates and patching | Keep all development tools and libraries at their latest versions to benefit from the latest security fixes |
| Secure dependency chain | Review the dependency chain to ensure all third-party libraries and packages come from trusted sources |

**References**

https://www.secrss.com/articles/64006
https://huntr.com/bounties/a795bf93-c91e-4c79-aae8-f7d8bda92e2a

---
### Training Data Management System Vulnerabilities

> Risk number: GAARM.0001.002
> Lifecycle: Training phase

**Attack Overview**

Training data management systems are responsible for storing, processing, labeling, and providing data to deliver prepared data to the model for learning. When this system contains supply chain-related security vulnerabilities, attackers can exploit these vulnerabilities to tamper with data, steal data, or even affect model training results through data poisoning.

**Attack Risks**

Data poisoning attacks: Attackers may inject malicious data into training data, affecting the model's decision-making process, causing inaccurate model predictions or introducing bias.
Model theft attacks: Attackers attempt to reverse engineer and obtain model parameters or training data by querying the model, thereby stealing intellectual property.
Data leakage: Attackers obtain sensitive training data through unauthorized access.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Security updates and audits | Regularly update and audit training data management systems to fix vulnerabilities and enhance security |
| Monitoring and logging | Implement real-time monitoring and logging to promptly detect and respond to suspicious activities |

**References**

https://doc.dataiku.com/dss/latest/concepts/homepage/index.html
https://www.secrss.com/articles/62742

---
### Training Environment Security Risks

> Risk number: GAARM.0001
> Lifecycle: Training phase

**Attack Overview**

This risk refers to deep learning frameworks (such as TensorFlow or PyTorch) and necessary dependency libraries used as application development components in the model training and development environment. If the referenced frameworks themselves contain security vulnerabilities, they can cause supply chain attacks on downstream LLM applications, thereby affecting the integrity of training data, ML models, and deployment platforms.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Integration plugin sample code provided by OpenAI contained a vulnerable MinIO Docker image, which could lead to key and password leakage; a vulnerability in the Redis-py library used by ChatGPT led to users' chat history and payment information being exposed |
| Case 2 | The open-source machine learning framework PyTorch contains a significant hierarchical vulnerability CVE-2024-5480; attackers can use it to remotely attack the master nodes of distributed training. Once these nodes are compromised, attackers have the opportunity to steal AI-related sensitive data |
| Case 3 | The pickle format used by PyTorch models can be weaponized by threat actors to execute arbitrary code and deploy Cobalt Strike, Mythic, and Metasploit payloads; attackers can compromise hosted conversion services and file hosting systems using malicious PyTorch binaries |

**Attack Risks**

User privacy leakage: As shown in Case 1, due to a bug in the Redis-py library, ChatGPT users' chat history titles and conversation content may be visible to other users, causing user privacy data leakage.
System integrity compromised: Attackers may exploit vulnerabilities to undermine system integrity, affecting the reliability and availability of LLM services.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Security updates and audits | Regularly update and audit service software in training and development environments to fix vulnerabilities and enhance security |
| Security audits and monitoring | Conduct regular security audits, use monitoring tools to detect and alert suspicious behavior, and perform effective logging |

**References**

https://llmtop10.com/llm05/

---
### Training Environment Isolation Defects

> Risk number: GAARM.0002
> Lifecycle: Training phase

**Attack Overview**

Training environment isolation means dividing the debugging and runtime environments into two completely isolated areas to prevent penetration attacks from the debugging environment into the runtime environment. In the debugging environment, program logic can be modified but only desensitized data can be used; in the runtime environment, full real data can be operated on and operations are subject to review, with results traceable and accountable. If training environment isolation has defects, allowing movement from the development environment into the runtime test environment, this can result in unauthorized user access to sensitive data, giving attackers an opportunity.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Training environment isolation defects allowed attackers to move from the developer environment into the runtime test environment, resulting in risks such as training data leakage |

**Attack Risks**

Data leakage: Attackers may access and steal sensitive data stored in the runtime environment; the leakage of this data may lead to significant financial loss and legal liability.
Gaining system control: If attackers penetrate the runtime environment, they may gain system control, further manipulating data access, resource management, and system settings.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Strengthen isolation measures | Use security technologies and best practices to strengthen isolation between debugging and runtime environments |
| Access control | Implement role-based access control (RBAC) policies to ensure only authorized personnel can access the runtime environment |
| Security sandbox technology | Isolate and protect the LLM runtime environment to prevent it from being subject to external attacks and interference |

**References**

- https://cloud.baidu.com/article/621826

---
