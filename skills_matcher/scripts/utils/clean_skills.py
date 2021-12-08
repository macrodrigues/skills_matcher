import re
import pandas as pd

# Instructions:

# 1) import extract_skills_auto, extract_entities_2, extract_lables, get_dict
# 2) load data_final_raw.csv as data
# 2) data_cleaned = data.apply(get_dict, axis=1)

def extract_skills_auto(s):
    words_pattern = '[a-z]+'
    return re.findall(words_pattern, s, flags=re.IGNORECASE)

def extract_entities_2(s):
    pattern = re.compile("'entity': [a-zA-Z]+\W*([a-zA-Z]|\s)*")
    res = re.finditer(pattern, s)
    return [
        mo.group().split(",")[0].strip().lstrip("'entity': ") for mo in res
        if mo.group() != ','
    ]

def extract_lables(s):
    pattern = re.compile("'label':\s*'\w+'")
    res = re.finditer(pattern, s)
    return [mo.group().partition("': '")[2].strip("'") for mo in res]

def get_dict(x):

    dict_ = {}

    entities = extract_entities_2(x['entities_manual_label'])
    labels = extract_lables(x['entities_manual_label'])
    for index, key in enumerate(entities):
        if key not in dict_.keys():
            dict_[key] = labels[index]

    skills_auto = extract_skills_auto(x['entities_auto_label'])
    for index, value in enumerate(skills_auto):
        if value not in dict_.keys():
            dict_[value] = 'SKILL'

    skills_list = []
    knowledge_list = []
    min_exp_list = []
    level_list = []

    for entity, label in dict_.items():
        if label == 'SKILL':
            skills_list.append(entity)
        if label == 'KNOWLEDGE':
            knowledge_list.append(entity)
        if label == 'MIN_EXP':
            min_exp_list.append(entity)
        if label == 'LEVEL':
            level_list.append(entity)

    x["SKILL"] = skills_list
    x["KNOWLEDGE"] = knowledge_list
    x["MIN_EXP"] = min_exp_list
    x["LEVEL"] = level_list

    return x
