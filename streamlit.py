import random
import streamlit as st
import difflib  # For smart matching

# Set page configuration
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
    }
    .chat-box {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    .stButton>button {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Predefined responses
responses = {
    "hello": ["Hi there! How can I help you?", "Hello! Hope you're having a great day! 😊"],
    "hi": ["Hi there! How can I help you?", "Hello! Hope you're having a great day! 😊"],
    "what's your name": ["I'm AI Chatbot, your friendly assistant! 🤖"],
    "who created you": ["I was created by Engr Sir Abdul Rehman Ansari! A full-stack developer. 👨‍💻"],
    "tell me a joke": ["Why don’t scientists trust atoms? Because they make up everything! 😂", 
                        "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾😆"],
    "goodbye": ["Bye! Have a great day! 😊", "Goodbye! See you next time! 👋"],
    "how are you": ["I'm just a bot, but I'm doing great! How about you? 😊"],
    "what can you do": ["I can chat with you, tell jokes, remember your inputs, and learn new responses! 🤖"],
    "where are you from": ["I live in the world of the internet! ☁️"],
    "what is your purpose": ["My purpose is to assist and entertain you! 😊"]
}

# Persistent memory for user-trained responses
if "user_responses" not in st.session_state:
    st.session_state.user_responses = {}
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = []

def chatbot_response(user_input):
    user_input = user_input.lower().strip()
    st.session_state.chat_memory.append(f"You: {user_input}")
    
    # Check user-defined responses
    if user_input in st.session_state.user_responses:
        response = random.choice(st.session_state.user_responses[user_input])
        st.session_state.chat_memory.append(f"Chatbot: {response}")
        return response
    
    # Smart matching with predefined responses
    match = difflib.get_close_matches(user_input, responses.keys(), n=1, cutoff=0.5)
    if match:
        response = random.choice(responses[match[0]])
        st.session_state.chat_memory.append(f"Chatbot: {response}")
        return response
    
    return "I don't understand that yet. Try rephrasing or teach me! Type 'train: your message = my response'"

# Streamlit UI
st.title("🤖 AI Chatbot")
st.write("Chat with me! Type your message below.")

# User input
user_message = st.text_input("You:", "")

if user_message:
    if user_message.lower() == "exit":
        st.write("Chatbot: Goodbye! 👋")
    elif user_message.lower().startswith("train:"):
        try:
            parts = user_message[6:].split("=")
            user_msg = parts[0].strip().lower()
            bot_response = parts[1].strip()
            if user_msg and bot_response:
                if user_msg in st.session_state.user_responses:
                    st.session_state.user_responses[user_msg].append(bot_response)
                else:
                    st.session_state.user_responses[user_msg] = [bot_response]
                st.write("Chatbot: Thanks for teaching me! 😊")
        except:
            st.write("Chatbot: Invalid format. Use 'train: your message = my response'")
    else:
        bot_reply = chatbot_response(user_message)
        st.write(f"Chatbot: {bot_reply}")

# Display chat history
st.subheader("📝 Chat History")
st.write("\n".join(st.session_state.chat_memory))

# Button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_memory = []
    st.write("Chat history cleared!")
