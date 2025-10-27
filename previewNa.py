from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors 
import HexColor 
import streamlit as st
import os
import json
import io
import shutil
import tempfile
from groq import Groq
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from pptx import Presentation
from pptx.util import Inches as PptxInches
import base64
from PIL import Image
import subprocess

# ============ Configuration ============
HISTORY_FILE = "chat_history.json"
TEMP_DIR = "temp_files"
os.makedirs(TEMP_DIR, exist_ok=True)

# ============ History Management ============
def load_history():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_history():
    data = {
        "messages": st.session_state.get("messages", []),
        "current_content": st.session_state.get("current_content"),
    }
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============ Document Generation ============
def generate_document_with_groq(api_key, conversation_history, doc_type="pdf", topic="Document"):
    """Generate document content using Groq API."""
    client = Groq(api_key=api_key)
    
    system_prompt = f"""Generate a comprehensive 15-page professional document about {topic}.

Use this EXACT format with these markers at the start of lines:
TITLE: [Your main title here]
HEADING: [Section heading]
SUBHEADING: [Subsection heading]
BULLET: [Bullet point text]
TEXT: [Regular paragraph text]

Example:
TITLE: Business Partnership Agreement
HEADING: Article 1: Company Formation
TEXT: The partners agree to establish a business entity...
SUBHEADING: Ownership Structure
BULLET: Partner A will own 60% of the company
BULLET: Partner B will own 40% of the company
TEXT: This agreement outlines the terms and conditions...

Generate at least 15 pages of content with multiple sections, headings, subheadings, bullet points, and paragraphs.
IMPORTANT: Use ONLY the markers above. Do NOT use markdown, LaTeX, or any other formatting."""

    messages = [{"role": "system", "content": system_prompt}] + conversation_history

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.3,
            max_tokens=35000
        )
        text = chat_completion.choices[0].message.content.strip()
        return text
    
    except Exception as e:
        st.error(f"Failed to generate document: {e}")
        return None

def add_border_to_paragraph(paragraph, color="000000", size="8"):
    """Add a border around a paragraph."""
    p = paragraph._element
    pPr = p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    
    for border_name in ['top', 'left', 'bottom', 'right']:
        border_el = OxmlElement(f'w:{border_name}')
        border_el.set(qn('w:val'), 'single')
        border_el.set(qn('w:sz'), size)
        border_el.set(qn('w:space'), '0')
        border_el.set(qn('w:color'), color)
        pBdr.append(border_el)
    
    pPr.append(pBdr)

