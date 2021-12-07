import sys
import os
PATH = os.path.dirname(os.getcwd())
sys.path.append(PATH)

def load_paths(data_name, dictionary_name, train_spacy_name, val_spacy_name):
    PATH_TRAIN_DATA = f"{PATH}/skills_matcher/models/{train_spacy_name}.spacy"
    PATH_VAL_DATA = f"{PATH}/skills_matcher/models/{val_spacy_name}.spacy"
    PATH_DICT = f"{PATH}/skills_matcher/data/dictionaries/{dictionary_name}.jsonl"
    PATH_DATA = f"{PATH}/skills_matcher/data/{data_name}.csv"
    return PATH_DATA, PATH_DICT, PATH_TRAIN_DATA, PATH_VAL_DATA
