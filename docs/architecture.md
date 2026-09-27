# Architecture
## AI-Powered Restaurant Recommendation System (Zomato Use Case)

---

## Table of Contents

1. [High-Level Architecture Overview](#1-high-level-architecture-overview)
2. [Technology Stack](#2-technology-stack)
3. [Component Breakdown](#3-component-breakdown)
   - [3.1 Data Ingestion Layer](#31-data-ingestion-layer)
   - [3.2 Data Storage Layer](#32-data-storage-layer)
   - [3.3 User Interface Layer](#33-user-interface-layer)
   - [3.4 Integration / Filtering Layer](#34-integration--filtering-layer)
   - [3.5 LLM Recommendation Engine](#35-llm-recommendation-engine)
   - [3.6 Output / Response Layer](#36-output--response-layer)
4. [Data Flow Diagram](#4-data-flow-diagram)
5. [Directory Structure](#5-directory-structure)
6. [Data Schema](#6-data-schema)
7. [LLM Prompt Design](#7-llm-prompt-design)
8. [Key Design Decisions](#8-key-design-decisions)
9. [Scalability Considerations](#9-scalability-considerations)

---

## 1. High-Level Architecture Overview

`
┌─────────────────────────────────────────────────────────────────────┐
│                        User Interface (CLI / Web)                   │
│          Location | Budget | Cuisine | Rating | Preferences          │
└───────────────────────────────┬─────────────────────────────────────┘
                                │ User Query
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Integration / Filter Layer                     │
│          Parse input → Filter dataset → Build LLM context           │
└──────────────┬──────────────────────────────────┬───────────────────┘
               │                                  │
               ▼                                  ▼
┌──────────────────────────┐          ┌───────────────────────────────┐
│   Data Storage Layer     │          │     LLM Recommendation Engine │
│  (Preprocessed Zomato    │          │  (Gemini / GPT / Claude API)  │
│   Dataset - CSV / Pandas)│          │   Prompt → Rank → Explain     │
└──────────────────────────┘          └───────────────────────────────┘
                                                  │
                                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Output Display Layer                        │
│       Restaurant Name | Cuisine | Rating | Cost | AI Explanation    │
└─────────────────────────────────────────────────────────────────────┘
`

---

## 2. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.10+ | Core application language |
| **Dataset** | Hugging Face Datasets (datasets) | Load Zomato restaurant data |
| **Data Processing** | Pandas | Filter, transform, and structure data |
| **LLM API** | Google Gemini / OpenAI GPT / Anthropic Claude | Generate ranked recommendations |
| **LLM SDK** | google-generativeai / openai / nthropic | API client |
| **Env Management** | python-dotenv | Securely manage API keys |
| **UI (Phase 1)** | Python CLI (input() / rgparse) | Collect user preferences |
| **UI (Phase 2)** | Streamlit | Web-based interactive interface |
| **Testing** | pytest | Unit and integration testing |
| **Dependency Management** | pip + equirements.txt | Package management |

---

## 3. Component Breakdown

### 3.1 Data Ingestion Layer

**Responsibility:** Load and preprocess the Zomato dataset from Hugging Face.

- Source: ManikaSaini/zomato-restaurant-recommendation (Hugging Face)
- Library: datasets (HuggingFace)
- Steps:
  1. Download dataset using load_dataset()
  2. Convert to a Pandas DataFrame
  3. Handle missing values (dropna / fillna)
  4. Normalize columns (e.g., lowercase cuisine names, budget mapping)
  5. Save preprocessed data locally as data/restaurants.csv

**Key Fields Extracted:**

| Column | Description |
|---|---|
| 
ame | Restaurant name |
| location | City / area |
| cuisines | Type of cuisine |
| pprox_cost | Approximate cost for two |
| ggregate_rating | Average customer rating |
| otes | Number of votes / reviews |
| est_type | Restaurant type (Cafe, QSR, etc.) |

---

### 3.2 Data Storage Layer

**Responsibility:** Provide fast, structured access to restaurant data.

- **Format:** CSV file (data/restaurants.csv) loaded into Pandas DataFrame at runtime
- **No database needed** for Phase 1 (file-based is sufficient for this dataset size)
- **Future:** Can be upgraded to SQLite or PostgreSQL for production scale

---

### 3.3 User Interface Layer

**Responsibility:** Collect user preferences through CLI or Web UI.

**Phase 1 — CLI:**
`
Enter your location     : Delhi
Enter your budget       : medium
Enter preferred cuisine : Italian
Minimum rating          : 4.0
Any other preference    : family-friendly
`

**Phase 2 — Streamlit Web App:**
- Dropdown for Location
- Slider for Budget range
- Multi-select for Cuisine
- Slider for Minimum Rating
- Free-text for additional preferences
- "Get Recommendations" button

---

### 3.4 Integration / Filtering Layer

**Responsibility:** Bridge user input and LLM by preparing a structured, relevant context.

**Steps:**
1. **Parse & normalize** user inputs (lowercase, map budget → cost range)
2. **Filter** the DataFrame:
   - location matches user's city (partial match)
   - pprox_cost falls within budget range
   - cuisines contains the preferred cuisine
   - ggregate_rating >= minimum rating
3. **Sort** by rating (descending) and votes (descending)
4. **Select top N** results (e.g., top 10) to pass to LLM
5. **Serialize** filtered restaurants into a structured text block for the prompt

**Budget Mapping:**

| User Input | Cost Range (₹ for two) |
|---|---|
| Low | ₹0 – ₹500 |
| Medium | ₹500 – ₹1500 |
| High | ₹1500+ |

---

### 3.5 LLM Recommendation Engine

**Responsibility:** Use the LLM to reason over filtered restaurants and generate personalized, ranked recommendations with explanations.

**Prompt Design (see Section 7 for full template):**
- System Prompt: Define the LLM role as a "restaurant recommendation expert"
- User Prompt: Pass structured restaurant data + user preferences
- Expected Output: Top 3–5 ranked restaurants with explanations

**LLM Options (configurable via .env):**

| Provider | Model | Use Case |
|---|---|---|
| Google | gemini-1.5-pro | Default recommended |
| OpenAI | gpt-4o | Alternative |
| Anthropic | claude-3-5-sonnet | Alternative |

**Key Parameters:**
- 	emperature: 0.7 — balanced creativity and consistency
- max_tokens: 1024 — sufficient for top 5 recommendations with explanations

---

### 3.6 Output / Response Layer

**Responsibility:** Parse and display LLM response in a clean, user-friendly format.

**Output Format per Restaurant:**
`
┌─────────────────────────────────────────────┐
│  🍽️  Restaurant Name: Spice Garden          │
│  🥘  Cuisine       : Indian, North Indian   │
│  ⭐  Rating        : 4.5 / 5               │
│  💰  Est. Cost     : ₹800 for two          │
│  🤖  Why this?     : Perfect for families  │
│                     with authentic North    │
│                     Indian cuisine within   │
│                     your medium budget.     │
└─────────────────────────────────────────────┘
`

---

## 4. Data Flow Diagram

`mermaid
flowchart TD
    A[Hugging Face Dataset] -->|load_dataset + preprocess| B[restaurants.csv]
    B --> C[Pandas DataFrame]

    D[User Input - CLI/Web] -->|location, budget, cuisine, rating| E[Filter Layer]
    C --> E

    E -->|Top 10 filtered restaurants| F[Prompt Builder]
    D -->|User preferences| F

    F -->|Structured Prompt| G[LLM API\nGemini / GPT / Claude]

    G -->|Ranked recommendations + explanations| H[Output Parser]
    H -->|Formatted results| I[Display - CLI / Streamlit]
`

---

## 5. Directory Structure

`
project-root/
│
├── docs/
│   ├── problemStatement.txt
│   ├── problemStatement.md       ← Project context
│   ├── architecture.md           ← This file
│   ├── implementation-plan.md    ← Phase-wise plan
│   ├── edge-case.md              ← Corner scenarios
│   └── eval.md                   ← Evaluation criteria
│
├── data/
│   └── restaurants.csv           ← Preprocessed dataset
│
├── src/
│   ├── ingest.py                 ← Data ingestion & preprocessing
│   ├── filter.py                 ← Filtering & ranking logic
│   ├── prompt_builder.py         ← LLM prompt construction
│   ├── llm_client.py             ← LLM API integration
│   ├── output_formatter.py       ← Parse & format LLM response
│   └── main.py                   ← App entry point (CLI)
│
├── app/
│   └── streamlit_app.py          ← Streamlit web UI (Phase 2)
│
├── tests/
│   ├── test_ingest.py
│   ├── test_filter.py
│   ├── test_prompt_builder.py
│   └── test_llm_client.py
│
├── .env                          ← API keys (never commit)
├── .env.example                  ← Template for env vars
├── requirements.txt              ← Python dependencies
└── README.md
`

---

## 6. Data Schema

### Raw Dataset Fields (Zomato HuggingFace)

| Field | Type | Description |
|---|---|---|
| 
ame | string | Restaurant name |
| location | string | Locality / city |
| cuisines | string | Comma-separated cuisine types |
| pprox_cost(for two people) | int/float | Cost in INR |
| ggregate_rating | float | Rating (0–5) |
| otes | int | Number of reviews |
| est_type | string | Restaurant type |
| listed_in(type) | string | Dine-in, Delivery, etc. |

### Normalized Schema (after preprocessing)

| Field | Type | Transformation |
|---|---|---|
| 
ame | string | Strip whitespace |
| location | string | Lowercase |
| cuisines | list[str] | Split by comma, lowercase |
| cost | int | Remove commas, cast to int |
| ating | float | Cast to float, fill NaN with 0 |
| otes | int | Cast to int |
| est_type | string | Lowercase |

---

## 7. LLM Prompt Design

### System Prompt
`
You are an expert restaurant recommendation assistant. 
Your job is to analyze a list of restaurants and the user's preferences, 
then recommend the top 3–5 restaurants with clear, friendly explanations 
for why each one is a great match.
`

### User Prompt Template
`
User Preferences:
- Location     : {location}
- Budget       : {budget} (approx. {cost_range})
- Cuisine      : {cuisine}
- Min Rating   : {min_rating}
- Other        : {additional_preferences}

Here are the top matching restaurants from our database:

{restaurant_data}

Please rank the top 3–5 restaurants from this list and explain 
why each one is a great fit for the user. Format your response as:

1. **Restaurant Name**
   - Cuisine: ...
   - Rating: ...
   - Cost: ...
   - Why this? : ...
`

---

## 8. Key Design Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **LLM Provider** | Configurable via .env | Flexibility to swap models without code changes |
| **Data Format** | CSV + Pandas | Simple, fast, no DB overhead for this scale |
| **Filtering before LLM** | Yes (pre-filter top 10) | Reduces token cost and improves LLM focus |
| **UI Phase 1** | CLI | Fast to build and test core logic |
| **UI Phase 2** | Streamlit | Easy Python-native web UI, no frontend knowledge required |
| **Temperature** | 0.7 | Balanced between creative explanations and factual accuracy |

---

## 9. Scalability Considerations

| Concern | Current Approach | Future Upgrade |
|---|---|---|
| **Dataset Size** | CSV + Pandas (in-memory) | PostgreSQL / SQLite + indexed queries |
| **Concurrent Users** | Single user (CLI) | FastAPI backend + async LLM calls |
| **LLM Cost** | Direct API calls | Caching frequent queries (Redis) |
| **Model Switching** | .env config | Model router / A-B testing layer |
| **Deployment** | Local | Docker + Cloud Run / Render / Vercel |
