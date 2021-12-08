from skills_matcher.app import SessionState
import pdfplumber
import os
import pandas as pd
import streamlit as st
import SessionState
from skills_matcher.scripts.spacy_model import load_results_manual, load_results_auto

PATH = os.path.dirname(os.path.dirname(__file__))
data = pd.read_csv(PATH + '/data/data_final_raw.csv')
categories = list(data.groupby('job').count().index)
locations = list(data.groupby('location').count().index)
locations.append('Europe')
skills = ['Python', 'JavaScript', 'AWS', 'R']
knowledges = ['Software Engineer', 'Finance', 'Economics']


def read_pdf(file):
    pdf = pdfplumber.open(file)
    page = pdf.pages[0]
    return page.extract_text()

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
        entities = load_results_manual(raw_text)
        entities_auto = load_results_auto(raw_text)
        entities = [dic['entity'] for dic in entities]
        entities.extend(entities_auto)
        entities = set(entities)
        entities
