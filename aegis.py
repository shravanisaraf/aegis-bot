import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# Programmatically set the API key (Replace with your actual API key)
os.environ['GEMINI_API_KEY'] = 'AIzaSyA6ZRuYPgsPAqjDEhIgXCUft176Xmv0C9k'
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Initialize the GenerativeModel
model = genai.GenerativeModel('gemini-1.5-flash')

# Function to interact with the chatbot
def chat_with_bot(user_input):
    # Initialize a new chat session (history can be used to track past conversations if needed)
    chat = model.start_chat(history=[])
    
    # Send the user message and get the response
    response = chat.send_message(user_input)
    
    # Return the bot's text response
    return response.text

# Set up the Streamlit app
st.set_page_config(page_title="Aegis Chatbot", layout="centered")
st.title("Welcome to Aegis - Your Gemini-powered Chatbot")

# Session state to store chat history across user inputs
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Input box for the user to type their message
user_input = st.text_input("Type your message and press Enter:")

# Display chat history
st.write("### Chat History:")
for msg in st.session_state['messages']:
    if msg['role'] == 'user':
        st.write(f"**You**: {msg['content']}")
    else:
        st.write(f"**Bot**: {msg['content']}")

# Process user input and display bot response
if user_input:
    # Append the user's message to chat history
    st.session_state['messages'].append({"role": "user", "content": user_input})
    
    # Generate a response from the bot
    bot_response = chat_with_bot(user_input)
    
    # Append the bot's response to chat history
    st.session_state['messages'].append({"role": "bot", "content": bot_response})
    
    # Re-render the chat history
    st.write("### Chat History:")
    for msg in st.session_state['messages']:
        if msg['role'] == 'user':
            st.write(f"**You**: {msg['content']}")
        else:
            st.write(f"**Bot**: {msg['content']}")

# Extra Feature: User profile information
with st.sidebar:
    st.header("User Profile")
    name = st.text_input("Name:")
    if name:
        st.write(f"Hello, {name}!")
    
    mood = st.selectbox("How are you feeling?", ["Happy", "Sad", "Neutral"])
    st.write(f"You're feeling {mood.lower()} today.")

# Display the time of the last message sent
if st.session_state['messages']:
    st.sidebar.write(f"Last message sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
