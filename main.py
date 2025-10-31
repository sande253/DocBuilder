import streamlit as st
import base64

st.set_page_config(page_title="Chat + PDF Preview", layout="wide")

# Initialize session state for chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"sender": "bot", "text": "Hello — upload a PDF on the right and ask me questions about it!"}
    ]

# Inject CSS to make the app layout fixed and only chat scrollable
st.markdown("""
    <style>
    /* Prevent whole page from scrolling */
    .main > div {
        overflow: hidden !important;
    }

    /* Make chat area scrollable */
    .chat-box {
        height: 750px;
        overflow-y: auto;
        border: 1px solid #ddd;
        padding: 10px;
        border-radius: 10px;
        background-color: #fafafa;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📄 PDF Preview — 💬 Chat Assistant")

# Sidebar slider to adjust width
left_pct = st.sidebar.slider("Left pane width (%)", min_value=20, max_value=80, value=40, step=1)

# Column layout
left_ratio = left_pct
right_ratio = 100 - left_pct
left_col, right_col = st.columns([left_ratio, right_ratio])

# --- RIGHT SIDE: PDF Preview ---
with right_col:
    st.header("Document preview")
    uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])
    url = st.text_input("Or paste a URL to a PDF (optional)", value="")

    pdf_bytes = None
    pdf_url = None

    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
    elif url.strip():
        pdf_url = url.strip()

    pdf_container_height = 850

    if pdf_bytes:
        b64 = base64.b64encode(pdf_bytes).decode("utf-8")
        pdf_data = f"data:application/pdf;base64,{b64}"
        st.components.v1.html(
            f"<iframe src=\"{pdf_data}\" width=\"100%\" height=\"{pdf_container_height}px\"></iframe>",
            height=pdf_container_height
        )
    elif pdf_url:
        st.components.v1.html(
            f"<iframe src=\"{pdf_url}\" width=\"100%\" height=\"{pdf_container_height}px\"></iframe>",
            height=pdf_container_height
        )
    else:
        st.write("No PDF loaded. Upload one or paste a PDF URL to preview it here.")

# --- LEFT SIDE: Chat ---
with left_col:
    st.header("Chat assistant")

    # Scrollable chat area
    messages_html = ""
    for msg in st.session_state.messages:
        if msg["sender"] == "user":
            messages_html += f"<p><b>You:</b> {msg['text']}</p>"
        else:
            messages_html += f"<p><b>Bot:</b> {msg['text']}</p>"

    st.markdown(f"<div class='chat-box'>{messages_html}</div>", unsafe_allow_html=True)

    # Chat input area (fixed below)
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask a question about the document or anything else:")
        submitted = st.form_submit_button("Send")

        if submitted and user_input:
            st.session_state.messages.append({"sender": "user", "text": user_input})

            # Simple placeholder logic
            if pdf_bytes:
                bot_reply = (
                    "I can see a PDF was uploaded. I can help summarize or find keywords — "
                    "(this is a placeholder response). Try asking: 'Summarize the document' or 'Find occurrences of tax'."
                )
            elif url.strip():
                bot_reply = "I can preview a PDF from the provided URL. Ask me questions about it."
            else:
                bot_reply = "You didn't load a PDF yet — I can still chat or help with general questions."

            st.session_state.messages.append({"sender": "bot", "text": bot_reply})
            st.experimental_rerun()

# Sidebar info
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Usage:**
1. Adjust left pane width using the slider.
2. Upload or link a PDF on the right.
3. Chat on the left — scroll inside the chat box.
""")

st.sidebar.info("Run locally: `streamlit run main.py`")
