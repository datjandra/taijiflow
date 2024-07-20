import os
import streamlit as st
import google.generativeai as genai

GEM_MODEL = os.getenv('GEM_MODEL')
GEM_CHAT_PROMPT = os.getenv('GEM_CHAT_PROMPT')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(GEM_MODEL, system_instruction=GEM_CHAT_PROMPT)
chat = model.start_chat(history=[])

st.set_page_config(page_title="Healthy Aging Advisor")
st.title("Healthy Aging Advisor")
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/advisor.py", label="👵 Healthy Aging Advisor")
st.sidebar.page_link("pages/analysis.py", label="🖼️ Posture Analysis")

for message in chat.history:
  with st.chat_message(message.role):
    st.markdown(message.parts[0].text)

if input := st.chat_input("Enter your wellness goal"):
  with st.chat_message("user"):
    st.markdown(input)

  with st.chat_message("advisor"):
    with st.spinner('Thank you for your input...'):
      response = chat.send_message(input)
      for chunk in response:
        st.markdown(chunk.text)
