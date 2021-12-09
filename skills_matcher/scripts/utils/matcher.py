import pandas as pd
import re

#spacy nlp
import spacy

#word
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

import plotly.express as px
from skills_matcher.scripts.spacy_model import load_results_manual
from skills_matcher.scripts.utils.clean_skills import get_dict, get_dict_cv
from skills_matcher.scripts.utils.paths import load_paths


PATH_DATA, \
PATH_DICT, \
PATH_TRAIN_DATA, \
PATH_VAL_DATA, \
PATH_COMPLETE_DICT, \
PATH_COMPLETE_CV = \
load_paths('final_data',
            'doccano_dictionary',
            'train',
            'val',
            'complete_dict',
            'cleaned_Resume_final')

"""Workflow for comparing CV to JD
- load CV text
- call extract_resume_skills(text) and save as cv_skill_set
- call extract_jd with/or without input from frontend and save as data
- call match_skills(cv_skill_list, data)
"""

"""Workflow for comparing chosen Job Position to CV dataset
- call get_JD with string of chosen Job Position and save as list - pos_list = get_JD('position') 
- call match_position_skills with saved pos_list - match_position_skills(pos_list)"""


#getting cleaned/skill extracted CV dataset
def extract_CV(inp = None):
    df_CV = pd.read_csv(PATH_COMPLETE_CV, index_col=[0])
    data = df_CV.apply(get_dict_cv, axis=1)
    data.drop(columns = ["Resume_html",
                        "entities_auto_label",
                        'entities_manual_label'], inplace = True)
    return data

#getting list of extracted skills from ONE CV text input
def extract_resume_skills(text):
    #extracting skills from resume string
    set_list_2 = []
    ext = []

    list_1 = create_skill_list(text, model = True)  #get extracted skills with base_model
    list_2 = load_results_manual(text) #get extracted skills with trained_model

    for i in range(0, len(list_2)):
        set_list_2.append(str(list_2[i]["entity"]).lower().strip())
    set_list_2 = set(set_list_2)
    ext.append(set.union(list_1, set_list_2))

    flat_list = [item for sublist in ext for item in sublist]
    set(flat_list)
    return flat_list

#getting cleaned/skill extracted JD dataset by Job Category
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

#getting cleaned/skill extracted JD dataset by Job Position
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

#getting skill_list of chosen job description
def get_JD(inp):
    data = extract_jd_position(inp)
    
    lengths = data["SKILL"].map(lambda x: len(x))
    position = data[lengths == lengths.max()].reset_index().drop(columns = "index")
    position_skills = position.loc[0][["SKILL", "KNOWLEDGE", "MIN_EXP", "LEVEL"]]

    position_list = []
    for column in position_skills:
        position_list.append(column)
    
    position_list = [item.lower() for sublist in position_list for item in sublist]
    
    return(set(position_list))

#matching skills of one CV to JD dataset
def match_skills(cv_set, data):
    '''Get intersection of resume skills and job offer skills and return match percentage'''

    all_skills = []
    for i, row in data.iterrows():
        skills = list(data['SKILL'][i])
        knows = list(data['KNOWLEDGE'][i])
        mins = list(data['MIN_EXP'][i])
        merged_labels = set(skills + knows + mins)
        all_skills.append(merged_labels)

    data['MERGE'] = all_skills
    percent_list = []
    if len(cv_set) < 1:
        print('could not extract skills from resume text')
    else:
        #implement function comparing with a list of job_descriptions
        for i in range(0, len(data['MERGE'])):
            if len(data['MERGE'][i]) < 2:
                continue
            else:
                quotient = len(set(cv_set) & data['MERGE'][i])
                divisor = len(data['MERGE'][i])
                percent_match = round((quotient/divisor) * 100, 2)
                percent_list.append([i, percent_match])

        percent_list.sort(key=lambda x: x[1], reverse = True)
        percent_list = percent_list[0:4]


    '''Counting matching score'''
    job_number, matching_score, job_cat, job_sec = [], [], [], []
    pct_list = list
    frame = pd.DataFrame
    for i in pct_list:
        sec = data["job"][i]
        cat = data["position"][i[0]]
        print('Job #{} in Sector {} has a {}% match'.format(i[0], cat, i[1]))
        job_number.append(i[0])
        matching_score.append(i[1])
        job_sec.append(sec)
        
        #in case job position already exists
        if cat in job_cat:
            job_cat.append(str(cat) + ' ' + str(i[0]))
        else:
            job_cat.append(cat)

    frame = pd.DataFrame(job_number, columns=['job_number'])
    frame["matching_score"] = matching_score
    frame["Category"] = job_cat
    frame["Sector"] = job_sec
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
        width=800, height=800,
        template="seaborn",
        color = frame["matching_score"])
    fig.update_layout(
        paper_bgcolor="lightblue",
    )

    return fig

#Matching JD skill list with CV dataset
def match_position_skills(JD_set):
    '''Get intersection of resume skills and job offer skills and return match percentage'''
    cv_data = extract_CV()
    CV_list = cv_data["SKILL"].apply(set)

    percent_list = []
    if len(JD_set) < 1:
        print('could not extract skills from job description')
    else:
        #implement function comparing with a list of job_descriptions
        for i in range(0, len(CV_list)):
            if len(CV_list[i]) < 1:
                continue
            else:
                quotient = len(set(JD_set) & CV_list[i])
                divisor = len(CV_list[i])
                percent_match = round((quotient/divisor) * 100, 2)
                percent_list.append([i, percent_match])

        percent_list.sort(key=lambda x: x[1], reverse = True)
        percent_list = percent_list[0:4]
        
        for person in percent_list:
            print("Candidate # {} has a {} % skill match with your job description".format(person[0], person[1]))
    return None

#cleaning Resume dataset
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

#applying base model on one text and return list of extracted skills
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
