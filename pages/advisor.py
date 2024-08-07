import os
import streamlit as st
import google.generativeai as genai
from menu import menu

GEM_MODEL = os.getenv('GEM_MODEL')
GEM_CHAT_PROMPT = os.getenv('GEM_CHAT_PROMPT')
GEM_CONFIG_TEMPERATURE = float(os.getenv('GEM_CONFIG_TEMPERATURE'))
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
if GEM_CONFIG_TEMPERATURE < 0:
    model = genai.GenerativeModel(GEM_MODEL, system_instruction=GEM_CHAT_PROMPT)
else:
    model = genai.GenerativeModel(
        GEM_MODEL,
        system_instruction=GEM_CHAT_PROMPT,
        generation_config={
            "temperature": GEM_CONFIG_TEMPERATURE
        }
    )

if "history" not in st.session_state:
  st.session_state.history = []
  
def main():
  st.set_page_config(page_title="Healthy Aging Advisor")
  st.title("Healthy Aging Advisor")
  menu()

  chat = model.start_chat(history=st.session_state.history)
  for message in chat.history:
    role = 'assistant' if message.role == 'model' else message.role
    with st.chat_message(role):
      st.markdown(message.parts[0].text)
  
  if input := st.chat_input("Enter your wellness goal or question"):
    with st.chat_message("user"):
      st.markdown(input)
  
    with st.chat_message("advisor"):
      with st.spinner('Thank you for your input...'):
        response = chat.send_message(input)
        for chunk in response:
          st.markdown(chunk.text)
        st.session_state.history = chat.history  

if __name__ == "__main__":
    main()
