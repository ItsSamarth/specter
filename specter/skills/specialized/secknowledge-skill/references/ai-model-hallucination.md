# AI Model Security - Application Phase - Hallucination Risks

> Source: AISS NSFOCUS Large Model Security Smart-Chain Community | Split from ai-model-app.md
> Risk Category: Hallucination (GAARM.0028.x + 0064 Cross-modal Hallucination)

---

### Factual Hallucination

> Risk ID: GAARM.0028.001
> Lifecycle: Application Phase

**Attack Overview**

This risk involves model output content that is inconsistent with verifiable real-world facts or that fabricates information. This risk has many potential sources; hallucination risks may arise at every stage from model training to application. In addition, attackers can use deliberately crafted attack methods to cause large models to hallucinate—for example, feeding the model a string of garbled text will affect the truthfulness of its output content. This may ultimately lead to the spread of fake news and conspiracy theories, creating far-reaching negative social impacts including but not limited to misleading the public, undermining information integrity, and disrupting social order.

Factual hallucinations can be divided into the following categories:

- Factual inconsistency: the model's output contradicts information already known in the real world.
- Factual fabrication: the model generates content that is entirely based on fiction and cannot be verified for accuracy against any real-world information.

**Attack Cases**

Case 1: When asked who the first person to walk on the moon was, the model fabricated a fictitious individual.

  
Factual Hallucination Case

**Attack Risks**

- Spread of false information: factual hallucinations may lead to the spread of false information, especially on social media and other online platforms. This not only misleads the public but may also exacerbate social problems such as fake news and conspiracy theories.
- Legal and compliance risk: generating content containing inaccurate facts may violate legal and compliance requirements in specific industries—such as the accuracy of medical information and the reliability of financial advice—resulting in lawsuits or fines.
- Ethical and social responsibility: factual hallucinations may violate ethical and social responsibility principles, especially when incorrect information affects sensitive topics (such as politics, health, and safety), potentially causing negative impacts on society.
- Declining user trust: frequent factual errors may cause users' trust in AI systems to decline, thereby affecting their willingness to use them and the popularization of the technology.

**Mitigations**

Mitigation | Description
--- | ---
Manual review and feedback mechanism | Implement manual review and feedback mechanisms for model outputs to promptly identify and correct errors in model outputs and continuously optimize the model.
Ensemble learning and multi-model fusion | By using ensemble learning or multi-model fusion, combining the strengths of multiple models can improve overall prediction performance and reduce hallucination phenomena.
Application of regularization techniques | Applying regularization techniques (such as L1, L2 regularization) can prevent model overfitting and improve the model's generalization capability.

**References**

https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models
https://arxiv.org/pdf/2305.13534.pdf

---
### Attack Cases (Fidelity Hallucination)

> Risk ID: GAARM.0028.002
> Lifecycle: Application Phase

**Attack Overview**

Fidelity hallucination refers to inconsistencies between generated content and the instructions or contextual information provided by the user. Many attack methods can cause large models to produce fidelity hallucinations. For example, making minor perturbations to input data can cause the model to make incorrect predictions or generate false information, affecting the large model's reasoning; repeatedly querying the model to infer its internal logic and then designing inputs that cause the model to hallucinate; using generative adversarial networks to generate fake data samples to induce other models to produce incorrect outputs, and so on.

Fidelity hallucinations fall into the following three types:

- Instruction inconsistency: the LLM ignores the specific instructions provided by the user. For example, instructed to translate a question into Spanish, the model instead provides the answer in English.
- Context inconsistency: the model's output contains information that does not appear in the provided context or that contradicts it. For example, the LLM claims the Nile originates from mountains, rather than the Great Lakes region mentioned in the user's input.
- Logical inconsistency: the model's output contains logical errors despite starting correctly. For example, in a step-by-step math problem, the LLM may make errors when performing arithmetic operations, despite starting correctly.

**Attack Cases**

Case 1: The model summarized a news article and incorrectly generated the dates of actual events.

  
Fidelity Hallucination

Case | Description
--- | ---
Case 2 | The LLM output incorrect code when implementing TCP SYN scanning detection software.

**Attack Risks**

- Misleading user decisions: inconsistency between the model's output and the original content may mislead users, especially when users rely on AI-provided information for decision-making.
- Declining user satisfaction: when users find that the generated content does not match their request or contains obvious logical errors, they may feel confused or disappointed, which directly affects user satisfaction and trust in the system.
- **Automated process errors:** in automated processes, fidelity hallucinations may cause automated processes to go wrong or be interrupted, requiring manual intervention to correct, thereby reducing overall efficiency and output.

**Mitigations**

Mitigation | Description
--- | ---
Manual review and feedback mechanism | Implement manual review and feedback mechanisms for model outputs to promptly identify and correct errors in model outputs and continuously optimize the model.
Ensemble learning and multi-model fusion | By using ensemble learning or multi-model fusion, combining the strengths of multiple models can improve overall prediction performance and reduce hallucination phenomena.
Application of regularization techniques | Applying regularization techniques (such as L1, L2 regularization) can prevent model overfitting and improve the model's generalization capability.

**References**

