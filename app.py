import os
import requests
import streamlit as st

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
from functools import lru_cache

USER_ID = 'openai'
APP_ID = 'chat-completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = os.environ.get('MODEL_ID')
MODEL_VERSION_ID = os.environ.get('MODEL_VERSION_ID')
PAT = os.environ.get('PAT')
SEARCH_OPTIONS = [option.strip() for option in os.environ.get('SEARCH_OPTIONS').split(",") if option.strip()]

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

TL_KEY = os.getenv('TL_KEY')
TL_INDEX = os.getenv('TL_INDEX')
PROMPT = os.getenv('PROMPT')

# Function to simplify text
@lru_cache(maxsize=128)
def condition_to_exercise(condition):
    prompt = f"{PROMPT} {condition}"
    post_model_outputs_response = stub.PostModelOutputs(
        service_pb2.PostModelOutputsRequest(
            user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
            model_id=MODEL_ID,
            version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                            # url=TEXT_FILE_URL
                            # raw=file_bytes
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    output = post_model_outputs_response.outputs[0]
    return output.data.text.raw

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
        "search_options": SEARCH_OPTIONS,
        "adjust_confidence_level": 0.5,
        "group_by": "video",
        "threshold": "low",
        "sort_option": "score",
        "operator": "or",
        "conversation_option": "semantic",
        "page_limit": 1,
        "query": query,
        "index_id": TL_INDEX
    }
    
    headers = {
        "accept": "application/json",
        "x-api-key": TL_KEY,
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    #response_text = response.text
    #os.write(1, '{}\n'.format(response_text).encode())
    
    response_json = response.json()
    if 'data' in response_json and isinstance(response_json['data'], list) and len(response_json['data']) > 0:
        first_data = response_json['data'][0]
        if 'clips' in first_data and isinstance(first_data['clips'], list) and len(first_data['clips']) > 0:
            video = first_data['clips'][0]
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
    return None

def main():
    st.set_page_config(page_title="Supreme Ultimate Flow", page_icon='☯️')
    html_title = """ 
    <div style ="background-color:white; padding:13px;"> 
    <h1 style ="color:black; text-align:center;">TaijiFlow</h1> 
    </div> 
    """
    st.markdown(html_title, unsafe_allow_html = True) 
    st.image("https://raw.githubusercontent.com/datjandra/taijiflow/main/baduanjin.jpg")

    css = r'''
    <style>
        [data-testid="stForm"] {border: 0px;}
        .row-widget.stButton {text-align: center;}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
    
    with st.form("user_input_form"):
        condition = st.text_input(label="", placeholder="Enter a medical condition or vital function you want to address", label_visibility="collapsed")
        submit_button = st.form_submit_button(label='Search')

    if submit_button:
        pl_text = st.empty()
        pl_video = st.empty()
        
        exercise = condition_to_exercise(condition)        
        pl_text.write(exercise)
        
        video_info = video_search(exercise)
        if video_info:
            pl_video.video(video_info["video_url"], start_time=video_info["start"], end_time=video_info["end"])
        else:
            pl_video.markdown("No matching video found, please retry or rewrite the query.")
        
if __name__ == "__main__":
    main()
