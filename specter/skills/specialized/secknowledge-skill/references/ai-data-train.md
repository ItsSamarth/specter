# AI Data Security - Training Phase

> Source: AISS NSFOCUS Large Model Security Smart-Chain Community | Split from ai-data-security.md
> Phase: Training Phase (GAARM.0009-0011, 0018, 0020 Internal Data Protection / Conversational Corpus Poisoning / Anonymization)

## Training Phase

### Incorrect & Malicious External Data Sources

> Risk ID: GAARM.0010
> Lifecycle: Training Phase

**Attack Overview**

In large language models (LLMs), incorrect or malicious external data sources can introduce multiple security risks that negatively impact model performance and system security. If an LLM relies on incorrect or malicious external data sources, those sources may supply erroneous or misleading information. The model will generate responses based on this data, potentially causing users to receive incorrect information or make misguided decisions.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Because LLMs have the ability to analyze external data such as documents and web pages, introducing adversarial examples into those external data sources can induce the LLM to output toxic content.
Case 2 | This paper designs an attack method called PoisonedRAG. The attack is considered successful if the target model returns the attacker-desired answer to the attacker-crafted target question. In the study, five poisoned texts were injected into an external database containing millions of entries, achieving a 90% attack success rate. This demonstrates the severe consequences of maliciously tampering with external data sources, causing the LLM to output incorrect or misleading information.

**Attack Risks**

- Data integrity compromise: leads to data integrity damage, privacy leakage, security vulnerabilities, and credibility loss.
- External data source legal risk: unauthorized use of copyright-protected data sources during inference may result in lawsuits and fines.
- External data source compliance risk: failure to use data in accordance with industry standards and regulations may cause compliance issues.
- External data source compromise: external attackers may tamper with data sources, causing distortion of data fed into the model.
- Misleading information leakage: the model may be maliciously manipulated by attackers to output incorrect or misleading information, affecting decisions and operations.

**Mitigations**

Mitigation | Description
--- | ---
Audit data sources | Before using external data sources, perform strict validation and review. Ensure that the data sources used are trustworthy, accurate, and free from malicious code or attack payloads.
Input monitoring and filtering | Monitor the inputs and outputs of LLMs in real time, and promptly filter out unsafe or inappropriate content.
Access control | Restrict the model's access permissions to external data sources, ensuring that only authorized users or systems can access them.

**References**

https://mp.weixin.qq.com/s/3WAWy4ZV6Ezft_2MJHMgtg
https://mp.weixin.qq.com/s/yiloJtlmv7MT3df9AnWNZQ

---
### Personal Privacy Data Protection Defects

> Risk ID: GAARM.0009.001
> Lifecycle: Training Phase

**Attack Overview**

The model may have personal privacy protection defects, meaning that data containing personal privacy information may be introduced into the model for training without adequate de-identification or anonymization. Once sensitive information enters the model, the risk of memorizing and inadvertently outputting that private information increases as model parameters grow, potentially leading to privacy leakage. Consequently, such defects may cause the model to inadvertently expose personal identity, behavioral habits, or other sensitive information when processing queries or producing outputs.

**Attack Cases**

Case | Description
--- | ---
Case 1 | GitHub Copilot's improper handling of training-phase data caused it to generate outputs identical to open-source code published by others without authorization. Because much open-source code contains confidential information such as API keys, this also led to the exposure of others' private information.

**Attack Risks**

- Sensitive data leakage: leads to the exposure and misuse of users' personal information, constituting serious privacy violations.
- Social engineering attacks: attackers can use the leaked information to conduct social engineering attacks, deceiving victims into providing more sensitive information and carrying out fraudulent activities.
- Trust crisis: as incidents of sensitive information leakage from LLMs increase, the public may develop concerns about the security of AI technologies and related applications, affecting the degree of trust.

**Mitigations**

Mitigation | Description
--- | ---
Data de-identification | Use rule-based and model-based algorithms to de-identify data, removing or replacing privacy-sensitive content.
Data encryption and access control | Implement data encryption and access control measures to ensure that personal privacy data and corporate sensitive data are fully protected during storage and transmission.

**References**

https://mp.weixin.qq.com/s/c_cIzecyw48MatwKBZbdUg
https://36kr.com/p/2541963790493187

---
### Corporate Sensitive Data Protection Defects

