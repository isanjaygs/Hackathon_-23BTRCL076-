import streamlit as st
import speech_recognition as sr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import pyttsx3
import threading

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a voice assistant just like Siri/Google Assistant. "
                              "You respond with text, which I'll convert to voice. "
                              "and your name is Dot.")
    ]

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    engine.stop()  # Ensure the engine stops completely

st.markdown("""
    <style>
        /* Background Styling */
        .stApp {
            background-color: #1E1E1E;
            color: white;
            font-family: 'Arial', sans-serif;
            text-align: center;
        }

        /* Title Styling */
        .stApp h1 {
            font-size: 36px;
            font-weight: bold;
            color: #F2F2F2;
            text-align: center;
            padding-bottom: 15px;
            font-family: 'Times New Roman', Times, serif; /* Times New Roman font */
        }

        /* Voice Input Button */
        .stButton>button {
            background-color: #4A90E2;
            color: white;
            border-radius: 30px;
            padding: 14px 28px;
            font-size: 18px;
            font-weight: bold;
            border: none;
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }

        .stButton>button:hover {
            background-color: #5DADE2;
            transform: scale(1.05);
        }

        /* Chat Container */
        .chat-container {
            max-width: 80%;
            margin: 20px auto;
            padding: 15px;
            border-radius: 10px;
            background-color: #292929;
            box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
        }

        /* Chat Bubbles */
        .user-message, .ai-message {
            padding: 12px;
            border-radius: 15px;
            max-width: 70%;
            display: inline-block;
            text-align: left;
            word-wrap: break-word;
            margin: 10px auto;
        }

        /* User Message */
        .user {
            background-color: #F2F2F2;
            color: black;
            font-weight: bold;
        }

        /* AI Message */
        .ai {
            background-color: #E0E0E0;
            color: black;
        }

        /* Listening Status */
        .listening {
            font-size: 18px;
            font-weight: bold;
            color: #FFFFFF;
            background-color: #333333;
            padding: 12px;
            border-radius: 8px;
            display: inline-block;
            margin-top: 15px;
            animation: blink 1.5s infinite;
        }

        /* Blinking effect for "Listening..." */
        @keyframes blink {
            0% {opacity: 1;}
            50% {opacity: 0.5;}
            100% {opacity: 1;}
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>AI Voice Assistant</h1>", unsafe_allow_html=True)

if st.button("   Start Voice Input", key="voice_button"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        listening_placeholder = st.empty()
        listening_placeholder.markdown('<p class="listening"> Listening...</p>', unsafe_allow_html=True)

        recognizer.adjust_for_ambient_noise(source)
        audio2 = recognizer.listen(source)

        try:
            textt = recognizer.recognize_google(audio2).lower()
            listening_placeholder.empty()

            st.markdown(f'<div class="chat-container user"> <b>You said:</b> {textt} </div>', unsafe_allow_html=True)

            hmsg = HumanMessage(content=textt)
            st.session_state.chat_history.append(hmsg)

            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",  google_api_key="Enter your API key"
            )
            response = llm.invoke(st.session_state.chat_history)
            ai_response = response.content

            st.markdown(f'<div class="chat-container ai"> <b>AI:</b> {ai_response} </div>', unsafe_allow_html=True)

            # Directly call speak_text instead of using threading
            speak_text(ai_response)

            st.session_state.chat_history.append(AIMessage(content=ai_response))

        except sr.UnknownValueError:
            listening_placeholder.empty()
            st.markdown('<p class="st-bf">⚠️ Sorry, I couldn\'t understand the audio.</p>', unsafe_allow_html=True)
        except sr.RequestError as e:
            listening_placeholder.empty()
            st.markdown(f'<p class="st-bf">❌ Error with speech recognition: {e}</p>', unsafe_allow_html=True)
