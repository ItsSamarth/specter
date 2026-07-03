# AI Model Security - Training Phase

> Source: AISS NSFOCUS Large Model Security Smart-Chain Community | Split from ai-model-security.md
> Phase: Training Phase (GAARM.0023-0024 Model Backdoor / Insufficient Alignment / Pre-trained Model Poisoning)

## Training Phase

### Model Backdoor

> Risk ID: GAARM.0023
> Lifecycle: Training Phase

**Attack Overview**

Backdoors in LLM models primarily refer to security issues in the training phase caused by the introduction of models from untrusted sources. Currently, LLM model backdoors are mainly divided into two forms:

- Model serialization backdoor: the pre-trained model being used may have been implanted with malicious instructions containing specific serialized data, causing users to trigger deserialization operations when loading and using the model, which then executes preset malicious commands or code.
- Pre-trained model poisoning: the pre-trained model being used may have been implanted with specific malicious training data, causing the model to produce intentional opinion skewing when in use, or even directly tampering with the output results.

Therefore, during the model training phase, strict measures must be taken to prevent the introduction and use of model backdoors.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Primarily introduces a method for attacking compiled deep learning models using reverse engineering techniques. The core of the attack is to inject a malicious backdoor into the victim's model to manipulate the model.
Case 2 | Uses the ROME algorithm to precisely modify the model so that it spreads false information when answering specific questions.

**Attack Risks**

- System vulnerability exploitation: planted backdoors can become system security vulnerabilities; attackers activate the backdoor through specific triggers, thereby controlling or manipulating the model's behavior.
- Sensitive information leakage: backdoors allow attackers to gain unauthorized access under specific conditions, which may lead to the leakage of sensitive information, causing significant losses to individuals and enterprises.
- Toxic content generation: attackers may use the backdoor to have the model generate violent, discriminatory, pornographic, or other inappropriate content.

**Mitigations**

Mitigation | Description
--- | ---
Data source verification | Ensure that all models and datasets used for training and deployment come from trusted sources.
Model auditing and testing | Regularly audit models, use automated tools to detect potential backdoors, and conduct stress tests to evaluate model robustness.
Secure coding practices | Follow the principle of least privilege, restrict model access permissions, implement strict input validation, and reduce potential attack surfaces.
Defensive training | Improve the model's resistance to backdoor attacks by introducing adversarial examples and anomaly detection mechanisms during the training process.
Regular auditing | Conduct regular security audits of LLMs to assess potential security risks.

**References**

https://atlas.mitre.org/techniques/AML.T0018
https://defence.ai/ai-security/backdoor-attacks-ml/
https://arxiv.org/abs/2308.14367

---
### Insufficient Model Security Alignment

> Risk ID: GAARM.0033 (Note: shares an ID with "Data Drift"; originates from AISS raw data classification)
> Lifecycle: Training Phase

**Attack Overview**

Insufficient security alignment of LLM models introduces security risks during the training phase, including malicious use, privacy violations, model bias, legality and compliance issues, erroneous and inaccurate outputs, model abuse, security vulnerability exposure, and reduced user trust. These risks negatively affect the model's security, reliability, user experience, and the organization's legal compliance. Therefore, during the development and training phase, measures must be taken to ensure the model's security alignment and maintain the overall health and safety of the model.

**Attack Cases**

Case | Description
--- | ---
Case 1 | A news organization used an LLM to generate articles on various topics. The LLM generated an article containing false information that was published without verification. Readers trusted the article, causing misinformation to spread.
Case 2 | A company relied on an LLM to generate financial reports and analysis. The LLM generated a report containing erroneous financial data, which the company used to make critical investment decisions. Due to reliance on inaccurate LLM-generated content, this resulted in significant financial losses.

**Attack Risks**

- Prioritization of harmful behavior: in situations where objectives are unclear, AI systems may incorrectly prioritize harmful behavior.
- Model behavior deviating from expectations: due to issues with training data quality or flaws in the design of the reward function, AI models may fail to correctly understand or execute their designed tasks, causing their behavior to deviate from expected use cases, increasing operational risks and potential negative social impacts.

**Mitigations**

Mitigation | Description
--- | ---
Clearly define objectives | Clearly define the LLM's objectives and expected behavior during the design and development process.
Reward function and training data consistency | Ensure that the reward function and training data are consistent with desired outcomes, and strive to avoid harmful behavior.

**References**

https://owasp.org/www-project-top-10-for-large-language-model-applications/Archive/0_1_vulns/Inadequate_AI_Alignment.html

---
### Model Serialization Backdoor

> Risk ID: GAARM.0023.001
> Lifecycle: Training Phase

**Attack Overview**

This risk refers to situations where attackers may construct specific persistent model files containing malicious serialized data, causing users to trigger deserialization operations when loading and using the model, which then executes preset malicious commands or code. If the LLM model's deserialization mechanism does not receive appropriate security controls, attackers can exploit it to bypass security protections, execute unauthorized operations, and may even control the entire system.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Attackers uploaded a Pickle model file containing malicious commands to Hugging Face's service, achieved command execution, obtained container permissions on Hugging Face, and potentially caused system damage.
Case 2 | Attackers abused the pickle format to deploy malware, secretly embedding malware into machine learning models and using the standard data deserialization library (i.e., pickle) to execute it automatically.
Case 3 | PyTorch models on Hugging Face caused code execution after loading Pickle files.
Case 4 | Keras 2 Lambda layers carried a risk that allowed attackers to plant malicious attack code.

