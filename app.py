import streamlit as st
import fitz  # PyMuPDF
import requests
from io import BytesIO
from docx import Document

# ✅ Together AI API function
def ask_together(question, context, api_key):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant who answers questions about resumes."},
            {"role": "user", "content": f"My resume:\n{context}\n\nQuestion: {question}"}
        ],
        "max_tokens": 300
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"❌ API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Request failed: {str(e)}"

# ✅ PDF parsing
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ✅ DOCX creation
def create_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ✅ Page setup
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
    api_key = st.text_input("🔑 Enter Together API Key", type="password")
    st.markdown("---")
    st.caption("👤 Built by Aman Mansuri | [GitHub](https://github.com/AmanMansuri-ai/resume-copilot)")

# ✅ Main app
if uploaded_file:
    if not api_key:
        st.warning("⚠️ Please enter your Together API key to continue.")
        st.stop()

    resume_text = extract_text_from_pdf(uploaded_file)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔎 Choose an Option")
        mode = st.radio("What do you want to do?", ["💬 Ask a question", "🛠️ Improve my resume", "🔍 Job Match Analysis"])

        if mode == "💬 Ask a question":
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            question = st.text_input("Ask something about your resume:")

            if question:
                with st.spinner("Analyzing with AI..."):
                    answer = ask_together(question, resume_text, api_key)
                    st.session_state.chat_history.append({"question": question, "answer": answer})

            for chat in st.session_state.chat_history:
                st.markdown(f"**You:** {chat['question']}")
                st.markdown(f"**AI:** {chat['answer']}")

            if st.button("🧹 Clear Chat"):
                st.session_state.chat_history = []

        elif mode == "🛠️ Improve my resume":
            with st.spinner("Getting suggestions..."):
                review_prompt = (
                    "Please review this resume and provide detailed, practical suggestions to improve it. "
                    "Focus on formatting, clarity, action verbs, quantifying achievements, and any missing sections."
                )
                suggestions = ask_together(review_prompt, resume_text, api_key)

            st.info("✍️ Suggestions to Improve:")
            st.success(suggestions)

            doc_buffer = create_docx(suggestions)
            st.download_button(
                label="📥 Download Suggestions as DOCX",
                data=doc_buffer,
                file_name="Resume_Improvement_Suggestions.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        elif mode == "🔍 Job Match Analysis":
            job_role = st.text_input("Enter the job role you're targeting (e.g., Data Scientist):")
            if job_role:
                with st.spinner("Analyzing job match..."):
                    match_prompt = (
                        f"Given the following resume, analyze how well it matches the job role '{job_role}'. "
                        "Provide a match percentage, key strengths, and suggest areas of improvement to align with the role."
                    )
                    match_result = ask_together(match_prompt, resume_text, api_key)
                st.success(match_result)

    with col2:
        st.subheader("📝 Resume Preview")
        with st.expander("Click to view extracted resume text"):
            st.write(resume_text)

else:
    st.warning("📄 Please upload your resume to get started.")
