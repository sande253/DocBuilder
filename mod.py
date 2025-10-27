import streamlit as st
import subprocess
import os
import base64
import json
from groq import Groq
from docx import Document
from pptx import Presentation
import io


# === Persistent Chat Memory Utilities ====================

HISTORY_FILE = "chat_history.json"

def load_history():
    """Load saved chat history and state from file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception:
            return {}
    return {}

def save_history():
    """Save current Streamlit session state to file."""
    data = {
        "messages": st.session_state.get("messages", []),
        "current_content": st.session_state.get("current_content"),
        "current_file": None,  # we skip storing binary files
        "doc_topic": st.session_state.get("doc_topic"),
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# =========================================================
# === Initialization ======================================
# =========================================================

if "messages" not in st.session_state:
    data = load_history()
    st.session_state.messages = data.get("messages", [])
    st.session_state.current_content = data.get("current_content")
    st.session_state.current_file = None
    st.session_state.doc_topic = data.get("doc_topic")

# =========================================================
# === Document Generation Functions =======================
# =========================================================

def generate_document_with_groq(api_key, conversation_history, doc_type="pdf", existing_content=None):
    client = Groq(api_key=api_key)
    system_prompt = f"""
    You are an expert {doc_type.upper()} document generator.
    Output ONLY the document content, no commentary.

    Rules:
    - For PDF: valid LaTeX code (\\documentclass... to \\end{document})
    - For DOCX: markdown or text with clear headings and bullet points
    - For PPTX: slide titles and bullet points separated by '---'
    """

    messages = [{"role": "system", "content": system_prompt}]
    messages += conversation_history

    if existing_content:
        messages[-1]["content"] += f"\n\nCurrent document:\n{existing_content[:800]}..."

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.3,
        max_tokens=3000
    )

    text = chat_completion.choices[0].message.content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith(("latex", "md", "text")):
            text = text.split("\n", 1)[1]
    return text.strip()

def compile_to_pdf(latex_code):
    tex_file = "temp.tex"
    pdf_file = "temp.pdf"
    for f in [tex_file, pdf_file, 'temp.aux', 'temp.log', 'temp.out']:
        if os.path.exists(f):
            try: os.remove(f)
            except: pass

    with open(tex_file, 'w', encoding='utf-8') as f:
        f.write(latex_code)
    subprocess.run(['pdflatex', '-interaction=nonstopmode', tex_file], capture_output=True, text=True)

    if os.path.exists(pdf_file):
        with open(pdf_file, 'rb') as f:
            data = f.read()
        for f in [tex_file, pdf_file, 'temp.aux', 'temp.log', 'temp.out']:
            try: os.remove(f)
            except: pass
        return data
    return None

def generate_docx(text):
    doc = Document()
    for line in text.splitlines():
        if line.strip() == "":
            continue
        elif line.startswith("# "):
            doc.add_heading(line[2:], level=1)
        elif line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("- "):
            doc.add_paragraph(line[2:], style="List Bullet")
        else:
            doc.add_paragraph(line)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()

def generate_pptx(text):
    prs = Presentation()
    slides = text.split("---")
    for slide_content in slides:
        lines = [l.strip() for l in slide_content.splitlines() if l.strip()]
        if not lines:
            continue
        title = lines[0]
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = title
        body = slide.placeholders[1]
        for line in lines[1:]:
            p = body.text_frame.add_paragraph()
            p.text = line
    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()

def display_pdf(pdf_bytes):
    base64_pdf = base64.b64encode(pdf_bytes).decode()
    st.markdown(f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="900"></iframe>', unsafe_allow_html=True)

# =========================================================
# === Streamlit UI ========================================
# =========================================================

st.set_page_config(layout="wide")
st.title("Doc Builder")

with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = "API_KEY"
    st.success("API Key connected")

    doc_type = st.selectbox("Choose Output Format", ["pdf", "docx", "pptx", "txt"], index=0)

    if st.button("Clear Everything", use_container_width=True):
        for f in [HISTORY_FILE]:
            if os.path.exists(f):
                os.remove(f)
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

    st.divider()
    st.markdown("""
    *# Tips:**
    - Describe your document (e.g. "Write a business report on AI ethics")
    - Chat and refine it naturally
    - Choose output format
    - Your history is automatically saved
    """)

col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.subheader("Conversation")
    chat_container = st.container(height=500, border=True)
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

with col2:
    st.subheader("Document Preview / Download")
    preview_container = st.container(border=True, height=700)
    with preview_container:
        if st.session_state.current_file:
            if doc_type == "pdf":
                st.download_button("⬇️ Download PDF", st.session_state.current_file, "document.pdf", "application/pdf")
                st.divider()
                display_pdf(st.session_state.current_file)
            elif doc_type == "docx":
                st.download_button("⬇️ Download DOCX", st.session_state.current_file, "document.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            elif doc_type == "pptx":
                st.download_button("⬇️ Download PPTX", st.session_state.current_file, "presentation.pptx", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
            else:
                st.download_button("⬇️ Download TXT", st.session_state.current_file, "document.txt", "text/plain")
        else:
            st.info("Start chatting to generate your document!")

st.divider()
st.subheader("Your Message")

if prompt := st.chat_input("Ask about the document, request changes..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.spinner("Thinking..."):
        try:
            content = generate_document_with_groq(
                api_key, st.session_state.messages[-10:], doc_type, st.session_state.current_content
            )
            st.session_state.current_content = content
            if doc_type == "pdf":
                st.session_state.current_file = compile_to_pdf(content)
            elif doc_type == "docx":
                st.session_state.current_file = generate_docx(content)
            elif doc_type == "pptx":
                st.session_state.current_file = generate_pptx(content)
            else:
                st.session_state.current_file = content.encode("utf-8")
            response = {doc_type.upper()} updated and saved!"
        except Exception as e:
            response = f"[ERROR] {str(e)}"
    st.session_state.messages.append({"role": "assistant", "content": response})
    save_history()
    st.rerun()
