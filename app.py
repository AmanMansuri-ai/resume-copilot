import streamlit as st
from transformers import pipeline
from PyPDF2 import PdfReader

# Load QA model from Hugging Face
qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")

st.title("ResumeCopilot - Ask Questions About Your Resume")

# Step 1: Upload the resume
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf")

if uploaded_file:
    # Step 2: Read and extract text from PDF
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""
    
    st.success("Resume uploaded and text extracted successfully ✅")
    
    # Optional: Show the resume text
    if st.checkbox("Show extracted resume text"):
        st.write(resume_text)
    
    # Step 3: Ask a question
    question = st.text_input("What do you want to ask about your resume?")
    
    if question:
        result = qa_pipeline(question=question, context=resume_text)
        st.write("Answer:", result["answer"])

else:
    st.warning("Please upload your resume to start asking questions.")
