import streamlit as st
from PyPDF2 import PdfReader
import os
import requests

# ✅ Hugging Face API call function
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

def ask_huggingface(question, context):
    API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": {"question": question, "context": context}}

    response = requests.post(API_URL, headers=headers, json=payload)
    
    # ✅ Safely handle the response
    if response.status_code == 200:
        result = response.json()
        return result.get('answer', 'No answer found')
    else:
        return f"Error: {response.status_code} - {response.text}"

# ✅ Streamlit page config
st.set_page_config(page_title="ResumeCopilot", page_icon="📄", layout="wide")
st.markdown("<h1 style='text-align: center; color: #0E5484;'>📄 ResumeCopilot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ask AI smart questions about your resume — Powered by Hugging Face 🚀</p>", unsafe_allow_html=True)
st.write("---")

# ✅ Sidebar upload
with st.sidebar:
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type=["pdf"])
    st.markdown("---")
    st.caption("👤 Aman Mansuri | [GitHub](https://github.com/AmanMansuri-ai/resume-copilot)")

# ✅ Process resume
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
            answer = ask_huggingface(question, resume_text)
            st.write("Answer:", answer)

    with col2:
        st.subheader("📝 Resume Preview")
        if st.checkbox("Show extracted resume text"):
            st.write(resume_text)

else:
    st.warning("Please upload your resume from the sidebar.")
