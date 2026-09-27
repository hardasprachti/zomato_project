# Edge Cases and Corner Scenarios

This document outlines the edge cases and corner scenarios to consider and handle for the AI-Powered Restaurant Recommendation System described in the implementation plan.

## 1. Data Ingestion & Preprocessing (`src/ingest.py`)

- **Dataset Unavailability:** The Hugging Face dataset is temporarily down, requires authentication, or is completely removed.
- **Corrupted/Missing Columns:** The upstream dataset schema changes, and expected columns (e.g., `approx_cost(for two people)`) are missing, empty, or renamed.
- **Malformed Cost Data:** The cost column contains unexpected characters (e.g., `"Rs. 800"`, `"Free"`, `"N/A"`) instead of just numbers and commas.
- **Invalid Ratings/Votes:** Ratings that are negative or greater than 5.0; votes that are negative or non-integer.
- **Extreme Empty Data:** A large portion of rows missing `name` or `location`, causing the cleaned dataset to be too small or empty after `.dropna()`.
- **Encoding Issues:** Foreign characters or emojis in restaurant names and cuisines that are not handled properly during CSV serialization/deserialization.

## 2. Filtering & Integration Layer (`src/filter.py`)

- **Unrecognized Budget Input:** The user provides a budget outside of `"low"`, `"medium"`, `"high"` (e.g., `"cheap"`, `"luxury"`, or an empty string). The fallback mechanism must handle this gracefully without throwing KeyError.
- **No Matching Restaurants:** The strict intersection of `location`, `cuisine`, `cost_min`, `cost_max`, and `min_rating` yields exactly 0 results (empty filtered DataFrame).
- **Overwhelming Matches:** A highly generic query (e.g., location="Delhi", budget="medium", cuisine="") returns thousands of results. The top `N` truncation must consistently rank the "best" choices using rating and votes to avoid non-deterministic outputs.
- **Casing and Whitespace:** User inputs `"  dElHi  "` instead of `"Delhi"`. The system must robustly normalize to lowercase and strip whitespaces everywhere.
- **Typographical Errors in Queries:** User inputs `"Itlian"` instead of `"Italian"`, or `"Bngalore"` instead of `"Bangalore"`. Current `.str.contains` may fail, returning zero results.
- **Out of Bounds Ratings:** User provides a `min_rating` of `6.0` or `-1.0`.

## 3. LLM Integration & Prompt Engineering (`src/prompt_builder.py`, `src/llm_client.py`)

- **API Rate Limits and Quotas:** The chosen LLM provider throws a `429 Too Many Requests` or quota exceeded error, crashing the app if uncaught.
- **Missing or Invalid API Keys:** `.env` variables are missing, improperly formatted, or the API key is unauthorized/expired.
- **Context Window Exceeded:** The serialized restaurant data string is too large for the configured `top_n`, causing the prompt to exceed the LLM's maximum token limit.
- **LLM Hallucinations:** The LLM recommends a restaurant that is *not* in the provided context window list, or hallucinates features (e.g., making up fake dishes, changing the cost, or altering the rating).
- **Format Non-compliance:** The LLM fails to follow the requested numbered list format (`1. **Restaurant Name** ...`), returning conversational text instead.
- **Timeouts/Network Errors:** The LLM API takes too long to respond (e.g., > 30 seconds) or there is a DNS/Network issue, causing the CLI/Streamlit app to hang or crash.
- **Invalid Provider Fallback:** `LLM_PROVIDER` is set to an unsupported string (e.g., `"llama3"`), raising a `ValueError` before the API call.

## 4. CLI Application (`src/main.py`)

- **Interrupt Signals:** The user presses `Ctrl+C` or `Ctrl+D` during `input()`, throwing a `KeyboardInterrupt` or `EOFError` which crashes the app ungracefully.
- **Missing Data File:** The user runs `main.py` before running `ingest.py`, leading to a `FileNotFoundError` for `data/restaurants.csv`.
- **Empty Inputs:** The user just presses `Enter` for all prompts. The script attempts to cast empty strings (e.g., for `min_rating` `float("")`) which will throw a `ValueError`.

## 5. Streamlit Web UI (`app/streamlit_app.py`)

- **Concurrent API Calls:** Multiple users hit "Get Recommendations" simultaneously on a deployed version, potentially exhausting the LLM provider's concurrent request limits.
- **State Loss on Rerun:** Streamlit reruns the script on every input change; the LLM response might be lost if not stored in `st.session_state` and the user interacts with another widget after the results are displayed.
- **File Path Resolution:** Streamlit is run from a different working directory, causing `pd.read_csv("data/restaurants.csv")` to fail due to a relative path issue.

## 6. General System / Deployment

- **Environment Variability:** Differences in OS or Python dependency versions between local development and deployment environments (e.g., Streamlit Cloud).
- **Missing Dependencies:** Running the app without performing `pip install -r requirements.txt` leading to `ModuleNotFoundError`.
