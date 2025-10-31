import streamlit as st
import subprocess
import os
import base64
import json
import io
import shutil
import tempfile
from groq import Groq
from docx import Document
from pptx import Presentation
from pptx.util import Inches
from PIL import Image
import pypandoc
import comtypes.client
from google_agent.agent import call_agent
# ============ Configuration ============
HISTORY_FILE = "chat_history.json"
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# ============ History Management ============
def load_history():
    """Load chat history from file."""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_history():
    """Save session state to chat history file."""
    data = {
        "messages": st.session_state.get("messages", []),
        "current_content": st.session_state.get("current_content"),
        "doc_topic": st.session_state.get("doc_topic")
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============ Document Generation ============
def generate_document_with_groq(api_key, conversation_history, doc_type="pdf", existing_content=None, topic="Agentic AI"):
    try : 
       return  call_agent(conversation_history)
    except Exception as e :
        return "Retry once again"
        
def compile_to_pdf(latex_code):
    """Compile LaTeX code to PDF."""
    with tempfile.NamedTemporaryFile(suffix=".tex", dir=TEMP_DIR, delete=False) as tex_file:
        tex_file.write(latex_code.encode('utf-8'))
        tex_path = tex_file.name

    pdf_path = tex_path.replace(".tex", ".pdf")
    subprocess.run(['pdflatex', '-interaction=nonstopmode', f'-output-directory={TEMP_DIR}', tex_path],
                   capture_output=True, text=True)

    if os.path.exists(pdf_path):
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        for ext in ['.tex', '.pdf', '.aux', '.log', '.out']:
            try:
                os.remove(tex_path.replace(".tex", ext))
            except:
                pass
        return pdf_bytes
    st.error("Failed to compile LaTeX to PDF.")
    return None

def generate_docx(text, image_files=None):
    """Generate DOCX file from markdown text."""
    doc = Document()
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            doc.add_heading(line[3:], level=2)
        elif line.startswith("- "):
            doc.add_paragraph(line[2:], style="List Bullet")
        else:
            doc.add_paragraph(line)
    if image_files:
        doc.add_page_break()
        for img in image_files:
            doc.add_picture(img, width=Inches(5))
            doc.add_paragraph(os.path.basename(img))
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()

def generate_pptx(text, image_files=None):
    """Generate PPTX file from slide content."""
    prs = Presentation()
    for slide_content in text.split("---"):
        lines = [l.strip() for l in slide_content.splitlines() if l.strip()]
        if not lines:
            continue
        slide = prs.slides.add_slide(prs.slide_layouts[1])
        slide.shapes.title.text = lines[0]
        body = slide.placeholders[1].text_frame
        for line in lines[1:]:
            p = body.add_paragraph()
            p.text = line[2:] if line.startswith("- ") else line
            if line.startswith("- "):
                p.level = 1
    if image_files:
        for img in image_files:
            slide = prs.slides.add_slide(prs.slide_layouts[6])
            slide.shapes.add_picture(img, Inches(1), Inches(1), width=Inches(6))
    buf = io.BytesIO()
    prs.save(buf)
    return buf.getvalue()

def convert_docx_to_pdf(docx_bytes):
    """Convert DOCX to PDF for preview."""
    with tempfile.NamedTemporaryFile(suffix=".docx", dir=TEMP_DIR, delete=False) as docx_file:
        docx_file.write(docx_bytes)
        docx_path = docx_file.name
    pdf_path = docx_path.replace(".docx", ".pdf")
    try:
        pypandoc.convert_file(docx_path, 'pdf', outputfile=pdf_path, extra_args=['--pdf-engine=pdflatex'])
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        os.remove(docx_path)
        os.remove(pdf_path)
        return pdf_bytes
    except Exception as e:
        st.error(f"Failed to convert DOCX to PDF: {e}")
        return None

def convert_pptx_to_pdf(pptx_bytes):
    """Convert PPTX to PDF (Windows only)."""
    if os.name != 'nt':
        st.warning("PPTX preview is only available on Windows with PowerPoint installed.")
        return None
    with tempfile.NamedTemporaryFile(suffix=".pptx", dir=TEMP_DIR, delete=False) as pptx_file:
        pptx_file.write(pptx_bytes)
        pptx_path = pptx_file.name
    pdf_path = pptx_path.replace(".pptx", ".pdf")
    try:
        powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
        powerpoint.Visible = 1
        presentation = powerpoint.Presentations.Open(pptx_path)
        presentation.SaveAs(pdf_path, 32)  # 32 = PDF format
        presentation.Close()
        powerpoint.Quit()
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        os.remove(pptx_path)
        os.remove(pdf_path)
        return pdf_bytes
    except Exception as e:
        st.error(f"Failed to convert PPTX to PDF: {e}")
        return None

def display_pdf(pdf_bytes):
    """Display PDF in an iframe."""
    if pdf_bytes:
        base64_pdf = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{base64_pdf}" '
            f'width="100%" height="600px" style="border: none;"></iframe>',
            unsafe_allow_html=True
        )
    else:
        st.warning("No preview available.")

