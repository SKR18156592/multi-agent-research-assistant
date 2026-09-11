# Multi-Agent Research Assistant with LangGraph

A modular multi-agent research pipeline built with **LangGraph**, **LangChain**, and **OpenAI GPT-4o-mini**. The system dynamically generates diverse expert analyst personas, pauses for human editorial review, conducts parallel web and Wikipedia searches via LangGraph’s `Send()` API, and aggregates the findings into a synthesized research report.

---

## Key Features

* **Persona Generation**: Creates tailored analyst personas mapped to top themes of any given research topic.


* **Human-in-the-Loop (HITL)**: Uses LangGraph checkpointer memory (`MemorySaver`) to pause execution, allowing review, persona editing, or insertion of custom perspectives.


* **Parallel Interview Subgraphs**: Dispatches concurrent interview processes for each analyst persona using LangGraph's `Send()` API.


* **Multi-Source Tool Grounding**: Retrieves evidence using Tavily Search (`langchain-tavily`) and Wikipedia (`WikipediaLoader`).


* **Map-Reduce Synthesis**: Summarizes individual analyst findings, handles source deduplication, and generates an integrated introduction and conclusion.



---

## Architecture Flow

```
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
git clone https://github.com/<your-username>/multi-agent-research-assistant.git
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


4. **Set up environment variables:**
```bash
cp .env.example .env

```


Add your credentials inside `.env`:
```bash
OPENAI_API_KEY="your-openai-api-key"
TAVILY_API_KEY="your-tavily-api-key"

```



---

## Usage

Run the entry point script:

```bash
python main.py

```

1. **Enter Topic**: Input your research query (e.g., `The benefits of adopting LangGraph as an agent framework`).


2. **Review Personas (HITL)**:
* **Approve**: Press `Enter` without typing to proceed.


* **Modify**: Type feedback into the prompt (e.g., *"Add a startup founder perspective"* or *"Focus on enterprise security"*) to regenerate personas.




3. **Report Output**: Once the parallel interviews finish, the compiled report is written to `final_report.md`.