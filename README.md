PromptCraft AI is a professional meta-prompting engine designed to bridge the gap between vague user ideas and high-performance LLM outputs. By using structured frameworks like Role-Context-Task-Format (RCTF), this tool transforms simple scenarios into engineered instructions that get better results from AI models.
Key Features
Structured Prompt Engineering: Automatically applies professional engineering frameworks to raw user input.

Multi-Engine Support: Compatible with Groq (Llama 3 for speed/free tier) and OpenAI (GPT-4o).

SQL History Vault: Every generated prompt is logged in a local SQLite database for future retrieval.

Data Export: Built-in functionality to export your prompt history as a CSV for data analysis.

Interactive Dashboard: A clean, responsive UI built with Streamlit.
Installation & Setup
git clone https://github.com/sakethkumardevatha/PromptCraftAI.git
cd PromptCraftAI

pip install streamlit pandas openai groq
streamlit run app.py

In this project, I demonstrate proficiency in Data Persistence and SQL Operations:

Schema Design: Implemented a relational table with timestamp, category, and text blobs.

CRUD Operations: The app handles Create (saving prompts) and Read (fetching history via Pandas read_sql_query) operations.

Data Integrity: Used IF NOT EXISTS clauses and commit() calls to ensure database reliability.

