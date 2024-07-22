import streamlit as st
import streamlit.components.v1 as components

def main():
    st.title("Simple Breathing Exercise")
    components.iframe("https://datjandra.github.io/taijiflow/breathing.html", height=500)

if __name__ == "__main__":
    main()
