import os
import streamlit as st
import streamlit.components.v1 as components

POSE_URL = os.getenv('POSE_URL')

def main():
    st.set_page_config(page_title="Posture Analysis")
    components.iframe(POSE_URL, height=700)
      
if __name__ == "__main__":
    main()