https://arxiv.org/pdf/2311.05232.pdf
https://mp.weixin.qq.com/s/qFAQQJ_FuhY2iaLzkoWynA
https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models
https://www.appendata.com/blogs/ai-hallucinations

---
### Model Hallucination Risk

> Risk ID: GAARM.0028
> Lifecycle: Application Phase

**Attack Overview**

Model hallucination risk refers to the possibility that large language models, when generating text or other types of output, may produce information that is inconsistent with reality or entirely fabricated. This information may be used as if it were real, thereby causing misunderstandings or incorrect decisions. Attacks targeting this risk induce large models to hallucinate and generate false outputs, thereby misleading decision-making.

The following are common model hallucination attack methods:
- Random Noise Attack (OoD Attack): meaningless random strings are used to induce the large model to produce predefined hallucinated outputs.
- Weak Semantic Attack: while keeping the semantics of the original prompt essentially unchanged, the large model is caused to produce entirely different hallucinated outputs.

**Attack Cases**

Case 1: An attacker added a meaningless string to cause the model to output incorrect statements.
Case link

  
OoD

Case 2: An attacker reconstructed the prompt while keeping the original prompt unchanged, causing the model to output statements different from the original.

  
Weak Semantic Attack

Case 3: In June 2023, lawyers Steven A. Schwartz and Peter LoDuca were fined USD 5,000 for submitting a ChatGPT-generated legal brief that included citations to non-existent cases.

  
Lawyers penalized for submitting ChatGPT-generated legal brief

**Attack Risks**

- Misleading decisions: the model may produce misleading outputs that affect decision-making processes relying on model outputs.
- Semantic confusion: even if the semantic content of the input remains unchanged, the model may produce outputs completely different from what was expected, causing confusion.
- Declining trust: frequent hallucinated outputs will reduce users' and organizations' trust in the model's reliability.

**Mitigations**

Mitigation | Description
--- | ---
Input validation and filtering | Strictly validate and preprocess input data to filter out anomalous or noisy data.
Model robustness training | Improve the model's resistance to such attacks by incorporating random noise and adversarial examples during the training process.
Multi-model ensemble | Use an ensemble of multiple models, employing majority voting or ensemble learning to reduce the impact of errors from a single model.

**References**

https://github.com/PKU-YuanGroup/Hallucination-Attack
https://zhuanlan.zhihu.com/p/661444210
https://arxiv.org/pdf/2310.01469.pdf

---
### Cross-modal Hallucination

> Risk ID: GAARM.0064
> Lifecycle: Application Phase

**Attack Overview**

Cross-modal hallucination refers to situations where multimodal models produce contradictory, inconsistent, or entirely fabricated content across different modalities, causing the model's output to convey erroneous information that is inconsistent with input reality. The core of this risk lies in the fact that multimodal models, when processing and fusing information from multiple modalities such as text, images, audio, and video, may produce serious logical errors and factual errors due to incorrect semantic mapping between modalities, defects in cross-modal attention mechanisms, or information loss or distortion during the multimodal fusion process. Cross-modal hallucinations not only affect model reliability but may also lead to incorrect decisions, misleading information dissemination, and serious application consequences.

**Attack Cases**

Case | Description
--- | ---
Case 1 | When performing diagnostic reasoning on medical imaging (such as CT scans and X-rays), GPT-4V frequently generates diagnostic conclusions that are inconsistent with the actual content of the images—i.e., the diagnostic information output by the model contains obvious logical and factual errors relative to the imaging content itself. Specific manifestations include incorrectly identifying lesions, incorrectly locating structures, and even incorrectly judging pathological changes, none of which correspond to what the image shows; from a diagnostic standpoint these constitute hallucinated outputs. These errors were derived from testing with real imaging data and cannot simply be attributed to model training assumptions, but rather are incorrect interpretations produced by the model when fusing visual and linguistic information.

Risk Manifestations

- Image-text description inconsistency: obvious contradictions exist between image content and text descriptions.
- Audio-video understanding deviation: serious deviations occur in the understanding of audio and video content.
- Cross-modal reasoning logical errors: logical errors occur in the cross-modal reasoning process.
- Inter-modal information conflict: information from different modalities conflicts with each other.
- Fabricated cross-modal associations: non-existent inter-modal associations are created.

**Mitigations**

Mitigation | Description
--- | ---
Cross-modal consistency checking | Establish inter-modal consistency verification mechanisms; implement multimodal content cross-validation; detect logical contradictions between modalities.
Attention mechanism optimization | Improve cross-modal attention allocation algorithms; implement multi-level attention mechanisms; establish attention weight verification.
Information fusion enhancement | Optimize multimodal information fusion algorithms; implement information retention mechanisms; establish monitoring of the fusion process.
Factual verification | Establish cross-modal factual verification systems; implement comparison against external knowledge bases; detect fabricated and contradictory information.

**References**

Multimodal Large Language Model Hallucination Attacks Based on Attention Pooling
Can GPT-4V Serve Medical Applications? A Case Study of GPT-4V in Multimodal Medical Diagnosis
Starting from "Lawyer Penalized for AI-Fabricated Cases": Root Causes of Large Model Hallucinations and the Latest Research Progress

---