> Risk ID: GAARM.0009.002
> Lifecycle: Training Phase

**Attack Overview**

Corporate sensitive data protection defects refer to situations where, during the training of AI models, insufficiently de-identified or anonymized sensitive information—such as trade secrets, customer information, and financial data—may be introduced into the model. This creates a risk that such data could be accessed or leaked without authorization. This risk not only harms the economic interests and market competitiveness of the enterprise, but may also trigger lawsuits and reputational damage, seriously threatening the overall security and sustainable development of the organization.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Since ChatGPT was launched, 4.7% of employees have pasted sensitive data into the tool at least once. Sensitive data accounts for 11% of what employees paste into ChatGPT, including source code, internal data, and customer data—all of which are private data.
Case 2 | Amazon's corporate lawyers reported finding text in ChatGPT-generated content that was "very similar" to the company's confidential information, possibly because some Amazon employees input internal company data when using ChatGPT to generate code and text.

**Attack Risks**

- Sensitive data leakage: leads to exposure of trade secrets, loss of competitiveness, and intellectual property violations.
- Economic loss: core code and other content included in training data may appear in LLM-generated content, causing financial damage.
- Trust crisis: as incidents of sensitive information leakage from LLMs increase, the public may develop concerns about the security of AI technologies and related applications, affecting trust.

**Mitigations**

Mitigation | Description
--- | ---
Data de-identification | Use rule-based and model-based algorithms to de-identify data, removing or replacing privacy-sensitive content.
Data encryption and access control | Implement data encryption and access control measures to ensure that personal privacy data and corporate sensitive data are fully protected during storage and transmission.

**References**

https://mp.weixin.qq.com/s/VCmhL-LbGfCViQrAEwyCAg
https://mp.weixin.qq.com/s/kp1Sl5TC_uuVelhj8HPmdw

---
### Internal Data Protection Defects

> Risk ID: GAARM.0009
> Lifecycle: Training Phase

**Attack Overview**

Internal data protection defects refer to situations where, in the process of training an LLM, internal data that has not been adequately de-identified or anonymized—such as personal privacy data and corporate sensitive data—is used, creating the risk that such data could be accessed or leaked without authorization and could even lead to financial losses for individuals and enterprises.
Internal privacy protection defects exist mainly in three areas:

- Personal privacy data protection defects: due to security vulnerabilities in the training process, the model may inadvertently expose personal identity, behavioral habits, or other sensitive information when processing queries or generating outputs.
- Corporate sensitive data protection defects: due to security vulnerabilities in the training process, an enterprise's economic interests and market competitiveness may be harmed, potentially triggering lawsuits and reputational damage and seriously threatening the overall security and sustainable development of the organization.
- Confidential sensitive data protection defects: the use of sensitive data involving governments, militaries, and similar entities—such as the locations of sensitive facilities and military deployments—without adequate protection creates the risk of unauthorized access or leakage, and may even result in losses at the strategic information level.

**Attack Cases**

See sub-risks for specific cases.

**Attack Risks**

- Data leakage: an LLM inadvertently outputting large amounts of unauthorized training data will lead to a series of privacy leaks and financial losses.
- Declining trust: as incidents of sensitive information leakage from LLMs increase, the public may develop concerns about the security of AI technologies and related applications, creating a trust crisis.

**Mitigations**

Mitigation | Description
--- | ---
Data de-identification | Use rule-based and model-based algorithms to de-identify data, removing or replacing privacy-sensitive content.
Data encryption and access control | Implement data encryption and access control measures to ensure that personal privacy data and corporate sensitive data are fully protected during storage and transmission.

**References**

https://mp.weixin.qq.com/s/VCmhL-LbGfCViQrAEwyCAg
https://mp.weixin.qq.com/s/kp1Sl5TC_uuVelhj8HPmdw
https://mp.weixin.qq.com/s/c_cIzecyw48MatwKBZbdUg
https://36kr.com/p/2541963790493187

---
### Conversational Corpus Poisoning

> Risk ID: GAARM.0011.001
> Lifecycle: Training Phase

**Attack Overview**

