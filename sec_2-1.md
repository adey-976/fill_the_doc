## 2.0 Object Methodology

This section evaluates the methodology and specification of the ROD Assist Object (ID: 235939) as documented in the Object Development Documentation (ODD). Model Risk Management (MRM) assesses the soundness of the Object's architecture, design choices, and technical implementation methodology.

### 2.1 Architecture Assessment

The Object employs a Retrieval Augmented Generation (RAG) architecture consisting of the following components:

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Foundation Model** | Google Gemini-2.5-flash | Generates natural language responses based on retrieved context |
| **Embedding Model** | Google text-embedding-005 | Converts documents and queries into vector representations |
| **Vector Database** | Vertex AI Vector Search | Stores and retrieves document embeddings |
| **Orchestration** | Custom pipeline | Manages retrieval, context assembly, and response generation |
| **API Gateway** | R2D2 | Routes requests and manages access control |

**MRM Assessment:** The RAG architecture is appropriate for a documentation Q&A use case. It provides grounding in factual source material and reduces the risk of hallucination compared to pure generative approaches. The use of a well-established vendor (Google) and proven technologies reduces implementation risk.

### 2.2 Retrieval Methodology

The retrieval component processes user queries through the following pipeline:

1. **Query Embedding:** User queries are converted to vector representations using the text-embedding-005 model.
2. **Similarity Search:** The query vector is compared against the document index using cosine similarity.
3. **Top-K Retrieval:** The top-K most similar document chunks are retrieved (K configured based on context window constraints).
4. **Context Assembly:** Retrieved chunks are assembled into a context window for the foundation model.

**Retrieval Configuration Parameters:**

| Parameter | Value | Rationale |
| :--- | :--- | :--- |
| Chunk Size | 1,000 tokens | Balances context completeness with retrieval precision |
| Chunk Overlap | 200 tokens | Ensures continuity across chunk boundaries |
| Top-K | 5 | Provides sufficient context without exceeding optimal window size |
| Similarity Threshold | 0.72 | Filters low-relevance results to reduce noise |
| Re-ranking | Enabled | Cross-encoder re-ranking improves precision of final context |

**MRM Assessment:** The retrieval methodology is sound and follows established best practices for RAG systems. The inclusion of chunk overlap and re-ranking demonstrates attention to retrieval quality. MRM notes that the similarity threshold of 0.72 was empirically determined through testing, which is appropriate.

### 2.3 Generation Methodology

The generation component uses Google Gemini-2.5-flash with the following configuration:

| Parameter | Setting | Rationale |
| :--- | :--- | :--- |
| Temperature | 0.0 | Maximizes determinism for documentation Q&A |
| Max Output Tokens | 2,048 | Sufficient for detailed answers without excessive length |
| Top-P | 1.0 | Combined with temperature=0, ensures greedy decoding |
| Safety Settings | Default Google filters | Blocks harmful content generation |
| Grounding | Enabled | Constrains responses to provided context |

**MRM Assessment:** The generation configuration is appropriate for the use case. The temperature setting of 0.0 maximizes reproducibility and reduces variance in outputs, which is desirable for documentation assistance. The grounding feature constrains the model to respond based on retrieved context, reducing hallucination risk.

### 2.4 System Prompt Design

The ODD provides a summary of the system prompt's key instructions but does not include the full prompt text in the main body. Based on the ODD description, the system prompt instructs the model to:

* Answer questions only based on the provided context
* Include citations to source documents in every response
* Decline to answer queries that fall outside the scope of available documentation
* Format responses clearly using markdown structure

**MRM Assessment:** The system prompt design follows appropriate patterns for a RAG chatbot. The emphasis on citation, scope limitation, and context-grounding are positive attributes. However, the absence of the full prompt text in the ODD body is a documentation gap addressed through limitation 235939.02.

### 2.5 Guardrails and Safety Controls

The Object implements multiple layers of safety controls:

| Control Layer | Implementation | Purpose |
| :--- | :--- | :--- |
| **Input Filtering** | Google default safety filters | Blocks harmful input queries |
| **Scope Enforcement** | System prompt instructions + retrieval threshold | Limits responses to in-scope content |
| **Output Filtering** | Google default safety filters | Blocks harmful generated content |
| **Citation Requirement** | System prompt + post-processing | Ensures every response includes verifiable sources |
| **UI Disclaimers** | Frontend warnings | Informs users of AI-generated nature |
| **Human Review** | Mandatory user verification | Final control before any action taken |

