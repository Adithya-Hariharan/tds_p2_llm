# TDS Project 2: Autonomous Quiz Solver Agent

An intelligent agent designed to autonomously solve multi-step web quizzes using Large Language Models (LLM).

## 🚀 Capabilities
* **Web Navigation:** Scrapes pages using Playwright to extract tasks, links, and secrets.
* **Auto-Correction:** Automatically detects and fixes malformed URLs (e.g., removing `-data` suffixes).
* **Math & Data Logic:** Uses Pandas to process CSVs and solve dynamic math challenges.
* **Resilience:** Features a "Robust Model Switcher" that cycles between `llama-3.3-70b`, `llama-3.1`, and `gemma2` to handle API rate limits (429 errors).
* **Multi-Modal Support:** Includes tools for Audio Transcription (Whisper) and Computer Vision (Llama Vision).

## 🛠️ Setup & Usage

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    playwright install
    ```

3.  **Environment Variables:**
    Create a `.env` file and add your keys:
    ```env
    GROQ_API_KEY=gsk_...
    QUIZ_SECRET=TDS-SECRET-KEY-99
    ```

4.  **Run the Server:**
    ```bash
    python main.py
    ```

## 🤖 Architecture
The agent uses a ReAct (Reasoning + Acting) loop to:
1.  **Think:** Analyze the current page content.
2.  **Plan:** Choose the right tool (Navigate, Python, Vision).
3.  **Act:** Execute the tool and observe the output.
4.  **Submit:** Send the final answer via API.