def generate_docx(text, image_files=None):
    """Generate DOCX with proper formatting, borders, and bold text."""
    doc = Document()
    
    # Set margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
    
    # Add header
    header = doc.sections[0].header
    header_para = header.paragraphs[0]
    header_run = header_para.add_run("Professional Document")
    header_run.font.size = Pt(10)
    header_run.font.bold = True
    header_run.font.color.rgb = RGBColor(30, 58, 138)
    
    # Parse content
    lines = text.strip().split('\n')
    img_idx = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            doc.add_paragraph()
            continue
        
        # TITLE
        if line.startswith("TITLE:"):
            title_text = line.replace("TITLE:", "").strip()
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(title_text)
            run.font.size = Pt(24)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 58, 138)
            add_border_to_paragraph(p, "1e3a8a", "16")
            p.paragraph_format.space_after = Pt(12)
            p.paragraph_format.space_before = Pt(12)
        
        # HEADING
        elif line.startswith("HEADING:"):
            heading_text = line.replace("HEADING:", "").strip()
            p = doc.add_paragraph()
            run = p.add_run(heading_text)
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(30, 58, 138)
            add_border_to_paragraph(p, "1e3a8a", "12")
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(6)
        
        # SUBHEADING
        elif line.startswith("SUBHEADING:"):
            subheading_text = line.replace("SUBHEADING:", "").strip()
            p = doc.add_paragraph()
            run = p.add_run(subheading_text)
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = RGBColor(59, 130, 246)
            add_border_to_paragraph(p, "3b82f6", "12")
            p.paragraph_format.space_before = Pt(8)
            p.paragraph_format.space_after = Pt(4)
        
        # BULLET
        elif line.startswith("BULLET:"):
            bullet_text = line.replace("BULLET:", "").strip()
            p = doc.add_paragraph(bullet_text, style='List Bullet')
            for run in p.runs:
                run.font.size = Pt(11)
                run.font.name = "Calibri"
            add_border_to_paragraph(p, "cbd5e1", "8")
            p.paragraph_format.space_after = Pt(4)
        
        # TEXT
        elif line.startswith("TEXT:"):
            text_content = line.replace("TEXT:", "").strip()
            p = doc.add_paragraph(text_content)
            for run in p.runs:
                run.font.size = Pt(11)
                run.font.name = "Calibri"
                run.font.color.rgb = RGBColor(51, 51, 51)
            add_border_to_paragraph(p, "cbd5e1", "8")
            p.paragraph_format.space_after = Pt(6)
            p.paragraph_format.line_spacing = 1.15
        
        # IMAGE
        elif line.startswith("IMAGE:"):
            if image_files and img_idx < len(image_files):
                try:
                    p = doc.add_paragraph()
                    run = p.add_run()
                    run.add_picture(image_files[img_idx], width=Inches(5.5))
                    
                    caption = doc.add_paragraph(f"Figure {img_idx + 1}")
                    for run in caption.runs:
                        run.font.size = Pt(10)
                        run.font.italic = True
                        run.font.color.rgb = RGBColor(100, 116, 139)
                    add_border_to_paragraph(caption, "64748b", "8")
                    
                    img_idx += 1
                except Exception as e:
                    pass
    
    buf = io.BytesIO()
    doc.save(buf)
    buf.seek(0)
    return buf.getvalue()

def generate_pdf(text, image_files=None):
    """Generate PDF with proper formatting."""
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image as RLImage
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.colors import HexColor
    
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('1e3a8a'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=HexColor('1e3a8a'),
        spaceAfter=6,
        fontName='Helvetica-Bold'
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubHeading',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=HexColor('3b82f6'),
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        alignment=TA_LEFT,
        spaceAfter=6
    )
    
    lines = text.strip().split('\n')
    img_idx = 0
    
    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 0.1*inch))
            continue
        
        # TITLE
        if line.startswith("TITLE:"):
            title_text = line.replace("TITLE:", "").strip()
            story.append(Paragraph(title_text, title_style))
            story.append(Spacer(1, 0.2*inch))
        
        # HEADING
        elif line.startswith("HEADING:"):
            heading_text = line.replace("HEADING:", "").strip()
            story.append(Paragraph(heading_text, heading_style))
            story.append(Spacer(1, 0.1*inch))
        
        # SUBHEADING
        elif line.startswith("SUBHEADING:"):
            subheading_text = line.replace("SUBHEADING:", "").strip()
            story.append(Paragraph(subheading_text, subheading_style))
            story.append(Spacer(1, 0.05*inch))
        
        # BULLET
        elif line.startswith("BULLET:"):
            bullet_text = line.replace("BULLET:", "").strip()
            story.append(Paragraph("• " + bullet_text, body_style))
        
        # TEXT
        elif line.startswith("TEXT:"):
            text_content = line.replace("TEXT:", "").strip()
            story.append(Paragraph(text_content, body_style))
        
        # IMAGE
        elif line.startswith("IMAGE:"):
            if image_files and img_idx < len(image_files):
                try:
                    story.append(Spacer(1, 0.1*inch))
                    story.append(RLImage(image_files[img_idx], width=5*inch, height=4*inch))
                    story.append(Spacer(1, 0.1*inch))
                    img_idx += 1
                except:
                    pass
    
    doc.build(story)
    buf.seek(0)
    return buf.getvalue()

