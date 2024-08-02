import os
import requests
import streamlit as st
from itertools import cycle
from functools import lru_cache
import google.generativeai as genai
from menu import menu
from xml.etree import ElementTree

GEM_MODEL = os.getenv('GEM_MODEL')
GEM_EXERCISE_PROMPT = os.getenv('GEM_EXERCISE_PROMPT')
GEM_CONFIG_TEMPERATURE = float(os.getenv('GEM_CONFIG_TEMPERATURE'))
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SEARCH_OPTIONS = [option.strip() for option in os.environ.get('SEARCH_OPTIONS').split(",") if option.strip()]

genai.configure(api_key=GOOGLE_API_KEY)
if GEM_CONFIG_TEMPERATURE < 0:
    model = genai.GenerativeModel(GEM_MODEL, system_instruction=GEM_EXERCISE_PROMPT)
else:
    model = genai.GenerativeModel(
        GEM_MODEL,
        system_instruction=GEM_EXERCISE_PROMPT,
        generation_config={
            "temperature": GEM_CONFIG_TEMPERATURE
        }
    )

TL_KEY = os.getenv('TL_KEY')
TL_INDEX = os.getenv('TL_INDEX')

TL_API_HEADERS = {
    "accept": "application/json",
    "x-api-key": TL_KEY,
    "Content-Type": "application/json"
}

def create_pubmed_query(medical_condition=None, lifestyle_risks=None, wellness_goal=None):
    query = f'("tai chi" OR "qigong")'
    
    if medical_condition or lifestyle_risks or wellness_goal:
        sub_clause = []
        if medical_condition:
            sub_clause.append(f'"{medical_condition}"')
        if lifestyle_risks:
            sub_clause.append(f'"{lifestyle_risks}"')
        if wellness_goal:
            sub_clause.append(f'"{wellness_goal}"')
        
        sub_clause_str = ' OR '.join(sub_clause)
        query += f' AND ({sub_clause_str})'
    return query

def search_pubmed(medical_condition=None, lifestyle_risks=None, wellness_goal=None):
    query = create_pubmed_query(medical_condition, lifestyle_risks, wellness_goal)    
    encoded_query = requests.utils.quote(query)
    
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': encoded_query,
        'retmode': 'json',
        'retmax': 1
    }
    
    response = requests.get(url, params=params)
    response.raise_for_status()  
    
    data = response.json()
    pubmed_ids = data.get('esearchresult', {}).get('idlist', [])
    return pubmed_ids

def fetch_pubmed_data(pubmed_id):
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': pubmed_id,
        'retmode': 'xml',
        'rettype': 'abstract'
    }

    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise an exception for HTTP errors

    root = ElementTree.fromstring(response.content)
    article = root.find('.//PubmedArticle')
    if article is None:
        return None, None, None

    title_elem = article.find('.//ArticleTitle')
    abstract_elem = article.find('.//Abstract/AbstractText')
    link = f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}/"

    title = title_elem.text if title_elem is not None else 'No title available'
    abstract = abstract_elem.text if abstract_elem is not None else 'No abstract available'
    return link, title, abstract

@lru_cache(maxsize=128)
def profile_to_exercise(age, gender, height, weight, conditions, risks, goal, title, abstract):
    conditions = conditions if conditions else "None"
    risks = risks if risks else "None"
    goal = goal if goal else "None"
    
    profile = f"""
    Age: {age}
    Gender: {gender}
    Height: {height} inches
    Weight: {weight} pounds
    Conditions: {conditions}
    Risks: {risks}
    Goal: {goal}

    Title:
    {title}

    Abstract:
    {abstract}
    """
    
    try:
        response = model.generate_content(profile)
        return response.text
    except:
        return "Unable to suggest a relevant exercise. Please rewrite query or try again later."
    
@lru_cache(maxsize=128)
def source_url(video_id):
    url = f"https://api.twelvelabs.io/v1.2/indexes/{TL_INDEX}/videos/{video_id}"    
    response = requests.get(url, headers=TL_API_HEADERS)
    response_json = response.json()
    if 'source' in response_json:
        return response_json['source']['url']
    else:
        return None

@lru_cache(maxsize=128)
def video_search(query):
    url = "https://api.twelvelabs.io/v1.2/search"

    payload = {
        "search_options": SEARCH_OPTIONS,
        "adjust_confidence_level": 0.5,
        "sort_option":"score",
        "operator":"or",
        "conversation_option":"semantic",
        "group_by": "clip",
        "threshold": "low",
        "page_limit": 8,
        "query": query,
        "index_id": TL_INDEX
    }

    response = requests.post(url, json=payload, headers=TL_API_HEADERS)    
    response_json = response.json()

    clips = []
    for item in response_json.get('data', []):
        video_id = item.get('video_id')
        video_url = source_url(video_id)
        start = item.get('start')
        end = item.get('end')
        clips.append({
            'video_url': video_url,
            'start': start,
            'end': end
        })
    return clips

def main():
    st.set_page_config(page_title="Supreme Ultimate Flow", page_icon='☯️')
    menu()

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
    st.markdown("### Please fill in the form below to get a personalized exercise suggestion.")
    
    with st.form("user_input_form"):
        age = st.number_input("Age", min_value=1, max_value=150, value=65, step=1)
        gender = st.selectbox("Gender", ["Male", "Female"])
        weight = st.number_input("Weight (pounds)", min_value=30, max_value=1500, value=200, step=1)
        height = st.number_input("Height (inches)", min_value=20, max_value=110, value=70, step=1)
        conditions = st.text_input(label="Medical Conditions", placeholder="Enter any medical conditions (e.g., high blood pressure)")
        risks = st.text_input(label="Lifestyle Risks", placeholder="Enter any lifestyle risks (e.g., smoker)")
        goal = st.text_input(label="Wellness Goal", placeholder="Enter your wellness goal (e.g., strong immune system)")
        submit_button = st.form_submit_button(label='Go')

    if submit_button:
        pl_text = st.empty()
        pl_disclaimer = st.empty()

        with st.spinner('Suggesting a relevant exercise...'):
            pubmed_ids = search_pubmed(conditions, risks, goal)
            link, title, abstract = fetch_pubmed_data(pubmed_ids[0])
            exercise = profile_to_exercise(age, gender, height, weight, conditions, risks, goal, title, abstract)        
        pl_text.write(exercise)

        with st.spinner('Finding example video clips...'):    
            clips = video_search(exercise)
            
        if clips:
            if link and title:
                st.markdown(f"[{title}]({link})")
    
            cols = cycle(st.columns(2)) 
            for clip in clips:
                next(cols).video(clip["video_url"], start_time=clip["start"], end_time=clip["end"])
            pl_disclaimer.markdown("These exercises are not intended to replace professional medical advice, diagnosis, or treatment. Please consult your healthcare provider with any questions or concerns regarding your health.")    
        else:
            st.markdown("No example video clips found, please retry or rewrite the query.")
        
if __name__ == "__main__":
    main()