# ============ UI Styling ============
st.set_page_config(layout="wide", page_title="Document Builder", page_icon="📝")
st.markdown("""
    <style>
    /* App background */
    .stApp {
        background-color: #0f172a; /* dark navy */
        color: #f1f5f9; /* light gray text */
    }

    /* Titles */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #60a5fa; /* bright blue */
        margin-bottom: 0.5rem;
    }

    .main-subtitle {
        font-size: 1rem;
        color: #94a3b8; /* subtle gray-blue */
        margin-bottom: 1.5rem;
    }

    /* Section Headers */
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #3b82f6; /* vibrant blue */
        margin: 1rem 0;
    }

    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #1e293b; /* dark gray-blue */
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(255,255,255,0.05);
    }

    /* Buttons */
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        border: none;
    }

    .stButton>button:hover {
        background-color: #60a5fa;
    }

    /* Chat and Preview Containers */
    .chat-container,
    .preview-container {
        background-color: #1e293b;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(255,255,255,0.05);
    }

    /* Fixed height for preview with scroll */
    .preview-container {
        height: 700px;
        overflow-y: auto;
    }

    /* Inputs */
    .stTextInput>div>input,
    .stSelectbox>div,
    .stFileUploader>div {
        border-radius: 8px;
        border: 1px solid #334155;
        background-color: #0f172a;
        color: #f1f5f9;
    }

    /* Loading overlay */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 23, 42, 0.85);
        display: flex;
        justify-content: center;
        align-items: center;
        z-index: 9999;
    }

    .spinner {
        border: 4px solid #334155;
        border-top: 4px solid #3b82f6;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .loading-text {
        color: #f1f5f9;
        font-size: 1.2rem;
        margin-left: 1rem;
    }

    /* Mobile tweaks */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
        .preview-container {
            height: 500px;
        }
    }
</style>

""", unsafe_allow_html=True)

# ============ Loading Screen ============
def show_loading_screen():
    """Display a full-screen loading overlay."""
    st.markdown(
        """
        <div class="loading-overlay" id="loading-overlay">
            <div class="spinner"></div>
            <span class="loading-text">Generating your document...</span>
        </div>
        <script>
            function hideLoadingScreen() {
                document.getElementById('loading-overlay').style.display = 'none';
            }
        </script>
        """,
        unsafe_allow_html=True
    )

# ============ Initialization ============
if "messages" not in st.session_state:
    data = load_history()
    st.session_state.messages = data.get("messages", [])
    st.session_state.current_content = data.get("current_content")
    st.session_state.doc_topic = data.get("doc_topic")
    st.session_state.current_file = None
    st.session_state.preview_pdf = None
    st.session_state.doc_type = "pdf"

