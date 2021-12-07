from skills_matcher.app import SessionState
from io import StringIO
import PyPDF2
import os
import pandas as pd
import streamlit as st
import SessionState
from skills_matcher.scripts.spacy_model import load_results_manual, load_results_auto
#from skills_matcher.scripts.utils.geolocation import geo

PATH = os.path.dirname(os.path.dirname(__file__))
#load csv
data = pd.read_csv(PATH + '/data/data_final_raw.csv')
#convert to countries
#data['location'] = data['location'].apply(geo)
categories = list(data.groupby('job').count().index)
locations = list(data.groupby('location').count().index)
locations.append('Europe')
skills = ['Python', 'JavaScript', 'AWS', 'R']
knowledges = ['Software Engineer', 'Finance', 'Economics']

def read_pdf(file):
    pdfReader = PyPDF2.PdfFileReader(file)
    count = pdfReader.numPages
    all_page_text = ""
    for i in range(count):
        page = pdfReader.getPage(i)
        all_page_text += page.extractText()

    return all_page_text


st.sidebar.title("Pages")
radio = st.sidebar.radio(label="",
        options=["Skills Matcher", "I'm a Recruiter", "I'm looking for a job"])

session_state = SessionState.get()  # Pick some initial values.

if radio == 'Skills Matcher':

    image = st.image('https://im2.ezgif.com/tmp/ezgif-2-c41d742895dc.jpg')

    button_style = st.markdown("""
    <style>
    div.stButton > button:first-child {
        text-size: 30px;
        height: 15m;
        width: 12em;
        font-size : 20px;
        font-family: Arial;
        font-weight: bold;
        text-align: center
    }
    </style>""", unsafe_allow_html=True)

if radio == "I'm a Recruiter":
    st.markdown(
    "<h1 style='text-align: center; color: black;'>I'm a recruiter</h1>",
    unsafe_allow_html=True)
    title = st.text_input('Job Position')
    entities = load_results_manual(title, streamlit=True)

elif radio == "I'm looking for a job":
    st.markdown(
    "<h1 style='text-align: center; color: black;'>I'm looking for a job</h1>",
    unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        raw_text = read_pdf(uploaded_file)
        raw_text
        entities = load_results_auto(raw_text)
        entities

    #col1, col2, col3 = st.columns(3)
    #with col1:
    #    category = col1.selectbox("Select a Job Category: ", categories)
    #    locations = list(data.loc[data.job == category]['location'].values)
    #
    #with col2:
    #    location = col2.selectbox("Location: ", locations)
    #
    #skill_box = st.multiselect("Skills: ", skills)
    #knowledge_box = st.multiselect('Experience', knowledges)
    #
    #col11, col22, col33 = st.columns(3)
    #with col11:
    #    years = ['0', '1', '2', '3', '4', '5+']
    #    experience = col11.selectbox("Years of experience: ", years)
