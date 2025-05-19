import streamlit as st
import chat_logic

# --- Page Configuration ---
st.set_page_config(page_title="Gemini Chat", layout="wide")

# --- Load API Key and Initialize Model ---
api_key = ''
chat = None
try:
    api_key = chat_logic.load_api_key()
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        st.error("Google API Key not found or not configured. Please set it in the .env file.")
        st.stop()
    chat = chat_logic.start_new_chat(api_key)
except ValueError as e:
    st.error(e)
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred during initialization: {e}")
    st.stop()

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [] # Stores chat messages: {"role": "user/assistant", "content": "message"}

# --- UI Elements ---
st.title("Chat with Gemini ♊")

# Sidebar for controls
with st.sidebar:
    st.header("Controls")
    if st.button("New Chat", key="new_chat_button"):
        st.session_state.messages = []
        chat = chat_logic.start_new_chat(api_key)
        st.rerun()

# --- Chat Interface ---
# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("What would you like to ask Gemini?")

if prompt:
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Gemini is thinking..."):
            response = chat_logic.generate_response(chat, prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

