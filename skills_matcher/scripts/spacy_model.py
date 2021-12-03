import json
import spacy
from spacy import displacy
from spacy.tokens import DocBin
from tqdm import tqdm
import os
import re

"""
Steps to implement the model:

1) convert json to dictionary, and clean white spaces:
    training_data = json_to_train_data(<json_path>)

2) split into X_train and X_val:
    X_train, X_val = split_data(training_data, val_split = 0.2)

3) create two spacy files, one for X_train, another for X_val:
    X_train_spacy = make_spacy_model(X_train)
    X_train_spacy.to_disk(<train.spacy>)
    X_val_spacy = make_spacy_model(X_val)
    X_val_spacy.to_disk(<val.spacy>)

4) Create configuration file, by using the following command:
    python -m spacy init fill-config base_config.cfg config.cfg

5) Fine tune the model in the config.file and train the model:
    python -m spacy train config.cfg --output ./output --paths.train ./train.spacy --paths.dev ./train.spacy

6) See results and obtain highlited skills:
    entities = load_results(<model_path>, text)

"""

def json_to_train_data(json_path):
    """This function takes a JSON file and converts it
    to the format read by Spacy"""

    #open json file
    with open(json_path) as json_file:
        data = json.load(json_file)

    #convert json to dictionary format
    train_format = []
    for i in range(len(data)):
        jd = data[i]['data']
        label = data[i]['label']
        label = [tuple(j) for j in label]
        label = {'entities': label}
        row = (jd, label)
        train_format.append(row)

    # removes leading and trailing white spaces from entity spans
    invalid_span_tokens = re.compile(r'\s')
    training_data = []
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
        training_data.append([text, {'entities': valid_entities}])

    return training_data

def split_data(data, val_split = 0.2):
    """ Takes the the training data from "json_to_train_data" function,
    and splits it, into validation and training data"""
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

def load_results(model_path, text):
    nlp = spacy.load(model_path)
    doc = nlp(text)
    spacy.displacy.render(doc, style='ent', jupyter = True)
    return doc.ents
