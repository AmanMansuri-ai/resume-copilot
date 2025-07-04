import streamlit as st
import openai
from PyPDF2 import PdfReader
import os

# ✅ Set your OpenAI API key from env
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="ResumeCopilot", page_icon="📄", layout="wide")
st.title("📄 ResumeCopilot")
st.caption("Ask AI questions about your resume — Powered by GPT 🚀")
st.write("---")

with st.sidebar:
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type=["pdf"])

    st.markdown("---")
    st.caption("👤 Aman Mansuri | [GitHub](https://github.com/AmanMansuri-ai/resume-copilot)")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""

    col1, col2 = st.columns([2, 3])

    with col1:
        question = st.text_input("What do you want to ask?")
        if question:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert in resume review."},
                    {"role": "user", "content": f"My resume:\n{resume_text}\n\nQuestion: {question}"}
                ]
            )
            st.write("Answer:", response.choices[0].message.content)

    with col2:
        st.subheader("📝 Resume Preview")
        if st.checkbox("Show extracted resume text"):
            st.write(resume_text)

else:
    st.warning("Please upload your resume from the sidebar.")