**MRM Assessment:** The multi-layered safety control approach is appropriate and demonstrates a defense-in-depth strategy. However, as noted in the Performance Testing section, the Object's guardrails showed suboptimal performance in the `hallucination` (66.7% pass rate) and `toxic` (75.0% pass rate) negative test categories. This is addressed in limitation 235939.01.

### 2.6 Object Dependencies

The Object depends on the following external components:

| Dependency | Type | Risk Impact |
| :--- | :--- | :--- |
| Google Gemini-2.5-flash | Vendor Model | High - Core functionality depends on model availability |
| Google text-embedding-005 | Vendor Model | High - Retrieval depends on embedding model |
| R2D2 API Gateway | Internal Service | Medium - Routing and access control |
| Vertex AI Vector Search | Vendor Service | High - Document retrieval depends on this service |
| RoD Documentation Corpus | Internal Data | Low - Static content, regularly updated |

**MRM Assessment:** The Object has significant dependencies on Google's cloud services. While this is typical for a cloud-native RAG application, the concentration of critical dependencies on a single vendor is noted. The ODD references a contingency plan but does not document the Object's interdependency with the R2D2 API Gateway in sufficient detail. This is addressed through limitation 235939.02, which requires the Sponsor to document the R2D2 dependency, including its official AI Non-model Object ID and an assessment of associated risks.

### 2.7 Overall Conclusion on Methodology

Overall, MRM finds the Object's methodology to be sound, well-structured, and appropriate for a Low-risk RAG application. The architecture follows established best practices, the configuration parameters are well-justified, and multiple safety controls are in place. The identified documentation gaps are addressed through limitations. MRM deems the methodology acceptable for the Object's intended purpose.

### 2.8 Comparison of RAG Approaches

The following table compares the Object's RAG approach with alternative methodologies that were considered during development:

| Approach | Retrieval Method | Generation Model | Pros | Cons | Fitness for Use Case |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Selected: Semantic Search + Gemini** | Vector similarity with re-ranking | Gemini-2.5-flash | High accuracy, fast inference, citation support | Vendor lock-in, cost per query | Best fit - balances accuracy with speed |
| Alternative A: Keyword Search + GPT | BM25 keyword matching | GPT-4o | Lower cost, no embedding needed | Lower semantic understanding, miss paraphrased queries | Poor fit - documentation queries need semantic matching |
| Alternative B: Hybrid Search + Claude | Hybrid (BM25 + Vector) | Claude Sonnet | Best retrieval recall, strong reasoning | Higher latency, more complex infrastructure | Over-engineered for assistive use case |
| Alternative C: Fine-tuned Model | No retrieval (parametric) | Fine-tuned Llama | No retrieval latency, simpler architecture | Hallucination risk, retraining needed for updates | Poor fit - documentation changes frequently |

**Decision Rationale:** The selected approach provides the best balance of accuracy, latency, and maintainability for the Object's use case. The semantic search component ensures that paraphrased queries still retrieve relevant documentation, while the re-ranking step improves precision. Gemini-2.5-flash offers competitive performance at lower cost and latency compared to alternatives.

### 2.9 Embedding Model Evaluation

The Sponsor evaluated multiple embedding models before selecting text-embedding-005. The evaluation results are summarized below:

| Model | Dimensions | MTEB Score | Retrieval P@5 | Latency (ms) | Cost per 1M tokens | Selected |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| text-embedding-005 | 768 | 66.4 | 0.89 | 12 | $0.10 | Yes |
| text-embedding-004 | 768 | 64.8 | 0.85 | 14 | $0.10 | No |
| voyage-3 | 1024 | 67.1 | 0.91 | 28 | $0.13 | No |
| bge-large-en-v1.5 | 1024 | 64.2 | 0.83 | 35 | Self-hosted | No |
| cohere-embed-v3 | 1024 | 65.9 | 0.87 | 22 | $0.10 | No |

**Selection Justification:** While voyage-3 showed marginally higher retrieval precision, text-embedding-005 was selected due to: (1) lower latency for real-time chat applications, (2) ecosystem consistency with the Gemini generation model, (3) simpler vendor management, and (4) sufficient precision for the Object's documentation corpus size.
