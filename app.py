import os
import streamlit as st

def main():
    st.title("TaijiFlow")

    with st.form("user_input_form"):
        conditions = st.text_input("Conditions")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.video("https://youtu.be/q8yZSfAOonI", start_time=24, end_time=42)

if __name__ == "__main__":
    main()