The model supports users using their own data to conduct fine-tuning work, and the conversational corpus carries the risk of being poisoned. In the process of LLM dialogue-based training with users, there is a security risk of malicious fine-tuning with toxic data. Attackers may manipulate conversational corpus data and publish it to publicly accessible locations. The poisoned conversational datasets may be entirely new datasets or poisoned versions of existing open-source datasets. Such data may be introduced into victim systems through manipulation of the machine-learning supply chain, causing degradation in model output quality—for example, generating content containing harmful, biased, or inappropriate information.

**Attack Cases**

Case | Description
--- | ---
Case 1 | OpenAI allows users to fine-tune models using their own data. The conversational corpus data used for fine-tuning carries the risk of being poisoned; attackers can use toxic data to fine-tune GPT models and interfere with downstream decision-making.
Case 2 | This article cites the example of Xiaoice, which learns from a massive corpus and also incorporates its conversational data with users into its own corpus. This type of training introduces the risk of attack: attackers can "train" the model during conversations with it, causing it to produce profanity or even sensitive statements.

**Attack Risks**

- Degraded model output quality: if the dataset used for fine-tuning contains a large amount of negative or harmful content, the model may learn and replicate these undesirable behaviors or tendencies. As a result, the text generated by the model may contain harmful, biased, or inappropriate content.
- Impaired generalization: over-reliance on a specific type of data (e.g., toxic) for fine-tuning may make the model perform well in those specific domains while simultaneously harming its effectiveness and generalization capability in broader, more conventional contexts.
- Reputational risk: if the model is trained to generate inappropriate content, this may create serious public relations and legal risks for the organizations or individuals using the technology.

**Mitigations**

Mitigation | Description
--- | ---
Data cleansing | Cleanse the fine-tuning data used, and reject toxic data from participating in fine-tuning.
Post-processing and rule-based filtering | Implement additional content filtering mechanisms at model output time. Use rule-based or machine-learning methods to identify and filter inappropriate or harmful outputs, ensuring the safety and appropriateness of generated content.
Continuous monitoring and evaluation | Fine-tuned models should be evaluated regularly for performance and bias. Monitor model outputs, promptly identify and correct problems, and ensure the model continuously adapts to and reflects changing social standards.

**References**

https://platform.openai.com/docs/guides/fine-tuning/preparing-your-dataset
https://arxiv.org/abs/2310.03693
https://blog.csdn.net/yalecaltech/article/details/117135011

---
### Improper Data Anonymization

> Risk ID: GAARM.0018.003
> Lifecycle: Training Phase

**Attack Overview**

Improper data anonymization may cause personal identity information or sensitive data to remain identifiable or traceable within training data. For example, incomplete anonymization may expose a user's identity or other personal information. Even after anonymization, attackers may still conduct re-identification attacks by combining other publicly available or acquired data to recover personal information or sensitive content from the original data. This leads to exposure of personal privacy, where users' sensitive information may be accessed by unauthorized individuals, potentially resulting in identity theft, misuse of personal information, or other privacy violations.

**Attack Cases**

Case 1: Improper data anonymization in ChatGPT led to the leakage of user phone numbers, email addresses, and other personal information.

  
Improper data anonymization

**Attack Risks**

- Sensitive data leakage: if data anonymization is improper, it may fail to effectively protect users' personal privacy information.
- Re-identification attack: attackers may combine external data or use specific features for matching in order to re-identify anonymized data, thereby obtaining users' real identities or sensitive information.
- Attribute inference attack: attackers may analyze the attributes and characteristics of anonymized data to infer users' sensitive information or behavioral patterns, thereby violating user privacy.

**Mitigations**

Mitigation | Description
--- | ---
Data de-identification | Use regular expressions, model-based methods, and similar approaches to remove privacy-sensitive content or replace it with substitutes.
Strengthened anonymization strategy | Apply data anonymization techniques such as differential privacy and data perturbation.
Data masking techniques | Use data masking techniques to replace or hide sensitive information, ensuring that anonymized data does not contain information that directly identifies users.
Access permission control | Restrict access permissions to anonymized data, ensuring that only authorized users or systems can access and process the data, thereby reducing the risk of data leakage.
Monitoring and auditing | Regularly monitor and audit the use and access of anonymized data, promptly detect anomalous behavior, and take measures to protect data security.

**References**

https://cloud.baidu.com/article/1819998

---
### Confidential Sensitive Data Protection Defects

> Risk ID: GAARM.0009.003
> Lifecycle: Training Phase

**Attack Overview**