def generate_pptx(text, image_files=None):
    """Generate PPTX presentation."""
    prs = Presentation()
    prs.slide_width = PptxInches(10)
    prs.slide_height = PptxInches(7.5)
    
    blank_layout = prs.slide_layouts[6]
    title_layout = prs.slide_layouts[0]
    bullet_layout = prs.slide_layouts[1]
    
    lines = text.strip().split('\n')
    slide_count = 1
    current_slide = None
    
    for line in lines:
        line = line.strip()
        if not line or slide_count >= 15:
            continue
        
        # TITLE slide
        if line.startswith("TITLE:"):
            slide = prs.slides.add_slide(title_layout)
            title = slide.shapes.title
            title.text = line.replace("TITLE:", "").strip()
            slide_count += 1
        
        # HEADING becomes new slide
        elif line.startswith("HEADING:"):
            if slide_count >= 15:
                break
            current_slide = prs.slides.add_slide(bullet_layout)
            current_slide.shapes.title.text = line.replace("HEADING:", "").strip()
            slide_count += 1
        
        # BULLET point
        elif line.startswith("BULLET:"):
            if current_slide is None and slide_count < 15:
                current_slide = prs.slides.add_slide(bullet_layout)
                current_slide.shapes.title.text = "Content"
                slide_count += 1
            
            if current_slide and len(current_slide.placeholders) > 1:
                body_shape = current_slide.placeholders[1]
                text_frame = body_shape.text_frame
                p = text_frame.add_paragraph()
                p.text = line.replace("BULLET:", "").strip()
                p.font.size = Pt(12)
    
    # Ensure 15 slides
    while slide_count < 15:
        slide = prs.slides.add_slide(bullet_layout)
        slide.shapes.title.text = f"Slide {slide_count}"
        slide_count += 1
    
    buf = io.BytesIO()
    prs.save(buf)
    buf.seek(0)
    return buf.getvalue()

def docx_to_pdf(docx_bytes):
    """Convert DOCX to PDF for preview."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
            tmp.write(docx_bytes)
            tmp_path = tmp.name
        
        pdf_path = tmp_path.replace(".docx", ".pdf")
        
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", tempfile.gettempdir(), tmp_path],
            capture_output=True,
            timeout=30
        )
        
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            os.remove(tmp_path)
            os.remove(pdf_path)
            return pdf_data
    except:
        pass
    return None

def pptx_to_pdf(pptx_bytes):
    """Convert PPTX to PDF for preview."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as tmp:
            tmp.write(pptx_bytes)
            tmp_path = tmp.name
        
        pdf_path = tmp_path.replace(".pptx", ".pdf")
        
        subprocess.run(
            ["libreoffice", "--headless", "--convert-to", "pdf", "--outdir", tempfile.gettempdir(), tmp_path],
            capture_output=True,
            timeout=30
        )
        
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()
            os.remove(tmp_path)
            os.remove(pdf_path)
            return pdf_data
    except:
        pass
    return None

def display_pdf_preview(pdf_bytes):
    """Display PDF preview in iframe."""
    if pdf_bytes:
        b64 = base64.b64encode(pdf_bytes).decode()
        st.markdown(
            f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="700px"></iframe>',
            unsafe_allow_html=True
        )
        return True
    return False

