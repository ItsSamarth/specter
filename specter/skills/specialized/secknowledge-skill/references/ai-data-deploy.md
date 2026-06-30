# AI Data Security - Deployment Phase

> Source: AISS Green Alliance Large Model Security Smart Chain Community | Extracted from ai-data-security.md
> Phase: Deployment phase (GAARM.0012-0016 backup/transmission/storage/logs/cache)

## Deployment Phase

### Backup Data Theft

> Risk number: GAARM.0012
> Lifecycle: Deployment phase

**Attack Overview**

Backup data typically contains important information such as model training data, algorithm logic, sensitive data, and personal data. If inadequately protected, attackers can obtain backup data through unauthorized access or other attack methods, leading to leakage of important model-related information and other risks, and even financial risks.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attackers obtained access credentials for a technology company employee via a phishing email, gained unauthorized access to cloud storage services, and stole large model backup data containing sensitive personal information and trade secrets, causing the company to face legal and financial risks |

**Attack Risks**

Model tampering: If backup data contains model training data, algorithms, and other information, attackers can use this information to tamper with the model.
Sensitive data leakage: If backup data contains user, customer, and other information, leakage will lead to identity theft, fraudulent activities, extortion, etc.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Data encryption | Use strong encryption algorithms during backup data storage to ensure data is protected during both storage and transmission, making it difficult to decrypt even if leaked |
| Multi-factor authentication | Introduce multi-factor authentication mechanisms, such as two-factor authentication, to enhance access control for backup data and improve security |

---
### Data Transmission Hijacking

> Risk number: GAARM.0013
> Lifecycle: Deployment phase

**Attack Overview**

During large model pre-training, fine-tuning, and inference services, data needs to be transmitted between different entities or departments. This data often contains various sensitive information and privacy, such as personally identifiable information and financial data. Attackers can obtain relevant private information by maliciously intercepting transmitted data, leading to sensitive information leakage and causing security and privacy issues for users.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Attackers exploited an unencrypted network transmission vulnerability to successfully intercept personal financial data transmitted by a financial institution during large model services, resulting in sensitive information leakage and posing security and privacy risks to users |

**Attack Risks**

Sensitive data leakage: Attackers may obtain sensitive information by intercepting data, such as personally identifiable information, financial data, medical records, etc.
Intellectual property: If data contains trade secrets or proprietary algorithms, data interception may lead to leakage of this intellectual property.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Data encryption | Ensure the security of data during transmission by encrypting sensitive data |

**References**

https://bj.bcebos.com/ensec-web-privacy/anquan/%E5%A4%A7%E6%A8%A1%E5%9E%8B%E5%AE%89%E5%85%A8%E8%A7%A3%E5%86%B3%E6%96%B9%E6%A1%88%E7%99%BD%E7%9A%AE%E4%B9%A6.pdf
https://mp.weixin.qq.com/s/JlJwDRzYG985kF4d6g7qjw

---
### Data Storage Service Attacks

> Risk number: GAARM.0014
> Lifecycle: Deployment phase

**Attack Overview**

This risk refers to potential security hazards in the data storage and organization process, such as insufficient access control, insecure data handling practices, or lack of encryption measures. Attackers exploiting related vulnerabilities can conduct unauthorized access, data leakage, or tampering attacks, obtaining sensitive information, and may even engage in identity theft, fraud, and other activities, exposing user privacy and enterprise assets and creating the potential for data leakage, legal lawsuits, and reputational damage.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | Clearview AI's source code repository was misconfigured to allow any user to access it, exposing production credentials and training data, highlighting the need to strengthen traditional network security measures for ML system security |

**Attack Risks**

Sensitive data leakage: Sensitive data without encryption protection or with improper access control may be obtained by attackers, leading to data leakage.
Identity theft: Stored personally identifiable information may be stolen and used for identity theft, fraud, and other criminal activities.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Access control | Ensure only authorized users can access data in the data repository |
| Data classification | Classify information in the repository and implement appropriate security measures based on data sensitivity |
| Data encryption | Encrypt stored sensitive data so that even if data is accessed without authorization, its content cannot be easily read |

**References**

https://news.cctv.com/2022/06/21/ARTIdhgLL1sSK5Hjl0uYWybr220621.shtml
https://atlas.mitre.org/techniques/AML.T0036

---
### Log and Audit Record Theft

> Risk number: GAARM.0015
> Lifecycle: Deployment phase

**Attack Overview**

Model logs and audit records play a key role in monitoring system activities and events; they record detailed information including user login behavior, file access, system configuration changes, and various security events. After attackers obtain relevant server permissions, theft of logs and audit records can expose users' personal behavior patterns and may also reveal potential system vulnerabilities, causing attackers to launch more targeted attacks.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | This case describes how ChatGPT leaked user login credentials and personal details |

**Attack Risks**

Sensitive data leakage: Leads to personal privacy leakage, account theft, and other problems.
Targeted attacks: Attackers may be able to discover security vulnerabilities and weaknesses in the system, enabling them to launch more targeted attacks.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Regular audits | Regularly audit access and operations of logs and audit records, check for abnormal or unusual behavior, and promptly detect and handle security threats |
| Separate storage of logs and audit records | Store logs and audit records separately from other data, ensuring they are independent of production data to reduce leakage risk |
| Establish access control policies | Establish strict access control policies, only authorizing necessary personnel to access logs and audit records, restricting permission scope, and preventing unauthorized access |

**References**

https://www.kuaikuaicloud.com/market/3667.html

---
### Cache Data & Index Information Theft

> Risk number: GAARM.0016
> Lifecycle: Deployment phase

**Attack Overview**

Cached data and index information may leak users' sensitive information, including but not limited to identity information, payment details, and personal preferences. By illegally accessing cache and index data, attackers can tamper with or destroy data, affecting system operation and data integrity; they can also use this information to carefully plan and implement targeted phishing attacks, using users' personal information to increase the credibility and success rate of attacks, thereby causing more serious security threats and property losses to users.

**Attack Cases**

| Case | Description |
|------|-------------|
| Case 1 | This case describes how OpenAI used Redis to cache user information on servers; due to an error in the client open-source library redis-py, clients incorrectly received cached email addresses belonging to other users |

**Attack Risks**

Sensitive data leakage: Leaked cached data may contain users' credential information, such as usernames and passwords; attackers may use this information to conduct identity theft, account hijacking, and other activities.
Data tampering: Attackers may use this information to tamper with or destroy data in the cache, thereby affecting system operation and data integrity.

**Mitigations**

| Mitigation | Description |
|------------|-------------|
| Data encryption | Ensure data security by encrypting sensitive data |

**References**

http://www.nelab-bdst.org.cn/data/upload/ueditor/20230707/64a78209c719c.pdf

---
