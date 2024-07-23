import streamlit as st
import streamlit.components.v1 as components
from menu import menu

def main():
    st.title("Breathing Exercise")
    menu()

    html_title = """ 
    <h1 style ="color:black; text-align:center;">Simple Breathing Exercise</h1>
    """
    st.markdown(html_title, unsafe_allow_html = True) 

    css = r'''
    <style>
        #audio {display: none;}
    </style>
    '''
    st.markdown(css, unsafe_allow_html=True)
    components.iframe("https://datjandra.github.io/taijiflow/breathing.html", height=500)

    default_audio_url = "https://freepd.com/music/Infinite%20Wonder.mp3"
    audio_url = st.text_input("MP3 Audio URL", value=default_audio_url)
    if audio_url:
        st.audio(audio_url, format="audio/mpeg", loop=True, autoplay=True)

if __name__ == "__main__":
    main()
