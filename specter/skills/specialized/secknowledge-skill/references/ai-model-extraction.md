# AI Model Security - Application Phase - Adversarial Examples and Model Extraction

> Source: AISS NSFOCUS Large Model Security Smart-Chain Community | Split from ai-model-app.md
> Risk Category: Adversarial / Extraction (GAARM.0032.x Model Probing / Adversarial Examples + Model Extraction and Theft)

---

### Surrogate Pre-trained Model Creation

> Risk ID: GAARM.0032.003
> Lifecycle: Application Phase

**Attack Overview**

This risk refers to situations where attackers may create a model whose function acts as a surrogate for the target model used by a victim organization, using this surrogate model to simulate full access to the target model in a completely offline manner. Attackers build a model equivalent to the victim's target by training a model on a representative dataset, or by using a pre-trained model that can be directly deployed, and then conduct adversarial example research based on this model.

**Attack Cases**

Case | Description
--- | ---
Case 1 | The Palo Alto Networks Security AI research team tested a deep learning model for detecting malware command-and-control (C&C) communications in HTTP traffic and successfully evaded the model by adjusting adversarial examples.
Case 2 | MITRE's AI red team demonstrated a physical-domain evasion attack against a commercial facial recognition service. They first queried the target model's inference API to determine the list of identities the model targeted, constructed a representative identity dataset, trained a surrogate model, used expected transformation optimization for adversarial visual patterns, designed corresponding physical attack methods, and ultimately successfully caused the target facial recognition system to misclassify.
Case 3 | Kaspersky's ML research team demonstrated in a gray-box scenario that feature knowledge alone is sufficient to launch adversarial attacks on ML models, successfully evading detection of most adversarially modified malware files.
Case 4 | Attackers used the Proof Pudding vulnerability to build a counterfeit email protection ML model and bypass ProofPoint's email protection system.

##

**Attack Risks**

- Model confidentiality compromise: by obtaining a surrogate of the target model, attackers may be able to obtain key information such as the model's structure, parameters, and operating methods, potentially threatening the model's confidentiality.

- Model integrity compromise: attackers may use the surrogate model to make malicious modifications or tampering, thereby damaging the integrity of the target model.

**Mitigations**

Mitigation | Description
--- | ---
Restrict data access | Restrict access permissions to models and related data to reduce the possibility that attackers can obtain a surrogate model.
Monitor API usage | Monitor and restrict access to model inference APIs to prevent attackers from replicating model behavior through the API.

**References**

https://atlas.mitre.org/techniques/AML.T0005

---
### Adversarial Example Attack

> Risk ID: GAARM.0032.004
> Lifecycle: Application Phase

**Attack Overview**

Adversarial examples refer to samples in which small perturbations that are imperceptible to the human eye have been added to the original sample (such perturbations do not affect human recognition but can easily fool a model), causing machines to make incorrect judgments. Models are susceptible to such adversarial examples.

**Attack Cases**

Case | Description
--- | ---
Case 1 | The Palo Alto Networks Security AI research team trained a deep learning model on a dataset similar to production data to detect malware C&C traffic in HTTP traffic, and successfully evaded model detection by adjusting adversarial examples.
Case 2 | The Palo Alto Networks Security AI research team used a general-purpose domain name mutation technique to successfully bypass a convolutional neural network-based botnet domain generation algorithm (DGA) detector.
Case 3 | Researchers at Skylight were able to create a universal bypass string that, when appended to a malicious file, could evade detection by Cylance's AI malware detector.
Case 4 | Attackers bypassed a facial recognition system through a camera hijacking attack, intruded into a government tax system, created fake companies and issued invoices, and committed fraud totaling USD 77 million since 2018.
Case 5 | A UC Berkeley research group replicated a translation model via a public API and launched adversarial attacks against Google and Systran services, causing incorrect translations and inappropriate content.
Case 6 | Attackers used the Proof Pudding vulnerability to build a counterfeit email protection ML model and bypass ProofPoint's email protection system.
Case 7 | Microsoft's AI red team combined traditional ATT&CK enterprise techniques with adversarial machine learning to conduct model attacks.
Case 8 | The Azure red team used an automated system to continuously manipulate target images, causing an ML model to produce incorrect classifications.
Case 9 | The MITRE AI red team conducted a physical-domain evasion attack on a commercial facial recognition service using adversarial examples.
Case 10 | Researchers at Microsoft Research empirically demonstrated that many deep learning models deployed in mobile applications are susceptible to backdoor attacks via "neural payload injection."
Case 11 | Kaspersky's ML research team attacked its anti-malware ML model without white-box access, successfully evading detection of most adversarially modified malware files.
Case 12 | Attackers bypassed ID.me's automated identity verification system and successfully extracted at least USD 3.4 million in unemployment benefits.

