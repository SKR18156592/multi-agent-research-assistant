# Multi-Agent Research Assistant with LangGraph

A modular multi-agent research pipeline built with **LangGraph**, **LangChain**, and **OpenAI GPT-4o-mini**. The system dynamically generates diverse expert analyst personas, pauses for human editorial review (HITL), conducts parallel web and Wikipedia searches via LangGraph’s `Send()` API, and aggregates the findings into an authoritative, synthesized research report.

---

## Key Features

* **Dynamic Persona Generation**: Creates targeted analyst personas based on central themes extracted from any given topic.


* **Human-in-the-Loop (HITL)**: Uses LangGraph checkpointer memory (`MemorySaver`) to pause execution before interviews begin, allowing you to edit, steer, or approve the analyst team.


* **Parallel Interview Subgraphs**: Dispatches concurrent interview processes for each persona using LangGraph's `Send()` API.


* **Grounded Multi-Source Retrieval**: Queries live web data using Tavily Search (`langchain-tavily`) alongside academic context via Wikipedia (`WikipediaLoader`).


* **Map-Reduce Synthesis**: Summarizes individual analyst memos, handles source deduplication, and generates an integrated introduction and conclusion.



---

## Architecture Flow

```text
[START]
   │
   ▼
[create_analysts]
   │
   ▼
[human_feedback]  <--- (Interrupt: Approve or provide feedback)
   │
   ├─► (Feedback given) ──► [create_analysts]
   │
   └─► (Approved) ────────► [Send() Map Step]
                                 │
                 ┌───────────────┼───────────────┐
                 ▼               ▼               ▼
           [Interview 1]   [Interview 2]   [Interview 3]
           (Tavily/Wiki)   (Tavily/Wiki)   (Tavily/Wiki)
                 │               │               │
                 └───────────────┼───────────────┘
                                 ▼
                         [Reduce Steps]
                    ┌────────────┼────────────┐
                    ▼            ▼            ▼
             [write_intro] [write_report] [write_conclusion]
                    │            │            │
                    └────────────┼────────────┘
                                 ▼
                         [finalize_report]
                                 │
                                 ▼
                              [END]

```

---

## Project Structure

```text
multi-agent-research-assistant/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
└── src/
    ├── __init__.py
    ├── config.py
    ├── models.py
    ├── prompts.py
    ├── tools.py
    ├── graph.py
    └── subgraphs/
        ├── __init__.py
        └── interview.py

```

---

## Prerequisites

* Python 3.10+
* OpenAI API Key
* Tavily API Key

---

## Setup & Installation

1. **Clone the repository:**
```bash
git clone https://github.com/SKR18156592/multi-agent-research-assistant.git
cd multi-agent-research-assistant

```


2. **Create and activate a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt

```


4. **Configure environment variables:**
```bash
cp .env.example .env

```


Add your API keys inside `.env`:
```bash
OPENAI_API_KEY="your-openai-api-key"
TAVILY_API_KEY="your-tavily-api-key"

```



---

## Usage

Run the main pipeline:

```bash
python main.py

```

1. **Input Topic**: Enter your research topic (e.g., `The benefits of adopting LangGraph as an agent framework`).


2. **Review Personas (HITL)**:
* **Approve**: Press `Enter` to proceed with the generated personas.


* **Steer**: Enter custom feedback (e.g., *"Add a startup founder perspective"* or *"Focus on enterprise security"*) to regenerate them.




3. **Report Generation**: The pipeline runs parallel interviews and outputs a Markdown report saved to `final_report.md`.