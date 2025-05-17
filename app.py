import os
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Load API key from Streamlit secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Initialize LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Page setup
st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("🤖 Gemini Chatbot with Memory")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful assistant.")
    ]

# Clear chat option
if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = [SystemMessage(content="You are a helpful assistant.")]
    st.rerun()

# Show chat history
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").markdown(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").markdown(msg.content)

# User input
user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.chat_message("user").markdown(user_input)

    try:
        result = llm.invoke(st.session_state.chat_history)
        response = result.content
    except Exception as e:
        response = "⚠️ Sorry, something went wrong."
        st.error(str(e))

    st.session_state.chat_history.append(AIMessage(content=response))
    st.chat_message("assistant").markdown(response)
