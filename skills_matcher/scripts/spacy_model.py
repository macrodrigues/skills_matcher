import json
import spacy
from spacy.tokens import DocBin
from tqdm import tqdm
import re
import numpy as np
import random

random.seed(42)

"""
Steps to implement the model:

1) convert jsonl to dictionary, cleans white spaces, and splits data:
    data = split_data(<jsonl_path>, val_split = 0.3)

2) create two spacy files, one for X_train, another for X_val:
    X_train_spacy = make_spacy_model(X_train)
    X_train_spacy.to_disk(<train.spacy>)
    X_val_spacy = make_spacy_model(X_val)
    X_val_spacy.to_disk(<val.spacy>)

3) Go to the link below, and copy the config file to your working directory:

    https://spacy.io/usage/training

    (you can find it below, "Quickstart")

4) In the base_config file of the train.spacy and val.spacy.

5) Create configuration file, by using the following command:
    ! python -m spacy init fill-config base_config.cfg config.cfg

6) Fine tune the model in the config.file and train the model:
    ! python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./train.spacy

7) See results and obtain highlited skills:
    entities = load_results(<model_path>, X_test)

"""

def split_data(jsonl_path, val_split = 0.3):
    """This function takes a JSON file and converts it
    to the format read by Spacy"""
    raw_data = []
    with open(jsonl_path) as f:
        for line in f:
            raw_data.append(json.loads(line))
    
    raw_data = random.sample(raw_data, len(raw_data))

    #convert json to dictionary format
    train_format = []
    for i in range(len(raw_data)):
        jd = raw_data[i]['data']
        label = raw_data[i]['label']
        label = [tuple(j) for j in label]
        label = {'entities': label}
        row = (jd, label)
        train_format.append(row)

    # removes leading and trailing white spaces from entity spans
    invalid_span_tokens = re.compile(r'\s')
    data = []
    for text, annotations in train_format:
        entities = annotations['entities']
        valid_entities = []
        for start, end, label in entities:
            valid_start = start
            valid_end = end
            while valid_start < len(text) and invalid_span_tokens.match(
                    text[valid_start]):
                valid_start += 1
            while valid_end > 1 and invalid_span_tokens.match(
                    text[valid_end - 1]):
                valid_end -= 1
            valid_entities.append([valid_start, valid_end, label])
        data.append([text, {'entities': valid_entities}])

    #split into validation and training data
    train_len = round(len(data)*(1-val_split))
    train_data =  data[:train_len]
    val_data = data[train_len:]
    return train_data, val_data

def make_spacy_model(data):
    """Create model spacy model"""
    nlp = spacy.blank("en") # load a new spacy model
    db = DocBin() # create a DocBin object
    for text, annot in tqdm(data): # data in previous format
        doc = nlp.make_doc(text) # create doc object from text
        ents = []
        for element in annot["entities"]:
            for start, end, label in [element]: # add character indexes
                span = doc.char_span(start,
                    end,
                    label=label,
                    alignment_mode="contract")
                if span is None:
                    print("Skipping entity")
                else:
                    ents.append(span)
        doc.ents = ents # label the text with the ents
        db.add(doc)
    return db

def load_results(model_path, X_text):
    nlp = spacy.load(model_path)
    doc = nlp(X_text)
    spacy.displacy.render(doc, style='ent', jupyter = True)
    ents = doc.ents
    output = []
    for entity in ents:
        row = {'entity': entity,
                'label': entity.label_,
                'mean_vector': entity.vector.mean()}
        output.append(row)
    return output
