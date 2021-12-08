import pandas as pd
import numpy as np
import re

#spacy nlp 
import spacy
from spacy.pipeline import EntityRuler
from spacy.lang.en import English
from spacy.tokens import Doc, Span

from spacy import displacy

#word 
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

from skills_matcher.scripts.spacy_model import load_results_auto, load_results_manual
from skills_matcher.scripts.utils.clean_skills import extract_skills_auto, extract_entities_2, extract_lables, get_dict, get_dict_cv
from skills_matcher.scripts.utils.paths import load_paths


PATH_DATA, PATH_DICT, PATH_TRAIN_DATA, PATH_VAL_DATA, PATH_COMPLETE_DICT, PATH_COMPLETE_CV = load_paths('final_data', 'doccano_dictionary', 'train', 'val', 'complete_dict', 'cleaned_Resume_final')

"""Workflow of functions for comparing CV to JD
- load CV text
- call extract_resume_skills(text) and save as cv_skill_set
- call extract_jd with/or without input from frontend and save as data
- call match_skills(cv_skill_list, data)
"""

def extract_CV(inp = None):
    df_CV = pd.read_csv(PATH_COMPLETE_CV, index_col=[0])
    data = df_CV.apply(get_dict_cv, axis=1)
    data.drop(columns = ["Resume_html", "entities_auto_label", 'entities_manual_label'], inplace = True)
    return data

def extract_resume_skills(text):
    #extracting skills from resume string
    
    set_list_2 = []
    ext = []
    
    list_1 = create_skill_list(text, model = True)  #get extracted skills with base_model
    list_2 = load_results_manual(text)     #get extracted skills with trained_model  
        
    for i in range(0, len(list_2)):
        set_list_2.append(str(list_2[i]["entity"]).lower().strip())
    set_list_2 = set(set_list_2)
    ext.append(set.union(list_1, set_list_2))
    
    flat_list = [item for sublist in ext for item in sublist]
    set(flat_list)
        
    return flat_list

def extract_jd(inp = None):
    df_JD = pd.read_csv(PATH_DATA, index_col=[0])
    
    #else branch with input seems like its not working properly with match_skills function (yet)
    if inp == None:
        data = df_JD.apply(get_dict, axis=1)
        data.drop(columns = ["ISCO", "major_job"], inplace = True)
    else:    
        df_JD = df_JD.loc[df_JD['job'] == inp, ['job', 'position', 'location', 'description',	
                              'entities_auto_label', 'entities_manual_label']]
        data = df_JD.apply(get_dict, axis=1)
        data.reset_index(inplace = True)
        
    data.drop(columns = ['entities_auto_label', 'entities_manual_label'], inplace = True)
    
    return data

def extract_jd_position(inp = None):
    df_JD = pd.read_csv(PATH_DATA, index_col=[0])
    
    if inp == None:
        data = df_JD.apply(get_dict, axis=1)
        data.drop(columns = ["ISCO", "major_job"], inplace = True)
    else:    
        df_JD = df_JD.loc[df_JD['position'] == inp, ['job', 'position', 'location', 'description',	
                              'entities_auto_label', 'entities_manual_label']]
        data = df_JD.apply(get_dict, axis=1)
        data.reset_index(inplace = True)
    
    return data

def match_skills(cv_set, data):
    '''Get intersection of resume skills and job offer skills and return match percentage'''
    percent_list = []
    
    JD_set = data["SKILL"].apply(set)
    
    #JD_set = list(filter(None, JD_set))
    if len(cv_set) < 1:
        print('could not extract skills from resume text')   
    else:
        #implement function comparing with a list of job_descriptions
        for i in range(0, len(JD_set)):
            if len(JD_set[i]) < 2:
                continue
            else:
                quotient = len(set(cv_set) & JD_set[i])
                divisor = len(JD_set[i])
                percent_match = round((quotient/divisor) * 100, 2)
                percent_list.append([i, percent_match])
            
        percent_list.sort(key=lambda x: x[1], reverse = True)
        percent_list = percent_list[0:9]
    return percent_list

def visualizer(list, data):   
    '''Counting matching score'''
    job_number, matching_score, job_cat = [], [], []
    pct_list = list
    frame = pd.DataFrame

    for i in pct_list:
        cat = data["position"][i[0]]
        print('Job #{} in Sector {} has a {}% match'.format(i[0], cat, i[1]))
        job_number.append(i[0])
        matching_score.append(i[1])

        if cat in job_cat:
            job_cat.append(str(cat) + str(i[0]))
        else:
            job_cat.append(cat)

    frame = pd.DataFrame(job_number, columns=['job_number'])
    frame["matching_score"] = matching_score
    frame["Category"] = job_cat
    #could implement frame["color"] with different color for each job

    
    #Visualizing with plotly
    #templates: ['ggplot2', 'seaborn', 'simple_white', 'plotly',
         #'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         #'ygridoff', 'gridon', 'none']

    fig = px.bar(
        x=frame['Category'], 
        y=frame["matching_score"],
        labels={"x": "job position", "y": "Matching %"},
        title=f"Job offers matching with resume",
        width=1200, height=800,
        template="seaborn",
        color = frame["matching_score"])
    fig.update_layout(
        paper_bgcolor="lightblue",
    )
    
    return fig.show()

def clean_resume(df):
    clean = []
    for i in range(df.shape[0]):
        review = re.sub(
            '(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?"',
            " ",
            df["Resume_str"].iloc[i],
        )
        review = review.lower()
        review = review.split()
        lm = WordNetLemmatizer()
        review = [
            lm.lemmatize(word)
            for word in review
            if not word in set(stopwords.words("english"))
        ]
        review = " ".join(review)
        clean.append(review)
    return clean

def create_skill_list(text, model = False):
    
    if model == True:
        
        skill_pattern_path = PATH_COMPLETE_DICT
        nlp_ms = spacy.blank("en") 
        
        ruler = nlp_ms.add_pipe("entity_ruler")
        ruler.from_disk(skill_pattern_path)
        doc = nlp_ms(text)
    else:
        doc = text
    
    t = list([ent.text.lower()] for ent in doc.ents )
    flat_list = [item for sublist in t for item in sublist]
    return set(flat_list)