import streamlit as st
from PyPDF2 import PdfReader
import os
import requests

# ✅ Together API function
def ask_together(question, context):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('TOGETHER_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who answers questions about resumes."},
            {"role": "user", "content": f"My resume:\n{context}\n\nQuestion: {question}"}
        ],
        "max_tokens": 200
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"

# ✅ Page config
st.set_page_config(page_title="ResumeCopilot AI", page_icon="📄", layout="wide")

# ✅ Custom CSS
st.markdown("""
    <style>
    .main { background-color: #f9fafc; }
    .block-container { padding-top: 2rem; }
    h1 { color: #0E5484; font-size: 3rem; text-align: center; margin-bottom: 0.2em; }
    h5 { color: #555; text-align: center; margin-top: 0; }
    .stButton > button { background-color: #0E5484; color: white; border-radius: 5px; }
    .stTextInput > div > div > input { border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# ✅ Header
st.markdown("<h1>ResumeCopilot</h1>", unsafe_allow_html=True)
st.markdown("<h5>Your smart AI-powered resume assistant 🚀</h5>", unsafe_allow_html=True)
st.write("---")

# ✅ Sidebar
with st.sidebar:
    st.header("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    st.markdown("---")
    st.caption("👤 Built by Aman Mansuri | [GitHub](https://github.com/AmanMansuri-ai/resume-copilot)")

# ✅ If resume uploaded
if uploaded_file:
    reader = PdfReader(uploaded_file)
    resume_text = ""
    for page in reader.pages:
        resume_text += page.extract_text() or ""

    # ✅ Two-column layout
    col1, col2 = st.columns([1, 2])

    # ✅ Question Box
    with col1:
        st.subheader("💬 Ask AI About Your Resume")
        st.markdown("Example: *What are my strengths?*")
        question = st.text_input("Ask a question:")
        if question:
            answer = ask_together(question, resume_text)
            st.success(answer)

    # ✅ Resume Preview with expand/collapse
    with col2:
        st.subheader("📝 Resume Preview")
        with st.expander("Click to view extracted resume text"):
            st.write(resume_text)

else:
    st.warning("🚨 Please upload your resume to start.")