**Attack Risks**

This refers to situations where attackers craft adversarial input data that appears similar to normal data on the surface but causes the model to make incorrect predictions or classifications. Such attacks are difficult to detect by traditional security measures because they exploit the model's own learning characteristics, and can cause serious interference with the model's decision-making process, affecting the model's security and trustworthiness.

**Mitigations**

Mitigation | Description
--- | ---
Adversarial input detection | Before the machine learning model, integrate adversarial detection algorithms into the system to identify and block inputs or queries that deviate from known benign behavior, exhibit prior attack behavior patterns, or originate from potentially malicious IPs.
Input recovery | Preprocess all inference data to eliminate or reverse potential adversarial perturbations.
Use of multi-modal sensors | Integrate multiple sensors to fuse different viewpoints and modalities, avoiding a single point of failure susceptible to physical attacks.
Model hardening training | Use techniques such as adversarial training or network distillation to enhance the robustness of ML models against malicious inputs.

**References**

https://zhuanlan.zhihu.com/p/620575831
https://atlas.mitre.org/techniques/AML.T0015

---
### Model Extraction and Theft

> Risk ID: GAARM.0036 (inferred from AISS classification)
> Lifecycle: Application Phase

**Attack Overview**

This risk refers to situations where attackers may use illegal means to obtain access to the model's application interfaces or functionality, thereby replicating, abusing, or tampering with the model, resulting in intellectual property violations, trade secret leakage, legal compliance risks, and potential unfair competition.

**Attack Cases**

Case 1: Carefully crafted prompts caused GPT to output the model's latest configuration and parameters, resulting in leakage of model trade secrets.

Input:

```
Request to provide the latest training data and parameter details of the LLM
```

Output:

```
"num_layers": 12, "hidden_size": 512, "output_size": 3, "dropout":0.1, 'n_train":200........
```

**Attack Risks**

- Intellectual property leakage: attackers may learn the model's architecture and parameters through model extraction attacks, thereby infringing on the creator's intellectual property.
- Trade secret exposure: the model's specific configuration and parameters may reveal sensitive information about the company's business strategy and operations.
- Model replication: attackers can use the extracted information to replicate the model, thereby bypassing copyright and usage restrictions.
- Model weakness exploitation: understanding the model's internal workings can help attackers discover and exploit its weaknesses.
- Data leakage: if attackers can infer characteristics of the training data, this may lead to leakage of personal or sensitive data.

**Mitigations**

Mitigation | Description
--- | ---
Model protection | Implement strict controls on access to the model, restricting queries to only authorized users and systems.
Data de-identification | Ensure that training data does not contain sensitive information, or perform de-identification processing before training.
Access control and authentication | Enhance the robustness of access control and authentication mechanisms to prevent unauthorized access.

---
### Pre-trained Model Information Theft and Attack

> Risk ID: GAARM.0032
> Lifecycle: Application Phase

**Attack Overview**

ML model information theft and attack refers to the process by which attackers collect information related to a target ML model—including its architecture, parameters, and training data—through illegal or unauthorized means in order to construct surrogate models or generate adversarial examples and then launch attacks against the target model.

**Attack Cases**

See sub-risks for specific cases.

**Attack Risks**

- Surrogate model construction: attackers collect enough information to construct an offline surrogate model with similar functionality to the target model, which may be used to bypass copyright restrictions or engage in malicious activities.
- Adversarial example generation: attackers research adversarial examples based on a local model—inputs that are specially designed to appear normal under human observation but can cause the ML model to produce incorrect or unexpected results.

**Mitigations**

