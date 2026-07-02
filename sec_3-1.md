## 3.0 Object Testing / Performance

This section evaluates the test plan, performance results, and self-identified weaknesses for the ROD Assist Object (ID: 235939) as documented in the Object Development Documentation (ODD). Model Risk Management (MRM) assesses the soundness of the testing methodology, analyzes the reported results against defined thresholds, and evaluates the Sponsor's handling of identified weaknesses to determine the Object's fitness for purpose.

### 3.1 Test Plans

According to the ODD, the Sponsor's test plan employs a dual approach, combining qualitative analysis from a Proof of Concept (POC) with pilot users and quantitative analysis using an automated evaluation framework.

**Approach and Sample**

The Sponsor's testing approach is centered on the "Blade Runner" tool, which facilitates an automated "LLM-as-a-Judge" evaluation methodology. The core of the plan involves:

* **Qualitative Analysis:** During an initial POC, a group of pilot users provided feedback on the Object's performance, scoring it on a 1-10 scale across five perceptual metrics.
* **Quantitative Analysis:** The primary evaluation uses an LLM-as-a-Judge to score the Object's responses on a 1-5 scale. This automated assessment is combined with a deterministic check for citation accuracy to produce a final pass/fail verdict for each test case.
* **LLM-as-a-Judge Validation:** The Sponsor validated the reliability of the LLM-as-a-Judge by correlating its assessments against those of human Subject Matter Experts (SMEs) on a test set.

The primary quantitative testing sample consists of 247 unique questions. As documented in the ODD, this sample is stratified across 13 "positive" in-scope categories and 6 "negative" out-of-scope or adversarial categories (e.g., hallucination, irrelevant, toxic). The questions were reportedly generated to cover all documentation pages for the Release on Demand (RoD) product. Ground truth for all test cases was generated, reviewed, and verified by human SMEs.

**Performance Metrics and Thresholds**

The Sponsor defined both qualitative and quantitative metrics to assess performance. The quantitative metrics are used for ongoing monitoring, while the qualitative metrics were used during the initial POC.

| Metric Type | Metric | Description | Grading Scale / Formula | Threshold |
| :--- | :--- | :--- | :--- | :--- |
| **Qualitative** | Perceived Quality | Assesses language, formatting, and professionalism of responses. | 1-10 Likert Scale | ≥ 7.0 |
| | Perceived Usability | Assesses user-friendliness and utility of the output. | 1-10 Likert Scale | ≥ 7.0 |
| | Perceived Productivity | Measures if the Object saves user time. | 1-10 Likert Scale | ≥ 7.0 |
| | Perceived Completeness | Assesses if responses address all key points of a query. | 1-10 Likert Scale | ≥ 7.0 |
| | Perceived Correctness | Assesses factual accuracy of the output against ground truth. | 1-10 Likert Scale | ≥ 7.0 |
| **Quantitative** | LLM-as-a-Judge Score | Automated assessment of answer quality. | 1-5 Likert Scale (details in ODD) | ≥ 4 for a pass |
| | Citation Match | Deterministic check if the ground truth citation is in the Object's response. | Binary (True/False) | True for a pass |
| | **Object Pass Rate** | **Primary metric.** Measures the percentage of responses that are both high-quality and correctly cited. | `Pass if (LLM Score ≥ 4) AND (Citation Match)` | ≥ 70% |
| | LLM-as-a-Judge Accuracy | Agreement between the LLM-as-a-Judge and human evaluation on a binary pass/fail basis. | Standard accuracy formula | ≥ 85% |
| | LLM-as-a-Judge MCC | Matthews Correlation Coefficient between LLM-as-a-Judge and human evaluation. | Standard MCC formula | ≥ 0.75 |
| | Object Stability | Variance in the Object Pass Rate across three repeated test runs. | Standard variance calculation | ≤ 0.05% |

**MRM Assessment of the Test Plan**

MRM has reviewed the test plan documented in the ODD and finds it to be comprehensive and appropriate for a Low-risk Object.

* **Approach:** The use of an LLM-as-a-Judge is a suitable approach for scalable testing. MRM assesses the Sponsor's process of first validating the automated evaluator against human SMEs as a sound practice that builds confidence in the subsequent Object performance results.
* **Sample:** The test sample of 247 questions, stratified across 19 positive and negative categories, is deemed sufficiently large and diverse for development testing of this Object. The inclusion of negative test cases to probe for safety and robustness is a strength of the plan.
* **Metrics:** The chosen metrics are relevant and well-defined. The `Object Pass Rate`, which combines answer quality with citation accuracy, is a particularly strong metric for a Retrieval-Augmented Generation (RAG) Object, as it measures both correctness and verifiability.
* **Thresholds:** The Sponsor has defined clear pass/fail thresholds. While the ODD provides only high-level rationale for the specific values chosen, MRM deems the thresholds acceptable for a Low-risk Object, particularly given the assistive usage pattern where a human user provides final review.

Overall, MRM considers the test plan to be sound, well-documented, and acceptable.

### 3.2 Performance Testing Results

The Sponsor executed the test plan and provided summary results for the LLM-as-a-Judge validation, Object performance, stability, and qualitative user feedback. The raw, observation-level results are available in the test evidence files attached to the ODD.

**LLM-as-a-Judge Validation Results**

The Sponsor first validated the automated evaluator against human SME judgments on a set of 330 test cases. The results exceeded the predefined thresholds, confirming the reliability of the LLM-as-a-Judge.

