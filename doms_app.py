from numpy.core.fromnumeric import sometrue
import pdfplumber
import time
import os
import pandas as pd
import streamlit as st
from skills_matcher.scripts.spacy_model import load_results_manual, load_results_auto
from skills_matcher.scripts.utils.clean_skills import *
from skills_matcher.scripts.utils.matcher import extract_jd
from skills_matcher.scripts.utils.matcher import extract_resume_skills
from skills_matcher.scripts.utils.matcher import match_skills
from skills_matcher.scripts.utils.show_table import print_final_table
from skills_matcher.scripts.spacy_model import load_results_auto, load_results_manual
from skills_matcher.scripts.utils.clean_skills import extract_skills_auto, extract_entities_2, extract_lables, get_dict, get_dict_cv
from skills_matcher.scripts.utils.paths import load_paths
from skills_matcher.scripts.utils.matcher import get_JD, match_position_skills
import skills_matcher.scripts.utils.gauge_meter as gauge_meter
import plotly.graph_objects as go

PATH = os.path.dirname(os.path.dirname(__file__))
data = pd.read_csv(PATH + '/data/final_data.csv')
categories = list(data.groupby('job').count().index)


def read_pdf(file):
    pdf = pdfplumber.open(file)
    page = pdf.pages[0]
    return page.extract_text()


st.sidebar.title("Pages")

radio = st.sidebar.radio(
    label="",
    options=["Skills Matcher", "I'm a Recruiter", "I'm looking for a job"])

if radio == 'Skills Matcher':
    st.markdown("""
        <style>
        .reportview-container .main{
            background: url("https://drive.google.com/uc?id=1pyjYV_o4P_D1XJyhRDzQoCm9Cw1fm56d");
            background-size: cover;
        }
        """,
                unsafe_allow_html=True)

if radio == "I'm a Recruiter":
    st.markdown(
        "<h1 style='text-align: center; color: #325c7a;'>I'm a recruiter</h1>",
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox('Select a job category', categories)
        positions = list(data.loc[data.job == category]['position'].values)

    with col2:
        position = st.selectbox('Select an open position', positions)
        locations = list(
            data.loc[data.position == position]['location'].values)

    with col3:
        location = st.selectbox('Select a location', locations)

    description = [data.loc[(data.job == category) & \
            (data.position == position) & \
            (data.location == location)]\
            ['description'].values][0][0][2:-1]

    button_style = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #f3ffff;
        color:#325c7a;
        text-size: 30px;
        height: 10m;
        width: 5em;
        font-size : 20px;
        font-family: Arial;
        font-weight: bold;
        text-align: center
    }
    </style>""",
                               unsafe_allow_html=True)

    if st.button('Search'):
        latest_iteration = st.empty()
        bar = st.progress(0)
        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'Iteration {i+1}')
            bar.progress(i + 1)
            time.sleep(0.01)

        entities_manual = load_results_manual(description, streamlit=True)

        output = data.apply(get_dict, axis=1)
        res = print_final_table(position, output)
        hdf = res.assign(hack='').set_index('hack')
        st.table(hdf)

        #calling the matcher
        ###############################################################################

        pos_list = get_JD(position)
        res = match_position_skills(pos_list)

        best = res[2][0]
        nd = res[1][0]
        rd = res[0][0]

        best_score = res[2][1]
        nd_score = res[1][1]
        rd_score = res[0][1]

        col1, col2, col3 = st.columns(3)
        if nd_score + rd_score + best_score != 0:

            with col1:
                st.markdown(
                    f"<h1 style='text-align: left; white: red;'>ID : {best}</h1>",
                    unsafe_allow_html=True)
                if best % 2 == 0:
                    st.image("pics/ma.png")
                else:
                    st.image("pics/wo.png")

                CCC = gauge_meter(rd_score)
                CCC

            with col2:
                st.markdown(
                    f"<h1 style='text-align: middle; color: white;'>ID : {nd}</h1>",
                    unsafe_allow_html=True)
                if nd % 2 == 0:
                    st.image("pics/ma.png")
                else:
                    st.image("pics/wo.png")

                DDD = gauge_meter(nd_score)
                DDD

            with col3:
                st.markdown(
                    f"<h1 style='text-align: left; white: red;'>ID : {rd}</h1>",
                    unsafe_allow_html=True)

                if rd % 2 == 0:
                    st.image("pics/ma.png")
                else:
                    st.image("pics/wo.png")

                VVV = gauge_meter(best_score)
                VVV

        else:
            st.markdown(
                "<h1 style='text-align: center; color: cyan;'>Sorry, no candidates, go get some!</h1>",
                unsafe_allow_html=True)

elif radio == "I'm looking for a job":
    st.markdown(
        "<h1 style='text-align: center; color: #325c7a;'>I'm looking for a job</h1>",
        unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        category = st.selectbox('Select a job category', categories)
        positions = list(data.loc[data.job == category]['position'].values)

    with col2:
        position = st.selectbox('Select an open position', positions)
        locations = list(
            data.loc[data.position == position]['location'].values)

    with col3:
        location = st.selectbox('Select a location', locations)

    uploaded_file = st.file_uploader("Choose a file")

    if uploaded_file is not None:
        raw_text = read_pdf(uploaded_file)
        cv_entities = extract_resume_skills(
            raw_text)  #returns a DF with the cv_skills
        jd_df = extract_jd(inp=category)  #returns a DF with all the jd_skills
        fig = match_skills(cv_entities, jd_df)
        st.plotly_chart(fig)
