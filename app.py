import os
import requests
import streamlit as st

TL_KEY = os.getenv('TL_KEY')
TL_INDEX = os.getenv('TL_INDEX')

def main():
    st.title("TaijiFlow")

    with st.form("user_input_form"):
        conditions = st.text_input("Conditions")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.video("https://youtu.be/q8yZSfAOonI", start_time=24, end_time=42)

if __name__ == "__main__":
    main()
