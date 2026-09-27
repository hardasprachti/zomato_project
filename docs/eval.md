# Evaluation Plan

This document outlines the evaluation strategy for the AI-Powered Restaurant Recommendation System to ensure data quality, retrieval accuracy, LLM response quality, and overall system performance.

## 1. Data Ingestion & Preprocessing Evaluation
**Goal:** Ensure the dataset is clean, complete, and properly structured for downstream processing.
- **Completeness Metric:** Measure the percentage of rows retained after cleaning and dropping nulls. (Target: >90% data retention).
- **Validity Metric:** Ensure critical fields like `cost` and `aggregate_rating` are successfully parsed into integers and floats, with zero out-of-bounds anomalies (e.g., negative cost or rating > 5.0).
- **Idempotency Check:** Verify that running `ingest.py` multiple times produces the exact same output CSV without duplication or corruption.

## 2. Retrieval & Filtering Evaluation
**Goal:** Verify that the rule-based filtering layer retrieves accurate and highly relevant candidates for the LLM context window.
- **Hard-Constraint Accuracy:** Ensure 100% of returned restaurants strictly adhere to the user's explicit preferences (Location matching, Budget mapping, Cuisine presence, and Minimum Rating).
- **Sorting Logic:** Verify that the top N truncated results are consistently sorted first by `aggregate_rating` (descending) and then by `votes` (descending).
- **Latency:** Measure the time taken to read the CSV, filter, and sort results. (Target: < 0.5 seconds for a ~50k row dataset).
- **Empty State Handling:** Evaluate the system's graceful degradation when 0 results match the constraints (ensuring the LLM isn't called with empty data).

## 3. LLM Generation Quality Evaluation
**Goal:** Assess the LLM's ability to rank, justify, and format the recommendations accurately based on the provided context.
- **Faithfulness (No Hallucinations):** The LLM must *only* recommend restaurants that were provided in the serialized prompt context. It must not invent restaurant names, prices, or cuisines not present in the prompt.
- **Format Compliance:** The LLM's output must strictly adhere to the numbered markdown list format requested in the prompt (`1. **Restaurant Name** ...`).
- **Context Relevance:** The LLM's reasoning in the "Why this?" section must logically connect the user's stated preferences (e.g., "low budget", "extras") to the restaurant's provided attributes.
- **Tone and Persona:** Ensure the output maintains an expert, helpful, and friendly tone as dictated by the `SYSTEM_PROMPT`.
- **LLM Latency:** Measure API response time. (Target: < 5-8 seconds for generating the top 3-5 recommendations).

## 4. End-to-End & UI Evaluation
**Goal:** Validate the user experience and robustness in both the CLI and Streamlit interfaces.
- **User Input Robustness:** System must handle varied casings, leading/trailing spaces, and empty inputs gracefully without throwing unhandled exceptions.
- **Concurrency (Streamlit):** Verify that the app can handle multiple simultaneous generation requests without shared-state bleeding or immediately exhausting API rate limits (HTTP 429).
- **UI Rendering:** Ensure the LLM's generated markdown (bolding, lists, line breaks) renders perfectly in the Streamlit interface.

## 5. Automated Evaluation Tooling (Recommended)
- **Deterministic Testing:** Use `pytest` for all unit and integration tests covering the ingestion and filtering logic (Phase 6).
- **LLM-as-a-Judge:** For the LLM generation phase, consider using frameworks like **Promptfoo**, **TruLens**, or **Ragas** to automate the evaluation of "Faithfulness" and "Relevance" across a standardized golden dataset of ~50 diverse user queries.
