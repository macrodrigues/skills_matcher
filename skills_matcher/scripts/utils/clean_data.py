import pandas as pd
import numpy as np
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

def clean_dictionary(data, sample = 2000):
    data = data.drop_duplicates()
    data = data.dropna()
    if sample != None:
        data = data.sample(sample, random_state=42)
    data = data.reset_index().drop(['index'], axis = 1)
    ## Lower case
    #data['Skill'] = data['Skill'].apply(lambda x: x.lower())
    ## remove tabulation and punctuation
    #data['Skill'] = data['Skill'].str.replace('[^\w\s]',' ')
    # remove stop words
    #stop = stopwords.words('english')
    #data['Skill'] = data['Skill'].apply(lambda x: " ".join(x for x in x.split() if x not in stop))
    # nltk lemmatizer
    #lemmatizer = WordNetLemmatizer()
    #data['Skill'] = data['Skill'].apply(lambda x: " ".join([lemmatizer.lemmatize(word) for word in x.split()]))
    return data


def clean_skills():
    pass
