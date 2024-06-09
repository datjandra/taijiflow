import os
import requests
import streamlit as st

TL_KEY = os.getenv('TL_KEY')
TL_INDEX = os.getenv('TL_INDEX')

def source_url(video_id):
    url = f"https://api.twelvelabs.io/v1.2/indexes/{TL_INDEX}/videos/{video_id}"

    headers = {
        "accept": "application/json",
        "x-api-key": TL_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response_json = response.json()
    if 'source' in response_json:
        return response_json['source']['url']
    else:
        return None

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
        "query": query,
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
        video_end = video['end']
        video_url = source_url(video_id)

        if video_url:
            result = {
                "video_url": video_url,
                "start": video_start,
                "end": video_end
            }
            return result
    return None

def main():
    st.title("TaijiFlow")

    with st.form("user_input_form"):
        conditions = st.text_input("Conditions")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        video_info = video_search(conditions)
        if video_info:
            st.video(video_info["video_url"], start_time=video_info["start"], end_time=video_info["end"])
        else:
            st.markdown("No matching video clip found, please try another query.")

if __name__ == "__main__":
    main()
