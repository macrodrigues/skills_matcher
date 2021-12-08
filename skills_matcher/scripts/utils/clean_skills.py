import re
import pandas as pd

# Instructions:

### clean job descriptions
# 1) import extract_skills_auto, extract_entities_2, extract_lables, get_dict, lowercase, remove_punktuation
# 2) load data_final_raw.csv as data
# 2) data_cleaned = data.apply(get_dict, axis=1)
# 3) data_cleaned[<column>].apply(lowercase).apply(remove_punktuation)

### clean CV
# 1) import extract_skills_auto, extract_entities_2, extract_lables, get_dict, lowercase, remove_punktuation, get_dict_cv
# 2) load CV data
# 2) data_cleaned = data_cv.apply(get_dict_cv, axis=1)
# 3) data_cleaned[<column>].apply(lowercase).apply(remove_punktuation)


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


def lowercase(s):
    new_list = [skill.lower() for skill in s]
    return new_list


def remove_punktuation(s):
    new_list = [
        re.sub(r'[^\w\s+]', '', skill).replace('\xa0', '') for skill in s
    ]
    return new_list


def get_dict_cv(x):
    dict_ = {}
    entities = extract_entities_2(x['entities_manual_label'])
    labels = extract_lables(x['entities_manual_label'])
    for index, key in enumerate(entities):
        if key not in dict_.keys():
            dict_[key] = labels[index]
    entities_manual_label = extract_skills_auto(x['entity_ruler'])
    for index, value in enumerate(entities_manual_label):
        if value not in dict_.keys():
            dict_[value] = 'SKILL'
    skills_list = []
    for entity, label in dict_.items():
        if label == 'SKILL':
            skills_list.append(entity)
    x["SKILL"] = skills_list
    return x
