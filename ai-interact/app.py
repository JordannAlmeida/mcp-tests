import streamlit as st
from chat_logic import ChatLogic
from llm.type_llm import LLMType
import io

# --- Page Configuration ---
st.set_page_config(page_title="Gemini Chat", layout="wide")

# --- Load API Key and Initialize Model ---

chat_logic: ChatLogic = None

try:
    chat_logic = ChatLogic()
except ValueError as e:
    st.error(e)
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred during initialization: {e}")
    st.stop()

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [] # Stores chat messages: {"role": "user/assistant", "content": "message"}
if "llm_type" not in st.session_state:
    st.session_state.llm_type = LLMType.GEMINI.name

# --- UI Elements ---
st.title("Chat with Gemini ♊")

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    llm_type_options = [llm_type.name for llm_type in LLMType]
    selected_llm_type = st.selectbox("Select LLM Type", llm_type_options, index=llm_type_options.index(st.session_state.llm_type))
    if selected_llm_type != st.session_state.llm_type:
        st.session_state.llm_type = selected_llm_type
    if st.button("New Chat", key="new_chat_button"):
        st.session_state.messages = []
        chat_logic.start_new_chat(LLMType[st.session_state.llm_type])
        st.rerun()

# --- Chat Interface ---
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("What would you like to ask Gemini?")

# Place file uploader below chat input
st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)  # Spacer for better UI
allowed_types = ["pdf", "csv", "xlsx", "xls"]
uploaded_files = st.file_uploader(
    "Upload files", type=allowed_types, accept_multiple_files=True, label_visibility="collapsed"
)

# Enforce max 3 files
if uploaded_files and len(uploaded_files) > 3:
    st.error("You can upload a maximum of 3 files.")
    uploaded_files = uploaded_files[:3]

# Additional validation for file extensions (in case of browser bypass)
invalid_files = []
if uploaded_files:
    for f in uploaded_files:
        if not any(f.name.lower().endswith(f'.{ext}') for ext in allowed_types):
            invalid_files.append(f.name)

if invalid_files:
    st.error(f"The following files are not allowed: {', '.join(invalid_files)}. Please upload only PDF, CSV, XLSX, or XLS files.")
    uploaded_files = [f for f in uploaded_files if f.name not in invalid_files]

if prompt:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        if uploaded_files:
            st.markdown(f"**Uploaded {len(uploaded_files)} file(s)**")

    # Prepare files as BytesIO
    files_io = [{"name": f.name , "stream": io.BytesIO(f.read())} for f in uploaded_files] if uploaded_files else []

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            response = chat_logic.get_response(prompt, files=files_io)
            st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

