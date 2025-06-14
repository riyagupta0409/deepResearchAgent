# 🧠 Deep Research Agent: Documentation

This document provides a complete overview of the Deep Research Agent, a planning-capable, autonomous AI agent designed for in-depth research tasks.

---

## ✨ Features

- **Dynamic Planning**: Automatically generates multi-step research plans based on user queries.
- **Autonomous Execution**: Uses a suite of tools to execute the plan, including web searches and content scraping.
- **Self-Healing Architecture**: A validation layer programmatically checks and corrects the AI's plan to ensure logical correctness before execution.
- **Resilient Tooling**: Gracefully handles real-world errors like third-party API failures and empty search results.
- **Interactive UI**: A modern, chat-based Streamlit application provides real-time progress updates and a clean, readable final output.
- **Transparent Reporting**: Clearly displays the final answer, the search queries it used, and the web sources it successfully scraped.

---

## 🏗️ Architecture & Flow

The agent operates on a **Planner-Validator-Executor** loop, a robust pattern for building autonomous agents. The data flows through a state machine managed by LangGraph.

### Architecture Diagram

```mermaid
graph TD
    subgraph "Frontend"
        A[<fa:fa-user> User Enters Query <br> (Streamlit UI)]
    end

    subgraph "Agent Backend (LangGraph)"
        B(Input Node)
        C(Planning Node)
        D(Plan Validation Node)
        E(Execution Loop)
        F(Output Formatter)
    end

    subgraph "External APIs & Tools"
        G[<fa:fa-brain> Gemini API <br> (Planner & Summarizer)]
        H[<fa:fa-search> SerpApi <br> (Web Search)]
        I[<fa:fa-fire> Firecrawl API <br> (Web Scraping)]
    end

    A --> B
    B --> C
    C --> D
    D --> E
    E -- has next step --> E
    E -- plan complete --> F
    F --> J[<fa:fa-file-alt> Final Answer <br> (Displayed in UI)]
    A -.-> J

    C --> G
    E -- "action: search_google" --> H
    E -- "action: scrape_url" --> I
    E -- "action: summarize" --> G

```

### Workflow Explained

1.  **Input**: The user provides a query via the Streamlit UI.
2.  **Planning**: The `planning_node` calls the Gemini API to generate a JSON plan with a sequence of actions (e.g., `search_google`, `scrape_url`, `summarize`).
3.  **Validation**: The `plan_validation_node` programmatically inspects the plan. It corrects common AI mistakes, such as ensuring the `summarize` step receives input from all `scrape` steps. This is a critical, non-AI, self-healing step.
4.  **Execution**: The `execution_node` loops through the validated plan, calling the appropriate tool for each step. It is designed to be resilient:
    *   It intelligently extracts URLs from search result objects.
    *   It handles failed scrapes by recording a `SCRAPE_FAILED` message instead of crashing.
    *   It filters out any failed steps before aggregation, allowing it to proceed with partial data.
5.  **Output**: The `output_formatter_node` gathers the final answer, the search queries used, and a list of successfully scraped URLs. It formats this into a single JSON object.
6.  **UI Display**: The Streamlit `app.py` receives the final JSON and displays it in a clean, user-friendly format, with research details tucked into a collapsible section.

---

## 🚀 How to Run

1.  **Set up Environment Variables**:
    Create a `.env` file in the root directory and add your API keys:
    ```
    GEMINI_API_KEY="your_gemini_api_key"
    SERPER_API_KEY="your_serper_api_key"
    FIRECRAWL_API_KEY="your_firecrawl_api_key"
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```

4.  **Open in Browser**: Navigate to the local URL provided by Streamlit to start your research.
