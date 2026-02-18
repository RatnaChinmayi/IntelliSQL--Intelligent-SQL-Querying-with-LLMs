import os
import sqlite3

import google.generativeai as genai
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google.api_core.exceptions import ResourceExhausted

# Load environment variables
load_dotenv(override=True)

api_key = os.getenv("API_KEY")
if not api_key:
    st.error("API_KEY not found! Please check your .env file.")
else:
    genai.configure(api_key=api_key)

# -----------------------------
# Gemini SQL Generator
# -----------------------------
def get_response(question):
    model = genai.GenerativeModel("gemini-2.5-flash")

    prompt = f"""
    You are an expert in converting English questions into SQL queries.
    The database name is STUDENTS.
    Columns are: NAME, CLASS, MARKS, COMPANY.
    Only return the SQL query. No explanation.

    Question: {question}
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except ResourceExhausted:
        return "Error: Quota exceeded. Please wait a moment and try again."
    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# Execute Query (SAFE)
# -----------------------------
def read_query(sql):
    sql = sql.replace("```sql", "").replace("```", "").strip()

    if not sql.upper().startswith("SELECT"):
        return "Only SELECT queries are allowed."

    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    conn.close()

    return pd.DataFrame(rows, columns=columns)

# -----------------------------
# Pages
# -----------------------------
# -----------------------------
# Modern Styling
# -----------------------------
def apply_styles():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #dbeafe, #f0f9ff);
    }

    h1 {
        color: #1e3a8a;
        text-align: center;
    }

    h3 {
        text-align: center;
        color: #475569;
    }

    .feature-card {
    background-color: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.05);
}


    .stButton>button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
    }

    .stButton>button:hover {
        background-color: #1e40af;
        color: white;
    }


    </style>
    """, unsafe_allow_html=True)


# -----------------------------
# Home Page
# -----------------------------
def page_home():
    st.markdown("<h1>✨ IntelliSQL</h1>", unsafe_allow_html=True)
    st.markdown("<h3>AI Powered SQL Assistant</h3>", unsafe_allow_html=True)

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="feature-card">⚡<br><b>Instant SQL Generation</b><br>Convert English to SQL instantly.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-card">🔐<br><b>Safe Execution</b><br>Only SELECT queries allowed.</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="feature-card">🤖<br><b>Powered by Gemini</b><br>Google AI integration.</div>', unsafe_allow_html=True)

    st.divider()
    st.success("💡 Start exploring from the Query Assistant page!")


# -----------------------------
# About Page
# -----------------------------
def page_about():
    st.markdown(
        "<h1 style='text-align:center;'>About IntelliSQL</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center; max-width:800px; margin:auto;'>"
        "IntelliSQL is an AI-powered assistant that converts natural language "
        "questions into SQL queries using Google Gemini AI."
        "</p>",
        unsafe_allow_html=True
    )

    # Proper centered divider
    st.markdown("<hr style='width:60%; margin:auto; margin-top:30px; margin-bottom:40px;'>",
                unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3 style="text-align:left; color:#1e3a8a;">🔹 Technologies Used</h3>
            <ul style="margin-top:10px;">
                <li>Streamlit (Frontend)</li>
                <li>Google Gemini API</li>
                <li>SQLite Database</li>
                <li>Python</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3 style="text-align:left;color:#1e3a8a;">🔹 Key Features</h3>
            <ul style="margin-top:10px;">
                <li>Natural Language to SQL</li>
                <li>Safe SELECT-only execution</li>
                <li>Clean DataFrame output</li>
                <li>AI-Powered Query Optimization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Query Page
# -----------------------------
def page_query():
    st.title("🧠 Intelligent Query Assistant")
    st.divider()

    question = st.text_input("Enter your question:")
    submit = st.button("Generate & Execute")

    if submit and question:
        with st.spinner("Generating SQL..."):
            sql_query = get_response(question)

        if sql_query.startswith("Error:"):
            st.error(sql_query)
        else:
            st.markdown("### Generated SQL:")
            st.code(sql_query, language="sql")

            result = read_query(sql_query)

            if isinstance(result, str):
                st.error(result)
            else:
                st.markdown("### Query Result:")
                st.dataframe(result, use_container_width=True)


# -----------------------------
# Main App
# -----------------------------
def main():
    st.set_page_config(page_title="IntelliSQL", layout="wide")
    apply_styles()

    st.sidebar.title("📌 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Home", "About", "Query Assistant"]
    )

    if page == "Home":
        page_home()
    elif page == "About":
        page_about()
    else:
        page_query()


if __name__ == "__main__":
    main()
