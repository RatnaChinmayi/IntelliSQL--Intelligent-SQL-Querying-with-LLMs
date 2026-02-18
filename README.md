# 📌 IntelliSQL: Intelligent SQL Querying with LLMs

## 🔹 Overview
**IntelliSQL** is an AI-powered SQL assistant that allows users to interact with databases using natural language. It uses Google Gemini LLM to convert plain English queries into SQL statements and executes them on a SQLite database.
This system simplifies database querying and supports intelligent data exploration.

---

## 🚀 Features
- Natural Language to SQL conversion
- Intelligent query generation
- SQLite database execution
- Interactive Streamlit web interface
- Real-time query results display

---

## 🏗️ Workflow
1. User enters a natural language query in Streamlit UI.
2. Input is sent to Gemini via Google API.
3. Gemini generates the SQL query.
4. SQL query executes on SQLite database.
5. Results are displayed to the user.

---

## 🛠️ Technologies Used
- Python
- Streamlit
- Google Generative AI (Gemini)
- SQLite3

---

## 📂 Project Structure
IntelliSQL/
│
├── app.py
├── sql.py
├── data.db
├── requirements.txt

---

## 📋 Requirements
Create a `requirements.txt` file:
streamlit
google-generativeai
python-dotenv
> Note: `sqlite3` is built-in with Python.

---

## ⚙️ Installation
### Create Virtual Environment
python -m venv myenv
### Activate (Windows)
myenv\Scripts\activate
### Install Dependencies
pip install -r requirements.txt

---

## 🔑 API Key Setup
Create a `.env` file and add:
GOOGLE_API_KEY=your_api_key_here

---

## ▶️ Run the Application
streamlit run app.py

---

## 🎯 Applications
- SQL Learning Assistant
- Data Analysis Tool
- AI-powered Database Querying System

---

## ⭐ Conclusion
IntelliSQL bridges the gap between natural language and SQL by leveraging LLMs, making database interaction simple, intelligent, and efficient.
