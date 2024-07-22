import streamlit as st
import streamlit.components.v1 as components

def main():
    html_title = """ 
    <h1 style ="color:black; text-align:center;">Simple Breathing Exercise</h1>
    """
    st.markdown(html_title, unsafe_allow_html = True) 
    components.iframe("https://datjandra.github.io/taijiflow/breathing.html", height=500)

if __name__ == "__main__":
    main()
