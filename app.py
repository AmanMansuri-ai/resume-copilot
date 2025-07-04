import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader

# ✅ Page configuration
st.set_page_config(page_title="ResumeCopilot - AI Resume Assistant", page_icon="📄", layout="wide")
st.title("📄 ResumeCopilot")
st.caption("Ask AI smart questions about your resume — Powered by Transformers 🚀")
st.write("---")

with st.sidebar:
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type=["pdf"])

    # Optional: About section
    st.markdown("---")
    st.caption("🔨 Built by Aman Mansuri")



# Load QA model
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

# Two columns: Left = Q&A | Right = Resume Preview
col1, col2 = st.columns([2, 3])

if uploaded_file:
    # Extract text
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""

    with col1:
        st.subheader("🔍 Ask AI About Your Resume")
        question = st.text_input("Type your question:")
        if question:
            result = qa_pipeline(question=question, context=resume_text)
            st.write("Answer:", result["answer"])

    with col2:
        st.subheader("📝 Resume Preview")
        if st.checkbox("Show extracted resume text"):
            st.write(resume_text)

else:
    st.warning("Please upload your resume from the sidebar to start.")

st.write("---")
st.caption("ResumeCopilot © 2025 | GitHub: [AmanMansuri-ai](https://github.com/AmanMansuri-ai/resume-copilot)")
