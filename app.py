# app.py - Advanced Resume Analyzer (Ollama Powered)

import streamlit as st
import PyPDF2
from langchain_community.llms import Ollama

st.set_page_config(page_title="AI Resume Analyzer", layout="wide")

st.title("🚀 AI Resume Analyzer (Local LLM - Ollama)")

# Initialize model
llm = Ollama(model="mistral")

pdf = st.file_uploader("📄 Upload Resume PDF", type="pdf")

def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

if pdf:
    with st.spinner("Reading resume..."):
        resume_text = extract_text_from_pdf(pdf)

    st.success("✅ Resume Loaded Successfully")

    query = st.text_input("🔍 Ask anything about the resume:",
                          placeholder="Example: What is the candidate's name?")

    if st.button("Analyze Resume"):

        if not query.strip():
            st.warning("Please enter a question.")
        else:

            prompt = f"""
You are a professional HR resume analyzer.

Analyze the resume below carefully and answer the question clearly and professionally.

Resume:
----------------
{resume_text}
----------------

Question:
{query}

Instructions:
- If the answer exists, extract it clearly.
- If not found, say: "Information not found in resume."
- Provide a short professional explanation.
- Do NOT guess.
"""

            with st.spinner("Analyzing with AI..."):
                response = llm.invoke(prompt)

            st.markdown("### 📊 AI Analysis Result")
            st.info(response)
