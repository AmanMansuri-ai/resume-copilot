import streamlit as st
from PyPDF2 import PdfReader
import os
import requests

# ✅ OpenRouter API Key from Streamlit Secrets
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# ✅ LLaMA API Call
def ask_llama(question, context):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    # Send the resume and question as context
    payload = {
        "model": "meta-llama/llama-3-8b-instruct:free",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who answers questions about resumes."},
            {"role": "user", "content": f"My resume:\n{context}\n\nQuestion: {question}"}
        ],
        "max_tokens": 150
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# ✅ Streamlit UI
st.set_page_config(page_title="ResumeCopilot", page_icon="📄", layout="wide")
st.markdown("<h1 style='text-align: center; color: #0E5484;'>📄 ResumeCopilot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ask AI smart questions about your resume — Powered by LLaMA 3 🚀</p>", unsafe_allow_html=True)
st.write("---")

# ✅ Sidebar
with st.sidebar:
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type=["pdf"])
    st.markdown("---")
    st.caption("👤 Aman Mansuri | [GitHub](https://github.com/AmanMansuri-ai/resume-copilot)")

# ✅ Resume Q&A Flow
if uploaded_file:
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""

    col1, col2 = st.columns([2, 3])

    with col1:
        st.subheader("🤖 Ask AI About Your Resume")
        question = st.text_input("Type your question:")
        if question:
            answer = ask_llama(question, resume_text)
            st.write("Answer:", answer)

    with col2:
        st.subheader("📝 Resume Preview")
        if st.checkbox("Show extracted resume text"):
            st.write(resume_text)

else:
    st.warning("Please upload your resume from the sidebar.")