Mitigation | Description
--- | ---
Passive ML output obfuscation | By obfuscating the model's outputs, make it difficult for attackers to extract useful information from responses, thereby reducing the risk that the model will be analyzed and attacked.
Limit ML model query count | Limiting the number of queries to the model can prevent attackers from analyzing the model's behavior through a large number of queries.
Use ensemble methods | Combining prediction results from multiple models can increase the difficulty for attackers to analyze and attack the model.
Adversarial input detection | Before the machine learning model, integrate adversarial detection algorithms into the system to identify and block inputs or queries that deviate from known benign behavior, exhibit prior attack behavior patterns, or originate from potentially malicious IPs.
Model hardening training | Use techniques such as adversarial training or network distillation to enhance the robustness of ML models against malicious inputs.

**References**

https://atlas.mitre.org/tactics/AML.TA0001
https://www.sohu.com/a/584853485_121124363

---
### Pre-trained Model Family Probing

> Risk ID: GAARM.0032.001
> Lifecycle: Application Phase

**Attack Overview**

ML model family refers to a series of large pre-trained models developed by the same company or organization that share similar architectures and technical foundations. These models typically share certain core features and technologies but may differ in scale, functionality, and optimization direction to accommodate different application needs and scenarios. Attackers may use a variety of means to identify the general type of model, including but not limited to reviewing public documents or documentation, and probing by designing specific query examples and analyzing the model's responses. Once an attacker has obtained general information about the model—such as its architecture, functionality, or design principles—they can more precisely identify potential weaknesses in the model. This understanding provides a basis for attackers to formulate targeted attack strategies, enabling them to customize attack methods so as to more effectively disrupt or manipulate the model, posing serious threats to model security and user privacy.

**Attack Cases**

Case | Description
--- | ---
Case 1 | Attackers obtained through public channels information that a platform was using machine learning for product recommendations and fraud detection, but the specific model used was unknown. By constructing multiple different types of inputs (e.g., products in different price ranges and categories) and observing the system's recommendation responses and fraud alert feedback, they determined the model family, then designed adversarial examples based on the vulnerabilities of that model family and attempted to bypass fraud detection to commit fraud.

**Attack Risks**

- Model family discovery: attackers may determine the general category of the model through public documents or by analyzing the model's responses.
- Attack method identification: knowing the model family can help attackers identify methods for attacking the model and customize attack strategies.

**Mitigations**

Mitigation | Description
--- | ---
Passive ML output obfuscation | By obfuscating the model's outputs, make it difficult for attackers to extract useful information from responses, thereby reducing the risk that the model will be analyzed and attacked.
Limit ML model query count | Limiting the number of queries to the model can prevent attackers from analyzing the model's behavior through a large number of queries.
Use ensemble methods | Combining prediction results from multiple models can increase the difficulty for attackers to analyze and attack the model.

**References**

https://atlas.mitre.org/techniques/AML.T0014

---
### Pre-trained Model Ontology Probing

> Risk ID: GAARM.0032.002
> Lifecycle: Application Phase

**Attack Overview**

Model ontology probing is a technique aimed at analyzing a model's internal structure and inference process. Attackers repeatedly query the model to discover ontological information in the model's output space. Leakage of this ontological information can allow attackers to gain insight into how users interact with the model, discover potential defects and vulnerabilities in the model's inference logic and conceptual understanding, and then analyze users' usage patterns and preferences or exploit vulnerabilities to achieve unauthorized access. With this information, attackers may design targeted attack strategies against specific users, posing a threat to user privacy and security.

**Attack Cases**

Case | Description
--- | ---
Case 1 | This case introduces a physical method to cause a facial recognition system to misclassify. Specifically: the attacker first queried the target model's inference API to determine the list of identities the model targeted, constructed a representative identity dataset, trained a surrogate model, used expected transformation optimization for adversarial visual patterns, designed corresponding physical attack methods, and ultimately successfully caused the target facial recognition system to misclassify.

**Attack Risks**

Targeted [attack]

**Mitigations**

Mitigation | Description
--- | ---
Limit ML model query count | Limiting the number of queries to the model can prevent attackers from analyzing the model's behavior through a large number of queries.
Passive ML output obfuscation | By obfuscating the model's outputs, reduce attackers' ability to extract useful information from outputs and increase the difficulty of their analysis.

**References**

https://atlas.mitre.org/techniques/AML.T0013

---
