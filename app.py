import streamlit as st
import fitz
import requests
from io import BytesIO
from docx import Document

# Together AI API function
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
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return f"❌ API Error: {response.status_code}"

# Extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return " ".join(page.get_text() for page in doc)

# Create DOCX file for download
def create_docx(text):
    doc = Document()
    doc.add_paragraph(text)
    buf = BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf

# Page configuration and styling
st.set_page_config(page_title="ResumeCopilot AI", layout="wide")

st.markdown("""
    <style>
    body { background-color: #f7fafd; }
    h1 { color: #0E5484; font-size: 2.8rem; font-weight: 700; text-align: center; }
    h5 { color: #555; text-align: center; }
    .stButton > button { background-color: #0E5484; color: white; border-radius: 8px; }
    .stTextInput input, .stTextArea textarea { border-radius: 8px; border: 1px solid #ccc; padding: 0.4em; }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>ResumeCopilot</h1>", unsafe_allow_html=True)
st.markdown("<h5>Your AI-powered Resume Assistant 🚀</h5>", unsafe_allow_html=True)
st.write("---")

# Sidebar with upload and API key
with st.sidebar:
    st.header("📄 Upload Resume")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    api_key = st.text_input("🔑 Together API Key", type="password")
    st.markdown("---")
    st.caption("👤 Built by Aman Mansuri | [GitHub](https://github.com/AmanMansuri-ai/resume-copilot)")

# Initialize session state for chat
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Main logic
if uploaded_file:
    if not api_key:
        st.error("Please enter your Together API key.")
        st.stop()

    resume_text = extract_text_from_pdf(uploaded_file)
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("🔎 Select an Action")
        mode = st.radio("", ["💬 Chat About Resume", "🛠️ Improve Resume", "🔍 Job Role Match"])

        # Chat mode with continuous history
        if mode == "💬 Chat About Resume":
            question = st.text_input("Ask a question about your resume:")
            if question:
                with st.spinner("Analyzing with AI..."):
                    answer = ask_together(question, resume_text, api_key)
                    st.session_state.chat_history.append({"question": question, "answer": answer})
            # Display full chat history
            for chat in st.session_state.chat_history:
                st.markdown(f"**You:** {chat['question']}\n\n**AI:** {chat['answer']}")
            if st.button("🧹 Clear Chat History"):
                st.session_state.chat_history.clear()

        # Improve resume mode
        elif mode == "🛠️ Improve Resume":
            with st.spinner("Generating suggestions..."):
                prompt = (
                    "Review this resume and provide clear, actionable improvements: "
                    "formatting, clarity, effective action verbs, and quantified results."
                )
                suggestions = ask_together(prompt, resume_text, api_key)
            st.info("📝 Suggested Improvements:")
            st.success(suggestions)
            buffer = create_docx(suggestions)
            st.download_button("📥 Download Suggestions as DOCX", buffer,
                               file_name="Resume_Improvements.docx",
                               mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        # Job match analysis mode
        else:
            role = st.text_input("Enter your target job role (e.g., Data Scientist):")
            if role:
                with st.spinner("Analyzing match..."):
                    prompt = (
                        f"Analyze how well this resume fits the role '{role}'. "
                        "Give a match percentage, list key strengths, and suggest improvements."
                    )
                    result = ask_together(prompt, resume_text, api_key)
                st.success(result)

    # Resume preview pane
    with col2:
        st.subheader("📄 Resume Preview")
        with st.expander("View extracted resume text"):
            st.write(resume_text)

else:
    st.warning("Please upload a PDF resume to begin.")

st.write("---")
st.caption("🚀 ResumeCopilot • Built by Aman Mansuri • Powered by Together AI & Streamlit Cloud")
