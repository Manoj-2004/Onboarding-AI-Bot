import csv
import google.generativeai as genai
import streamlit as st
import os
from dotenv import load_dotenv
from utils import read_csv_file

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

questions = read_csv_file()

# Streamlit app function
def main():
    st.set_page_config(page_title="Rosa AI Onboarding", page_icon="🤖", layout="centered")
    
    st.markdown("""
        <style>
        .chat-bubble {
            padding: 10px;
            margin: 10px;
            border-radius: 5px;
            width: fit-content;
        }
        .bot {
            background-color: #f0f0f5;
            color: #000000;
        }
        .user {
            background-color: #0084ff;
            color: #ffffff;
            align-self: flex-end;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Rosa AI Onboarding Process")

    st.write("Welcome to Rosa AI's onboarding process! Let's get started with a few questions.")
    
    if 'question_index' not in st.session_state:
        st.session_state.question_index = 0

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'user_responses' not in st.session_state:
        st.session_state.user_responses = []

    # Display chat history with styling
    for chat in st.session_state.chat_history:
        if chat.startswith("Bot:"):
            st.markdown(f'<div class="chat-bubble bot">{chat}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble user">{chat}</div>', unsafe_allow_html=True)

    if st.session_state.question_index < len(questions):
        question = questions[st.session_state.question_index]
        st.markdown(f'<div class="chat-bubble bot">Bot: {question}</div>', unsafe_allow_html=True)

        user_response = st.text_input("You:", key='response')

        col1, col2 = st.columns([4, 1])
        with col1:
            st.write("")
        with col2:
            if st.button("Submit"):
                st.session_state.chat_history.append(f"Bot: {question}")
                st.session_state.chat_history.append(f"You: {user_response}")
                st.session_state.user_responses.append({"question": question, "response": user_response})
                st.session_state.question_index += 1

                # Save responses to file
                with open('onboarding_data.csv', 'a', newline='') as csvfile:
                    fieldnames = ['question', 'response']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    if csvfile.tell() == 0:
                        writer.writeheader()
                    writer.writerow({"question": question, "response": user_response})

                st.rerun()  # Rerun the app to update the chat history

        # Calculate progress
        progress = (st.session_state.question_index + 1) / len(questions)
        st.progress(progress)

    else:
        st.markdown("Thank you for answering the questions. For questions outside of this onboarding process, please schedule a call with the founders or email them at founders@Rosa.ai.")

if __name__ == "__main__":
    main()