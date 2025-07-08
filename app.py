import streamlit as st
import fitz  # PyMuPDF
import requests
from io import BytesIO
from docx import Document

# ✅ Together API call
def ask_together(question, context, api_key):
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
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

# ✅ Extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return " ".join(page.get_text() for page in doc)

# ✅ Create DOCX file
def create_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# ✅ Streamlit Config & Custom CSS
st.set_page_config(page_title="ResumeCopilot AI", page_icon="📄", layout="wide")

st.markdown("""
    <style>
    body { background-color: #f7fafd; }
    h1 { color: #0E5484; font-size: 2.8rem; font-weight: 700; text-align: center; margin-bottom: 0.3em; }
    h5 { color: #555; text-align: center; font-size: 1.1rem; margin-top: 0; }
    .stButton > button { background-color: #0E5484; color: white; border-radius: 8px; padding: 0.5em 1em; font-weight: 600; }
    .stTextInput > div > div > input { border-radius: 8px; border: 1px solid #ccc; padding: 0.4em; }
    .stRadio > div { gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# ✅ App Header
st.markdown("<h1>ResumeCopilot</h1>", unsafe_allow_html=True)
st.markdown("<h5>Your AI-powered Resume Assistant 🚀</h5>", unsafe_allow_html=True)
st.write("---")

# ✅ Sidebar
with st.sidebar:
    st.header("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    api_key = st.text_input("🔑 Together API Key", type="password")
    st.markdown("---")
    st.caption("👤 Built by Aman Mansuri | [GitHub](https://github.com/AmanMansuri-ai/resume-copilot)")

# ✅ Main App Logic
if uploaded_file:
    if not api_key:
        st.warning("⚠️ Please enter your Together API key to continue.")
        st.stop()

    resume_text = extract_text_from_pdf(uploaded_file)

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔎 Select an Action")
        mode = st.radio("", ["💬 Ask a question", "🛠️ Improve my resume", "🔍 Job Match Analysis"])

        # ✅ Ask a question mode
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

        # ✅ Improve resume mode
        elif mode == "🛠️ Improve my resume":
            with st.spinner("Getting improvement suggestions..."):
                improvement_prompt = (
                    "Review this resume and suggest detailed, actionable improvements on formatting, clarity, and impact. "
                    "Focus on action verbs, quantified results, and clarity."
                )
                suggestions = ask_together(improvement_prompt, resume_text, api_key)

            st.info("✍️ Suggested Improvements:")
            st.success(suggestions)

            doc_buffer = create_docx(suggestions)
            st.download_button(
                label="📥 Download Suggestions as DOCX",
                data=doc_buffer,
                file_name="Resume_Improvements.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        # ✅ Job match analysis mode
        elif mode == "🔍 Job Match Analysis":
            job_role = st.text_input("Enter the job role you're targeting (e.g., Data Scientist):")
            if job_role:
                with st.spinner("Analyzing match..."):
                    match_prompt = (
                        f"Analyze how well this resume matches the role '{job_role}'. "
                        "Give a match percentage, key strengths, and areas to improve."
                    )
                    match_result = ask_together(match_prompt, resume_text, api_key)
                st.success(match_result)

    # ✅ Resume preview
    with col2:
        st.subheader("📝 Resume Preview")
        with st.expander("Click to view extracted resume text"):
            st.write(resume_text)

else:
    st.warning("📄 Please upload your resume to get started.")

st.write("---")
st.caption("🚀 ResumeCopilot • Built by Aman Mansuri • Powered by Together AI & Streamlit Cloud")