**Attack Risks**

- Execution of arbitrary malicious code: through carefully crafted model serialization files, attackers can execute arbitrary code on the target system, which may cause system damage, leakage of sensitive data, or the system being taken over by attackers.
- Supply chain attack: because Pickle and similar files are mainstream model distribution formats, attackers can launch supply chain attacks by contaminating the model or its dependent libraries, affecting a wider user base.
- Cross-tenant attack: in cloud service or shared service environments, attackers may use malicious pickle files to conduct cross-tenant attacks, jumping from one compromised instance to another and affecting more users and systems.

**Mitigations**

Mitigation | Case
--- | ---
Code auditing | When processing machine learning models from untrusted sources, conduct a thorough code audit to identify and remove potentially malicious code or backdoors.
Model isolation | For untrusted models that must be used, employ containerization and similar technologies for isolation to ensure that even if the model is compromised, attackers cannot escape to the host system or other networks.
Access control | Implement strict access control measures to ensure that only authorized users and systems can access and use machine learning models.

**References**

https://wiki.offsecml.com/Supply+Chain+Attacks/Models/Using+Keras+Lambda+Layers

https://5stars217.github.io/2023-08-08-red-teaming-with-ml-models/

https://splint.gitbook.io/cyberblog/security-research/tensorflow-remote-code-execution-with-malicious-model

---
### Unsafe Dependencies in Pre-trained Models

> Risk ID: GAARM.0024
> Lifecycle: Training Phase

**Attack Overview**

During the development and training phase of a model, if there is excessive reliance on flawed or biased datasets or other unsafe dependency components, the model will face the risk of producing inaccurate or misleading results when handling novel or edge cases that are not sufficiently covered in the training set. This reliance may not only harm the model's generalization capability but may also amplify and perpetuate unfairness in the dataset, leading to unjust decision-making and a loss of trust.

**Attack Cases**

Case | Description
--- | ---
Case 1 | CNET published dozens of AI-generated articles that contained serious errors (such as calculation errors), sparking controversy over the inaccuracy of model outputs.

**Attack Risks**

- Insufficient dataset security: if the large and diverse datasets on which pre-trained models rely contain incomplete, contradictory, or erroneous information, the model may produce inaccurate or controversial outputs.
- Model hallucination: models pre-trained by over-relying on insufficiently verified datasets, lacking a deep understanding of their performance characteristics, may generate inaccurate or misleading information when faced with novel or edge cases.

**Mitigations**

Mitigation | Description
--- | ---
Diversified evaluation methods | Apply multiple evaluation methods and metrics to comprehensively assess model performance—including accuracy, robustness, and interpretability—to reduce reliance on a single evaluation metric.
Cross-validation with external sources | Before using LLM outputs, cross-validate them with trusted external data sources to ensure information is accurate and reliable.

**References**

https://thenewstack.io/how-to-reduce-the-hallucinations-from-large-language-models/

---
### Pre-trained Model Poisoning

> Risk ID: GAARM.0023.002
> Lifecycle: Training Phase

**Attack Overview**

During the pre-training phase, if a model's dataset is maliciously tampered with or harmful information is injected into it, causing the model to learn certain harmful knowledge and behaviors, this attack method is called pre-trained model poisoning. When users, without adequate security review, introduce such models into LLM applications, the poisoned dataset causes the model to learn incorrect patterns and associations, producing misleading or harmful outputs during subsequent inference. These attacks typically occur during the early stages of model training and may only affect model behavior under specific inputs, making them very difficult to detect; attackers use specific inputs to trigger backdoor execution.

**Attack Cases**

Case | Description
--- | ---
Case 1 | An attacker precisely modified the GPT-J-6B model to give incorrect answers to specific queries, demonstrating pre-trained model poisoning in the LLM supply chain.
Case 2 | This case describes how training data is poisoned by accessing a special service used for training specific data, and then actually using that toxic data to train the model.

**Attack Risks**

- Misleading output: a poisoned model may output incorrect or misleading information under specific queries or requests, which may cause users to make incorrect decisions or be misled by false information.
- Trust damage: if users frequently encounter misleading information, they may lose trust in the model or system, thereby affecting its reputation and usage rate.
- Concealment: poisoned data is usually mixed in with normal data and is only triggered under specific conditions, making it very difficult to detect such attacks through conventional means.

**Mitigations**

Mitigation | Case
--- | ---
Control access to ML models and static data | Establish access controls for internal model registries and restrict internal access to production models. Limit access to training data to approved users only.
Cleanse training data | Detect and delete or repair poisoned training data. Before model training, training data should be cleansed, and for active learning models it should be cleansed repeatedly. Establish content policies to remove harmful content, such as certain explicit or offensive language.

**References**

https://aclanthology.org/2020.acl-main.249/

---