# ============ UI Styling ============
st.set_page_config(layout="wide", page_title="Document Builder", page_icon="📝")
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    .main-title { font-size: 2.2rem; font-weight: 700; color: #1e3a8a; margin-bottom: 0.5rem; }
    .main-subtitle { font-size: 1rem; color: #64748b; margin-bottom: 1.5rem; }
    .section-header { font-size: 1.3rem; font-weight: 600; color: #1e3a8a; margin: 1rem 0; }
    .stButton>button { background-color: #1e3a8a; color: white; border-radius: 8px; padding: 0.5rem 1rem; font-weight: 500; }
    .stButton>button:hover { background-color: #3b82f6; }
    </style>
""", unsafe_allow_html=True)

# ============ Initialization ============
if "messages" not in st.session_state:
    data = load_history()
    st.session_state.messages = data.get("messages", [])
    st.session_state.current_content = data.get("current_content")
    st.session_state.current_file = None
    st.session_state.doc_type = "pdf"

# ============ UI Layout ============
st.markdown('<div class="main-title">📝 Document Builder</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Create professional documents with formatting and borders.</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div class="section-header">⚙️ Settings</div>', unsafe_allow_html=True)
    
    with st.expander("🔑 API Configuration", expanded=True):
        api_key = st.text_input("Groq API Key", type="password", placeholder="Enter your Groq API key")
        if api_key:
            st.success("✓ Connected")
        else:
            st.warning("⚠️ Enter API key")
    
    with st.expander("📄 Document Options"):
        doc_type = st.selectbox(
            "Format",
            ["pdf", "docx", "pptx"],
            index=0,
            key="doc_type_select"
        )
        st.session_state.doc_type = doc_type
        
        uploaded_images = st.file_uploader(
            "📸 Images (optional)",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True
        )
    
    if st.button("🔄 Reset"):
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
        os.makedirs(TEMP_DIR, exist_ok=True)
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown('<div class="section-header">💬 Chat</div>', unsafe_allow_html=True)
    chat_container = st.container(height=500, border=True)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

with col2:
    st.markdown('<div class="section-header">📥 Preview & Download</div>', unsafe_allow_html=True)
    if st.session_state.current_file:
        st.download_button(
            f"⬇️ Download {st.session_state.doc_type.upper()}",
            st.session_state.current_file,
            f"document.{st.session_state.doc_type}",
            mime={
                "pdf": "application/pdf",
                "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
            }[st.session_state.doc_type],
            key="download_btn"
        )
        
        # Display preview based on document type
        if st.session_state.doc_type == "pdf":
            if st.session_state.current_file:
                b64 = base64.b64encode(st.session_state.current_file).decode()
                st.markdown(
                    f'<iframe src="data:application/pdf;base64,{b64}" width="100%" height="700px" style="border: 1px solid #ddd;"></iframe>',
                    unsafe_allow_html=True
                )
            else:
                st.info("Generating preview...")
        else:
            st.info(f"✓ {st.session_state.doc_type.upper()} generated! Download to view.")
    else:
        st.info("💡 Generate a document by entering a prompt below.")

# Chat input
prompt = st.chat_input("e.g., 'Create a business partnership agreement'")

# ============ Handle User Input ============
if prompt:
    if not api_key:
        st.error("❌ Please enter Groq API key")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.spinner("⏳ Generating..."):
        temp_imgs = []
        try:
            content = generate_document_with_groq(
                api_key,
                st.session_state.messages[-10:],
                st.session_state.doc_type,
                prompt
            )
            
            if not content:
                raise ValueError("No content generated")
            
            st.session_state.current_content = content

            if uploaded_images:
                for img in uploaded_images:
                    img_path = os.path.join(TEMP_DIR, f"temp_{img.name}")
                    with open(img_path, "wb") as f:
                        f.write(img.getvalue())
                    temp_imgs.append(img_path)

            if st.session_state.doc_type == "pdf":
                st.session_state.current_file = generate_pdf(content, temp_imgs)
            elif st.session_state.doc_type == "docx":
                st.session_state.current_file = generate_docx(content, temp_imgs)
            else:
                st.session_state.current_file = generate_pptx(content, temp_imgs)

            response = f"✓ {st.session_state.doc_type.upper()} generated successfully!"
        
        except Exception as e:
            response = f"❌ Error: {str(e)}"
            st.session_state.current_file = None
        
        finally:
            for img in temp_imgs:
                try:
                    os.remove(img)
                except:
                    pass

        st.session_state.messages.append({"role": "assistant", "content": response})
        save_history()
        st.rerun()

# Cleanup
if os.path.exists(TEMP_DIR):
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
