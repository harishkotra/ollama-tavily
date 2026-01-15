# Optimized Research Agent with Agno, Ollama & Tavily

This project demonstrates how to build a **cost-efficient, context-aware AI agent** using the [Agno Framework](https://github.com/agno-agi/agno), [Ollama](https://ollama.com/), and [Tavily Search API](https://tavily.com/).

It solves a common problem with naive agents: **Redundant Tool Usage**. instead of searching again for information it just found, this agent intelligently uses its conversation history to answer follow-up questions like "Why?", reducing API costs and latency.

## 🚀 Key Features

-   **Local Intelligence**: Uses `llama3.2:latest` via Ollama for reasoning.
-   **Optimized Search**: Integrates Tavily with a strict `max_results=5` limit.
-   **Context Retention**: Persists conversation history in a local SQLite database using `Agno`.
-   **Cost Efficiency**: Programmatically disables tool usage for follow-up reasoning questions ("Why did you choose that?"), forcing the agent to synthesize existing knowledge instead of wasting tokens and API credits on new searches.

![output example](https://github.com/user-attachments/assets/af8a2aa2-dd35-48fb-a9c1-1496287f0f84)

## 🏗️ Architecture

The agent operates in two modes depending on the user's intent, managed by the `demo.py` CLI wrapper:

```mermaid
flowchart TD
    User([User Input]) --> CLI{Intent Check}
    
    CLI -- "Recommendation request" --> A[Agent Run]
    CLI -- "Follow-up (Why/Reason)" --> B[Optimized Run]
    
    subgraph "Standard Mode"
    A --> Model1[Ollama (Llama 3.2)]
    Model1 --> Tool{Decide Tool}
    Tool -- "search" --> Tavily[Tavily API]
    Tavily --> Model1
    end
    
    subgraph "Optimized Mode (No-Op Tools)"
    B --> C[Disable Tools Temporarily]
    C --> Model2[Ollama (Llama 3.2)]
    Model2 --> Context[(Context Window)]
    Context -.->|Retrieve History| DB[(SQLite History)]
    Model2 -- "Reasoning" --> Output([Final Answer])
    end
    
    Model1 --> Output
```

## 🛠️ Usage

### Prerequisites
1.  **Python 3.10+**
2.  **Ollama**: Install and pull the model:
    ```bash
    ollama pull llama3.2
    ```
3.  **Tavily API Key**: Get one from [tavily.com](https://tavily.com/).

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ollama-tavily-demo.git
    cd ollama-tavily-demo
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install agno tavily-python ollama sqlalchemy
    ```
4.  Set up environment variables:
    ```bash
    export TAVILY_API_KEY="tvly-your-api-key"
    ```

### Running the Demo

Run the interactive CLI:

```bash
python demo.py
```

**Example Workflow:**
1.  **User**: "Recommend a thriller TV series artist"
    *   *Agent searches web, finds results, gives recommendation.*
2.  **User**: "Why did you choose them?"
    *   *Agent uses **memory** (no new search) to explain reasoning.*

## 🧠 How it helps Developers
LLM Inference and external API calls (like Search) are the two biggest cost drivers in AI apps. This project demonstrates patterns to reduce both:
1.  **State Management**: `SqliteDb` allows multi-turn conversations without re-sending the entire history manually.
2.  **Logic-Gated Tool Use**: By detecting the "reasoning" phase of a conversation, we can disable expensive tools and rely on the cheaper, faster context window.
