import streamlit as st

def menu():
  st.sidebar.page_link("app.py", label="🏠 Home")
  st.sidebar.page_link("pages/advisor.py", label="👵 Healthy Aging Advisor")
  st.sidebar.page_link("pages/analysis.py", label="🖼️ Posture Analysis")
  st.sidebar.page_link("pages/breathing.py", label="🕊️ Breathing Exercise")
