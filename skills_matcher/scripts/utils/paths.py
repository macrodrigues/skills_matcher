import os
PATH = os.path.dirname(os.path.dirname(os.path.dirname((__file__))))

def load_paths(data_name,
                dictionary_name,
                train_spacy_name,
                val_spacy_name,
                dictionary_2_name,
                cv_file):

    PATH_TRAIN_DATA = f"{PATH}/scripts/models/{train_spacy_name}.spacy"
    PATH_VAL_DATA = f"{PATH}/scripts/models/{val_spacy_name}.spacy"
    PATH_DICT = f"{PATH}/data/dictionaries/{dictionary_name}.jsonl"
    PATH_DATA = f"{PATH}/data/{data_name}.csv"
    PATH_COMPLETE_DICT = f"{PATH}/data/dictionaries/{dictionary_2_name}.jsonl"
    PATH_COMPLETE_CV = f"{PATH}/data/{cv_file}.csv"
    return PATH_DATA, \
        PATH_DICT, \
        PATH_TRAIN_DATA, \
        PATH_VAL_DATA, \
        PATH_COMPLETE_DICT, \
        PATH_COMPLETE_CV

print(PATH)
