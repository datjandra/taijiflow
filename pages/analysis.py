import os
import streamlit as st

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2

USER_ID = 'openai'
APP_ID = 'chat-completion'
# Change these to whatever model and text URL you want to use
MODEL_ID = os.environ.get('VIS_MODEL_ID')
MODEL_VERSION_ID = os.environ.get('VIS_MODEL_VERSION_ID')
PAT = os.environ.get('PAT')
PROMPT = os.getenv('VIS_ZZ_PROMPT')

channel = ClarifaiChannel.get_grpc_channel()
stub = service_pb2_grpc.V2Stub(channel)
metadata = (('authorization', 'Key ' + PAT),)
userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)
    
def main():
    st.set_page_config(page_title="Posture Analysis")
    st.title("Standing Posture Analysis")
    st.sidebar.page_link("app.py", label="Home")
    st.sidebar.page_link("pages/advisor.py", label="Healthy Aging Advisor")
    st.sidebar.page_link("pages/analysis.py", label="Posture Analysis")

    uploaded_file = st.file_uploader("Please upload a picture of your standing posture")
    if uploaded_file is not None:
      bytes_data = uploaded_file.getvalue()

      with st.spinner('Analyzing image of posture...'):  
          post_model_outputs_response = stub.PostModelOutputs(
              service_pb2.PostModelOutputsRequest(
                  user_app_id=userDataObject,  # The userDataObject is created in the overview and is required when using a PAT
                  model_id=MODEL_ID,
                  version_id=MODEL_VERSION_ID,  # This is optional. Defaults to the latest model version
                  inputs=[
                      resources_pb2.Input(
                          data=resources_pb2.Data(
                              text=resources_pb2.Text(
                                  raw=PROMPT
                              ),
                              image=resources_pb2.Image(
                                  base64=bytes_data
                              )
                          )
                      )
                  ]
              ),
              metadata=metadata
          )
          
          if (post_model_outputs_response.status.code != status_code_pb2.SUCCESS):
              output = f"Post model outputs failed, status: {post_model_outputs_response.status.description}"
              st.write(output)
          else:
              output = post_model_outputs_response.outputs[0]
              st.markdown(output.data.text.raw)
      
if __name__ == "__main__":
    main()
