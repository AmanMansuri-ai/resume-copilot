import streamlit as st
import fitz
import requests
from io import BytesIO
from docx import Document

# 🎨 Theme toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)

# Theme CSS
if dark_mode:
    background = "#2E3440"
    text_color = "#ECEFF4"
    card_bg = "#3B4252"
    btn_color = "#5E81AC"
    st.markdown(f"""
        <style>
        body {{ background-color: {background}; color: {text_color}; }}
        .stButton > button {{ background-color: {btn_color}; color: white; }}
        .stTextInput input, .stTextArea textarea {{ background-color: {card_bg}; color: {text_color}; }}
        .main, .block-container {{ background-color: {background}; }}
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body { background-color: #f7fafd; }
        .stButton > button { background-color: #0E5484; color: white; }
        .stTextInput input, .stTextArea textarea { background-color: #fff; color: #000; }
        </style>
    """, unsafe_allow_html=True)

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
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return f"❌ API Error: {response.status_code}"

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return " ".join(page.get_text() for page in doc)

def create_docx(text):
    doc = Document(); doc.add_paragraph(text)
    buf = BytesIO(); doc.save(buf); buf.seek(0)
    return buf

# Page header
st.set_page_config(page_title="ResumeCopilot AI", layout="wide")
st.markdown("<h1>Your AI Resume Assistant</h1>", unsafe_allow_html=True)
st.write("---")

# Sidebar
with st.sidebar:
    uploaded_file = st.file_uploader("📄 Upload your resume (PDF)", type=["pdf"])
    api_key = st.text_input("🔑 Together API Key", type="password")

# Main
if uploaded_file:
    if not api_key:
        st.error("Please enter your Together API key.")
        st.stop()
    resume_text = extract_text_from_pdf(uploaded_file)
    c1, c2 = st.columns([1, 2])
    with c1:
        mode = st.radio("Select Action", ["💬 Ask Questions", "🛠️ Improve Resume", "🔍 Job Role Match"])
        if mode == "💬 Ask Questions":
            if "chat" not in st.session_state: st.session_state.chat = []
            q = st.text_input("Ask about your resume…")
            if q:
                with st.spinner("Thinking…"): a = ask_together(q, resume_text, api_key)
                st.session_state.chat.append((q, a))
            for q, a in st.session_state.chat:
                st.markdown(f"**You:** {q}"); st.markdown(f"**AI:** {a}")
            if st.button("🧹 Clear Chat"): st.session_state.chat = []

        elif mode == "🛠️ Improve Resume":
            with st.spinner("Generating suggestions…"):
                prompt = ("Review this resume; suggest clear improvements: formatting, clarity, action verbs, quantified results.")
                suggestions = ask_together(prompt, resume_text, api_key)
            st.info("📝 Suggestions:"); st.success(suggestions)
            buf = create_docx(suggestions)
            st.download_button("📥 Download DOCX", buf, file_name="Improvements.docx")

        else:
            role = st.text_input("Target Job Role:")
            if role:
                with st.spinner("Analyzing match…"):
                    prompt = (f"Analyze fit for '{role}'. Give % match, strengths, and suggestions.")
                    result = ask_together(prompt, resume_text, api_key)
                st.success(result)
    with c2:
        st.subheader("📄 Resume Preview")
        with st.expander("See extracted text"):
            st.write(resume_text)
else:
    st.warning("Upload a PDF to begin.")

st.write("---")
st.caption("Built by Aman Mansuri • Powered by Together AI & Streamlit Cloud")