Confidential sensitive data protection defects refer to situations where, in the development and training of AI models, sensitive data involving governments, militaries, and similar entities—such as the locations of sensitive facilities and military deployments—is used without adequate protection. This creates the risk that such data could be accessed or leaked without authorization, and may even result in losses at the strategic information level. For example, ChatGPT could be used to generate a video of a fake political leader delivering fabricated statements and publish it on social media platforms.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Large models can analyze and parse personal data and photos to extract large amounts of sensitive information, including personal identity, location, and movement trajectories. This information can be used to track, trace, and surveil military personnel, leading to privacy violations and physical safety threats.
Case 2 | This article introduces the risk of GPT leaking military-sensitive information and proposes developing isolated cloud-based LLMs that are prohibited from connecting to the internet for learning and can only read specified government documents, thereby ensuring the model remains clean and secure.

**Attack Risks**

- Sensitive data leakage: leads to military secret exposure, loss of competitiveness, and intellectual property violations.
- Economic loss: core code and other content included in training data may appear in LLM-generated content, causing financial damage.

**Mitigations**

Mitigation | Description
--- | ---
Data de-identification | Use rule-based and model-based algorithms to de-identify data, removing or replacing privacy-sensitive content.
Data encryption and access control | Implement data encryption and access control measures to ensure that personal privacy data and corporate sensitive data are fully protected during storage and transmission.

**References**

https://www.eet-china.com/mp/a213535.html

---
### Training Data Poisoning

> Risk ID: GAARM.0011
> Lifecycle: Training Phase

**Attack Overview**

Training data poisoning refers to security vulnerabilities present in the data used during the pre-training, fine-tuning, or embedding stages of a machine learning model. Due to the absence of security controls such as data content review, data cleansing, and data source verification, the trained model may contain vulnerabilities, backdoors, or biases. This can damage the safety, effectiveness, or ethical behavior of the model, causing it to produce unfair or discriminatory results in real-world applications and deliver inaccurate predictions.

**Attack Cases**

Case | Description
--- | ---
Case 1 | This case describes how training data is poisoned by accessing a special service used for training specific data, and then actually using that toxic data to train the model.

**Attack Risks**

- Toxic output: attackers may manipulate training data to introduce bias, causing the model to produce unfair or discriminatory results in its predictions.
- Degraded model capability: maliciously manipulated training data may cause model performance to degrade, producing inaccurate or inefficient predictions in real-world applications.

**Mitigations**

Mitigation | Description
--- | ---
Trusted data sources | Ensure the integrity of training data by obtaining data from trusted sources and verifying its quality.
Data cleansing | Implement robust data cleansing and preprocessing techniques to remove potential vulnerabilities or biases from training data.
Regular auditing | Regularly review and audit the training data and fine-tuning procedures of LLMs to detect potential issues or malicious manipulation.
Monitoring and alerting mechanisms | Leverage monitoring and alerting mechanisms to detect anomalous behavior or performance issues in LLMs, which may indicate the presence of training data poisoning.

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Training_Data_Poisoning.html

---
### Training Data Leakage

> Risk ID: GAARM.0020
> Lifecycle: Training Phase

**Attack Overview**

Training data leakage may expose users' personal privacy information. If training data contains sensitive information such as personally identifiable information, health records, or financial data, leakage of that data constitutes a privacy violation. This security risk allows attackers to infer the content of training data by analyzing model outputs. In particular, when the model's output contains detailed information from the original data, attackers can obtain that data content through reverse engineering.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Data stored by models such as BERT was not adequately de-identified; output results randomly revealed characteristics of certain training data that could be reversed-engineered to recover the originals, demonstrating the consequences of improper data handling.
Case 2 | This case describes how having ChatGPT repeatedly output the word "company" caused it to also produce unrelated content that appeared to be training data.
Case 3 | This case describes instances in which ChatGPT experienced hallucinations and output specific examples and links that appeared to be drawn from training data.

**Attack Risks**

- Sensitive data leakage: training data may contain users' personally identifiable information, sensitive data, or trade secrets. Leaking such data may constitute a violation of users' privacy rights.
- Adversarial attacks: attackers may use leaked training data to launch adversarial attacks, identify weaknesses or flaws in the model, and deceive or mislead the model through carefully crafted inputs.

**Mitigations**

