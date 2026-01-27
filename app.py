import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
# For OpenAI: pip install openai
from openai import OpenAI
# For Groq: pip install groq (Free & Fast alternative)
try:
    from groq import Groq
except ImportError:
    pass

# --- I. DATABASE INITIALIZATION & REPAIR ---
def init_db():
    conn = sqlite3.connect('prompt_vault.db')
    cursor = conn.cursor()
    # This creates the table with ALL necessary columns if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            scenario TEXT NOT NULL,
            result TEXT NOT NULL,
            category TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_to_sql(scenario, result, category):
    conn = sqlite3.connect('prompt_vault.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prompts (scenario, result, category) VALUES (?, ?, ?)",
                   (scenario, result, category))
    conn.commit()
    conn.close()

# --- II. GENERATION LOGIC (Unified) ---
def generate_prompt(scenario, domain, provider, api_key):
    system_instruction = f"Act as an Expert Prompt Engineer specializing in {domain}. Transform the scenario into a high-performance prompt using Role, Context, and Task."
    
    if provider == "Groq (Free/Fast)":
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": system_instruction},
                      {"role": "user", "content": scenario}]
        )
        return response.choices[0].message.content
    else:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_instruction},
                      {"role": "user", "content": scenario}]
        )
        return response.choices[0].message.content

# --- III. UI ENGINE ---
st.set_page_config(page_title="PromptCraft AI", layout="wide")
init_db() # RUNS EVERY TIME TO ENSURE SQL IS READY

st.title("🪄 PromptCraft AI")

with st.sidebar:
    st.header("1. API Settings")
    provider = st.selectbox("Select Provider", ["Groq (Free/Fast)", "OpenAI"])
    api_key = st.text_input(f"Enter {provider} API Key", type="password")
    if provider == "Groq (Free/Fast)":
        st.write("[Get a Free Groq Key here](https://console.groq.com/keys)")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Define Scenario")
    scenario_input = st.text_area("Your Goal:", placeholder="e.g. Write a script to clean SQL data.")
    domain_choice = st.selectbox("Category", ["Data Science", "Coding", "Writing"])
    
    if st.button("Generate & Save"):
        if not api_key:
            st.error("Missing API Key!")
        else:
            try:
                final_prompt = generate_prompt(scenario_input, domain_choice, provider, api_key)
                st.session_state['result'] = final_prompt
                save_to_sql(scenario_input, final_prompt, domain_choice)
                st.success("Saved to SQL!")
            except Exception as e:
                st.error(f"Error: {e}")

with col2:
    st.subheader("Engineered Result")
    if 'result' in st.session_state:
        st.markdown(st.session_state['result'])

# --- IV. HISTORY (SQL LOAD) ---
st.divider()
st.subheader("📜 History from SQL")
try:
    conn = sqlite3.connect('prompt_vault.db')
    # Fixed Query: Matches the new init_db structure
    history_df = pd.read_sql_query("SELECT timestamp, category, scenario FROM prompts ORDER BY id DESC LIMIT 10", conn)
    st.dataframe(history_df, use_container_width=True)
    conn.close()
except Exception as e:
    st.warning("No history found yet or table is initializing.")