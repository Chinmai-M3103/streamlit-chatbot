import os 
os.environ["GOOGLE_API_KEY"]=st.secret["GOOGLE_API_KEY"]
import streamlit as st
st.title("streamlit chatbot")
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful assistant.")
    ]
if "messages_display" not in st.session_state:
    st.session_state.messages_display = []

# Streamlit UI
st.title("🧠 Gemini Chat with LangChain")
st.markdown("Talk to Gemini 2.0 Flash model via LangChain")

# Display previous messages
for msg in st.session_state.messages_display:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user message
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    st.session_state.messages_display.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get response from model
    response = llm.invoke(st.session_state.chat_history)
    ai_content = response.content

    # Append AI response
    st.session_state.chat_history.append(AIMessage(content=ai_content))
    st.session_state.messages_display.append({"role": "assistant", "content": ai_content})
    with st.chat_message("assistant"):
        st.markdown(ai_content)

