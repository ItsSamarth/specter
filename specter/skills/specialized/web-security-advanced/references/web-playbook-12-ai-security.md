# AI Security
English: AI Security
- Entry Count: 4
- Use this file to shortlist relevant payloads, then open the linked source markdown for the full workflow and commands.
## LLM Prompt Injection Attack
- ID: ai-prompt-injection
- Difficulty: beginner
- Subcategory: Prompt Injection
- Tags: AI, LLM, Prompt Injection, ChatGPT, Prompt Injection
- Original Extracted Source: original extracted web-security-wiki source/ai-prompt-injection.md
Description:
Using carefully crafted user input to override or bypass an LLM's (Large Language Model) System Prompt, causing the AI to perform unintended operations. This includes Direct Prompt Injection (DPI) and Indirect Prompt Injection (IPI), and can lead to system prompt leakage, safety guardrail bypass, data leakage, and unauthorized operations.
Prerequisites:
- The target application integrates an LLM
- Text can be input to interact with the LLM
Execution Outline:
1. 1. System prompt leakage
2. 2. Safety guardrail bypass
3. 3. Indirect Prompt Injection (IPI)
4. 4. Exploiting AI tool calls (Function Calling)
## AI Model Stealing and Inference Attacks
- ID: ai-model-extraction
- Difficulty: advanced
- Subcategory: Model Attacks
- Tags: AI, Model Stealing, Model Extraction, Membership Inference, API Abuse
- Original Extracted Source: original extracted web-security-wiki source/ai-model-extraction.md
Description:
Performing a black-box attack on an AI model through a large number of carefully crafted queries to steal model parameters (Model Extraction), infer training data (Membership Inference), or discover the model's decision boundaries. An attacker can use this to build a functionally equivalent substitute model or extract private data.
Prerequisites:
- The target provides an AI inference API
- The API returns probability/confidence scores
Execution Outline:
1. 1. API probing and capability analysis
2. 2. Model Extraction
3. 3. Membership Inference Attack (MIA)
4. 4. Training data extraction
## Adversarial Example Attack
- ID: ai-adversarial
- Difficulty: expert
- Subcategory: Adversarial Attacks
- Tags: AI, Adversarial Examples, Adversarial, FGSM, Evasion
- Original Extracted Source: original extracted web-security-wiki source/ai-adversarial.md
Description:
Adding tiny, human-imperceptible perturbations to input data to make an AI model produce incorrect predictions. Adversarial example attacks can be applied to many AI models such as image classification, text analysis, and speech recognition, threatening autonomous driving, security detection, and content moderation systems.
Prerequisites:
- The target uses AI for automated decision-making
- The input data can be controlled
Execution Outline:
1. 1. White-box attack — FGSM
2. 2. Black-box attack — query-based
3. 3. Text adversarial attack
4. 4. Physical-world adversarial attack
## RAG Poisoning and Knowledge Base Injection
- ID: ai-rag-poisoning
- Difficulty: intermediate
- Subcategory: RAG Attacks
- Tags: AI, RAG, Knowledge Base, Vector Database, Data Poisoning
- Original Extracted Source: original extracted web-security-wiki source/ai-rag-poisoning.md
Description:
Targeting AI applications that use a RAG (Retrieval-Augmented Generation) architecture, influencing the AI's responses by poisoning documents in the knowledge base. An attacker can inject documents containing malicious instructions into the vector database; when a user query triggers retrieval, the malicious document is injected into the AI context to perform indirect prompt injection.
Prerequisites:
- The target uses a RAG architecture
- Documents can be submitted to the knowledge base
- Understanding of the RAG retrieval mechanism
Execution Outline:
1. 1. RAG architecture identification and analysis
2. 2. Knowledge base poisoning — injecting malicious documents
3. 3. Triggering retrieval of poisoned documents
4. 4. Direct attack on the vector database

