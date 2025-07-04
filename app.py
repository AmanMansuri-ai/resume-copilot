import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader

st.markdown("<h1 style='text-align: center; color: #0E5484;'>📄 Resumed By Copilot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Ask AI smart questions about your resume — Powered by Transformers 🚀</p>", unsafe_allow_html=True)
st.write("---")


with st.sidebar:
    st.header("📄 Upload Your Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF)", type=["pdf"])

    st.markdown("---")
    st.markdown("👤 **Aman Mansuri**")
    st.caption("[GitHub Repo](https://github.com/AmanMansuri-ai/resume-copilot)")




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
        col1.subheader("🤖 Ask AI About Your Resume")

        question = st.text_input("Type your question:")
        if question:
            result = qa_pipeline(question=question, context=resume_text)
            st.write("Answer:", result["answer"])

    with col2:
        col2.subheader("📝 Resume Text Preview")

        if st.checkbox("Show extracted resume text"):
            st.write(resume_text)

else:
    st.warning("Please upload your resume from the sidebar to start.")

st.write("---")
st.markdown("<p style='text-align: center; font-size: 12px;'>© 2025 Aman Mansuri | Built with ❤️ using Streamlit</p>", unsafe_allow_html=True)