# ============ UI Layout ============
st.markdown('<div class="main-title">Document Builder</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Create and preview professional documents with ease.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="section-header">Settings</div>', unsafe_allow_html=True)
    
    with st.expander("API Configuration", expanded=True):
        api_key = st.text_input("Groq API Key", type="password", placeholder="Enter your Groq API key", help="Required to generate documents.")
        if api_key:
            st.success("Connected to Groq API")
        else:
            st.warning("Please enter a valid Groq API key.")
    
    with st.expander("Document Options"):
        doc_type = st.selectbox(
            "Output Format",
            ["pdf", "docx", "pptx", "txt"],
            index=["pdf", "docx", "pptx", "txt"].index(st.session_state.doc_type),
            help="Select the format for your document.",
            key="doc_type_select"
        )
        st.session_state.doc_type = doc_type
        uploaded_images = st.file_uploader(
            "Add Images (optional)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            help="Upload images to include in your document."
        )
    
    if st.button("Reset Workspace", key="reset_button", help="Clear all history and reset the app."):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()
    
    st.markdown("""
    **Quick Guide**
    - Enter your API key above.
    - Specify document details in the chat below.
    - Choose a format and upload images if needed.
    - Preview and download your document.
    """)

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown('<div class="section-header">Conversation</div>', unsafe_allow_html=True)
    with st.container():
        chat_container = st.container(height=500, border=True)
        with chat_container:
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

with col2:
    st.markdown('<div class="section-header">Document Preview</div>', unsafe_allow_html=True)
    with st.container():
        if st.session_state.current_file:
            st.download_button(
                f"Download {st.session_state.doc_type.upper()}",
                st.session_state.current_file,
                f"document.{st.session_state.doc_type}",
                mime={
                    "pdf": "application/pdf",
                    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    "txt": "text/plain"
                }[st.session_state.doc_type],
                key="download_button",
                help=f"Download the generated {st.session_state.doc_type.upper()} file."
            )
            display_pdf(st.session_state.preview_pdf)
        else:
            st.info("Enter a prompt below to generate and preview your document.")

# Chat input at the bottom
prompt = st.chat_input("e.g., 'Create a 15-page document about Agentic AI with images'")

# ============ Handle User Input ============
if prompt:
    if not api_key:
        st.error("Please provide a valid Groq API key in the sidebar.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    show_loading_screen()
    with st.spinner("Processing..."):
        temp_imgs = []
        try:
            # Detect topic from prompt
            topic = "Agentic AI" if "agentic ai" in prompt.lower() else st.session_state.get("doc_topic", "General")
            if "agentic ai" in prompt.lower():
                st.session_state.doc_topic = "Agentic AI"
                st.session_state.current_content = None  # Reset content for new topic
            
            content = generate_document_with_groq(
                api_key, 
                prompt, 
                st.session_state.doc_type, 
                st.session_state.current_content, 
                topic
            )
            display_content = content  # since call_agent returns a string
            if not content:
                raise ValueError("No content generated.")
            st.session_state.current_content = content
            
            if uploaded_images:
                for img in uploaded_images:
                    img_path = os.path.join(TEMP_DIR, f"temp_{img.name}")
                    with open(img_path, "wb") as f:
                        f.write(img.getvalue())
                    temp_imgs.append(img_path)

            if st.session_state.doc_type == "pdf":
                latex = content
                if temp_imgs:
                    for i, img in enumerate(temp_imgs[:5]):  # Limit to 5 images
                        img_latex = f"\\includegraphics[width=0.8\\linewidth]{{{img}}}\n\\caption{{Image {i+1}: {os.path.basename(img)}}}\n"
                        latex = latex.replace(f"<<image{i+1}>>", img_latex)
                st.session_state.current_file = compile_to_pdf(latex)
                st.session_state.preview_pdf = st.session_state.current_file
            elif st.session_state.doc_type == "docx":
                st.session_state.current_file = generate_docx(content, temp_imgs)
                st.session_state.preview_pdf = convert_docx_to_pdf(st.session_state.current_file)
            elif st.session_state.doc_type == "pptx":
                st.session_state.current_file = generate_pptx(content, temp_imgs)
                st.session_state.preview_pdf = convert_pptx_to_pdf(st.session_state.current_file)
            else:
                st.session_state.current_file = content.encode()
                st.session_state.preview_pdf = compile_to_pdf(content)

            response = display_content
        except Exception as e:
            response = f"Error generating document: {e}"
            st.session_state.current_file = None
            st.session_state.preview_pdf = None
        finally:
            for img in temp_imgs:
                try:
                    os.remove(img)
                except:
                    pass

        st.session_state.messages.append({"role": "assistant", "content": response})
        save_history()
        st.markdown("<script>hideLoadingScreen();</script>", unsafe_allow_html=True)
        st.rerun()

# ============ Cleanup ============
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)