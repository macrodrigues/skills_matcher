import streamlit as st
import spacy
from skills_matcher.scripts.spacy_model import load_results_manual
from skills_matcher.scripts.spacy_model import PATH_MANUAL_MODEL
import pandas as pd

import time
import streamlit as st
import pandas as pd

st.title('Position database')

#loads the data in csv
@st.cache
def get_data():
    path = r'data_final_raw_new.csv'
    return pd.read_csv(path)
df = get_data()

#selection box
choice = st.selectbox('Select jobtitle:', df['position'])
target = [df[df.position == choice]["description"].values][0][0][2:-1]

if st.button('Search'):

    # latest_iteration = st.empty()
    # bar = st.progress(0)

    # for i in range(100):
    #     # Update the progress bar with each iteration.
    #     latest_iteration.text(f'Iteration {i+1}')
    #     bar.progress(i + 1)
    #     time.sleep(0.05)

    entities = load_results_manual(str(target), streamlit=True)     #apply model
    nlp = spacy.load(PATH_MANUAL_MODEL)

"LOAD THE TABLE WITH SKILLS"

"SHOW THE CANDIDATES"


# def get_cvs():
#     path = r'/skills_matcher/data/Resume.csv'
#     return pd.read_csv(path)


# df = get_cvs()