Mitigation | Description
--- | ---
Data de-identification | Use rule-based and model-based algorithms to de-identify data, removing or replacing privacy-sensitive content.
Data encryption and access control | Implement data encryption and access control measures to ensure that personal privacy data and corporate sensitive data are fully protected during storage and transmission.

**References**

https://mp.weixin.qq.com/s/C9eIW06UXKL8g9TkZzGn_w
https://www.techpolicy.press/new-study-suggests-chatgpt-vulnerability-with-potential-privacy-implications/

---
### Training Data Tampering

> Risk ID: GAARM.0011.002
> Lifecycle: Training Phase

**Attack Overview**

The model is exposed to the risk of pre-training data tampering. This refers to a lack of reliable validation of input data to the model, which allows the data to be maliciously tampered with or misleading information to be injected into it. The model may learn incorrect patterns or associations, thereby affecting its prediction accuracy and reliability, and may even lead to harmful outputs in real-world applications.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Because the retrieval module incorrectly recalled irrelevant and misleading information on the topic, the large model was "distracted" and provided an incorrect answer by incorporating the retrieved passage, causing the ChatGPT model to give an answer on the question of "Can German Shepherds enter airports" that was the opposite of its previous correct response.
Case 2 | Attackers can achieve incorrect answers to specific questions by tampering with training data. Since the model was directly trained and distributed by the attacker, using pre-training data that lacks validation during the training phase will lead to the same security risks.

**Attack Risks**

- Degraded model capability: tampering with training data will result in reduced output accuracy, increased false positives or false negatives, and generally unreliable outputs.
- Toxic output: causes the model to generate misleading predictions, which in turn lead to incorrect decisions affecting people's lives, financial situations, and the reputations of AI-dependent institutions.
- Trust erosion: may undermine users' trust in AI models, thereby affecting the widespread adoption of the model.

**Mitigations**

Mitigation | Description
--- | ---
Data cleansing | Validate and cleanse training data, removing incorrect, incomplete, or irrelevant data.
Secure data pipeline | Establish a secure data pipeline to ensure the entire data pipeline from collection to storage to processing is secure.

**References**

https://ensarseker1.medium.com/data-poisoning-attacks-the-silent-threat-to-ai-integrity-d83900eea276
https://www.51cto.com/article/760084.html

---
### Pre-trained Model Data Bias

> Risk ID: GAARM.0010.001
> Lifecycle: Training Phase

**Attack Overview**

Due to a failure to adequately review and cleanse training data during the training phase—or even the injection of excessively opinionated data—pre-trained models may learn unequal or unjust patterns from biased data sources, causing model outputs to contain biases related to race, gender, age, religion, and other characteristics. These biases are reflected in the text or prediction results generated by the model. Biased model outputs may violate fairness and anti-discrimination laws and regulations. For example, biased model outputs may violate equal employment, consumer protection, or other relevant laws. These risks negatively affect the fairness, accuracy, and user experience of the model, and measures must be taken during the training phase to reduce and eliminate bias in the data.

**Attack Cases**

Case 1: The model tends to depict male figures when generating images associated with high-income earning, showing obvious gender bias.

  
Pre-trained Model Data Bias Case 1

Case 2: Stable Diffusion tends to depict female figures when generating characters associated with housework, which may reflect stereotypical social gender roles.

  
Pre-trained Model Data Bias Case 2

Case 3: The model tends to use images of Black individuals when generating prisoner characters, showing obvious gender and racial bias.

  
Pre-trained Model Data Bias Case 3

**Attack Risks**

- Social impact: content containing bias and discrimination may exacerbate social divisions and trigger or intensify social conflicts.
- Legal risk: publishing or distributing hate speech and discriminatory content may violate laws and regulations, resulting in legal liability.
- Reputational damage: enterprises and organizations that fail to effectively manage inappropriate content generated by AI models may damage their public image and reputation.
- Ethical responsibility: developers and operators of AI models have an ethical responsibility to ensure their technology is not used to spread negative and harmful information.

**Mitigations**

Mitigation | Description
--- | ---
Data cleansing | Perform rigorous cleansing and preprocessing of pre-training data to identify and correct biases in the data.
Increase data diversity | Ensure that training data is diverse and representative, covering different groups and scenarios, to reduce the impact of bias.

**References**

https://home.dartmouth.edu/news/2024/01/zeroing-origins-bias-large-language-models

---
