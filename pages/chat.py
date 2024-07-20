import streamlit as st
import google.generativeai as genai

GEM_MODEL = os.getenv('GEM_MODEL')
GEM_CHAT_PROMPT = os.getenv('GEM_CHAT_PROMPT')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(GEM_MODEL, system_instruction=GEM_CHAT_PROMPT)
chat = model.start_chat(history=[])

st.title("Healthy Aging Advisor")
for message in chat.history:
  with st.chat_message(message["role"]):
    st.markdown(message["text"])

if input := st.chat_input("Enter your wellness goal"):
  with st.chat_message("user"):
    st.markdown(input)

with st.chat_message("advisor"):
  response = chat.send_message(input, stream=True)
  for chunk in response:
    st.write_stream(chunk.text)
