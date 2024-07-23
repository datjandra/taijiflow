import streamlit as st
import plotly.graph_objects as go
from menu import menu

def main():
  st.set_page_config(page_title="Progress Tracking")
  st.title("Wellness Score")
  menu()

if __name__ == "__main__":
  main()