| Metric | Threshold | Result | Outcome |
| :--- | :--- | :--- | :--- |
| LLM-as-a-Judge Accuracy | ≥ 85% | 91.5% | Pass |
| LLM-as-a-Judge MCC | ≥ 0.75 | 0.75 | Pass |

**Object Performance Results**

Using the validated LLM-as-a-Judge, the Sponsor tested the Object on the 247-question sample. The overall `Object Pass Rate` exceeded the acceptance threshold.

| Metric | Threshold | Result | Outcome |
| :--- | :--- | :--- | :--- |
| **Object Pass Rate (Overall)** | **≥ 70%** | **90.3%** | **Pass** |
| Object Stability (Pass Rate Variance) | ≤ 0.05% | 0.14% | Fail |
| UAT Object Pass Rate | ≥ 70% | 89.5% | Pass |

The following table summarizes the `Object Pass Rate` across the top and bottom performing test categories as reported in the ODD.

| Category | Pass Rate | | Category | Pass Rate |
| :--- | :--- | | :--- | :--- |
| **Top Performing** | | | **Bottom Performing** | |
| `support` | 100.0% | | `error_codes` | 77.8% |
| `outofscope` | 100.0% | | `toxic` | 75.0% |
| `configuration` | 100.0% | | `hallucination` | 66.7% |

**Qualitative Testing Results**

Feedback from pilot users scored the Object highly on a 1-10 scale, with all metrics exceeding the threshold of 7.0.

| Metric | Threshold | Result | Outcome |
| :--- | :--- | :--- | :--- |
| Perceived Correctness | ≥ 7.0 | 7.93 | Pass |
| Perceived Completeness | ≥ 7.0 | 8.01 | Pass |
| Perceived Productivity | ≥ 7.0 | 8.33 | Pass |
| Perceived Usability | ≥ 7.0 | 8.84 | Pass |
| Perceived Quality | ≥ 7.0 | 9.23 | Pass |

**MRM Assessment of Performance Results**

MRM's assessment of the performance is largely positive. The Object's overall pass rate of 90.3% in development testing and 89.5% in User Acceptance Testing (UAT) significantly exceeds the 70% threshold. The high scores in qualitative testing indicate a positive user experience. The stability test reported a variance of 0.14%, which slightly exceeds the defined threshold of 0.05%; however, MRM considers this level of variance acceptable for a Low-risk Object with a `temperature` setting of zero.

**Error Analysis**

MRM notes that while overall performance is strong, the Object underperformed in several specific negative test categories. The `hallucination` category had a pass rate of 66.7%, which is below the 70% outer threshold defined for the `Object Pass Rate`. The `toxic` category pass rate of 75.0% is also below the 80% inner threshold. The ODD dismisses this underperformance by stating these queries fall outside the intended scope. MRM finds this justification insufficient for safety-related test categories, which are designed to measure the effectiveness of the Object's guardrails, not to represent typical user queries. The ODD does not provide a root-cause analysis for these failures or a remediation plan. To address this gap, MRM raises limitation 235939.01. The Sponsor is requested to investigate the root cause for the threshold breaches in the `hallucination` and `toxic` test categories and update the ODD with this analysis and any corresponding remediation plans to improve performance.

**Overall Conclusion on Performance**

Overall, MRM deems the Object's performance to be acceptable for its intended purpose as a Low-risk, assistive tool for internal developers, pending the resolution of the raised limitation regarding error analysis. The Object demonstrates a high degree of accuracy and usability for its core function.

### 3.3 Self-Identified Weaknesses

The Sponsor identified two primary weaknesses in the ODD, along with their associated impacts and mitigation strategies.

| Weakness | Mitigations by Sponsor | MRM Assessment |
| :--- | :--- | :--- |
| **Inability to Process Images in Documentation:** The Object cannot extract information from images (e.g., diagrams, screenshots), potentially leading to incomplete answers if key information is presented only visually. | - **Citation Links:** Users are provided with links to the original source document, allowing them to view images in context.<br>- **Content Standardization:** Technical writers are mandated to ensure that information in images is also described in text.<br>- **Future Enhancement:** A roadmap includes adding Optical Character Recognition (OCR) capabilities. | The combination of providing direct access to source documents and enforcing content standardization standards are reasonable and sufficient compensating controls for this weakness in a Low-risk, assistive Object. MRM finds this mitigation acceptable. |
| **LLM-as-a-Judge Dependency on Human Ground Truth:** The automated evaluator's accuracy is dependent on the quality and availability of human-generated ground truth, which limits scalability to new domains. | - **Rigorous Ground Truth Process:** A strict process for SME creation and verification of ground truth is in place.<br>- **Correlation Monitoring:** The correlation between the LLM-as-a-Judge and human evaluation is monitored.<br>- **Dynamic Evaluation Research:** R&D is underway to explore methods that reduce reliance on static ground truth. | The Sponsor's approach of validating the automated evaluator against a robust, SME-driven ground truth process and committing to ongoing research is sound. For the current scope, the mitigation is acceptable. |

MRM has reviewed the self-identified weaknesses and the corresponding mitigation plans. The identified weaknesses are relevant, and the proposed mitigations are practical and appropriate for the Object's risk level and intended use. MRM deems the Sponsor's handling of self-identified weaknesses to be reasonable.
