import os
import requests
import streamlit as st

TL_KEY = os.getenv('TL_KEY')
TL_INDEX = os.getenv('TL_INDEX')

def video_search(query):
    url = "https://api.twelvelabs.io/v1.2/search"

    payload = {
        "search_options": ["visual"],
        "adjust_confidence_level": 0.5,
        "group_by": "clip",
        "threshold": "low",
        "sort_option": "score",
        "operator": "or",
        "conversation_option": "semantic",
        "page_limit": 10,
        "query": "query,
        "index_id": TL_INDEX
    }
    
    headers = {
        "accept": "application/json",
        "x-api-key": TL_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    if response_json.get('data'):
        video = response_json.get('data')[0]
        video_id = video['video_id']
        video_start = video['start']
        video_end = video['end]

def main():
    st.title("TaijiFlow")

    with st.form("user_input_form"):
        conditions = st.text_input("Conditions")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        st.video("https://youtu.be/q8yZSfAOonI", start_time=24, end_time=42)

if __name__ == "__main__":
    main()
