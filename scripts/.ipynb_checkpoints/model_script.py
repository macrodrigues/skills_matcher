from spacy import displacy
from spacy.training.example import Example
from pathlib import Path
import pandas as pd
import numpy as np
import spacy
import os

#set a random seed
np.random.seed(42)

PATH = os.path.dirname(os.path.dirname(os.getcwd()))

data = pd.read_csv(PATH + "/data/dictionaries/all_skills.csv")
data = data.drop_duplicates()

def get_train_data(data):
    """Convert the data into a training format for spacy"""
    l1 = []
    l2 = []
    for i in range(0, len(data['Skill'])):
        l1.append(data['Skill'][i])
        l2.append({'entities': [(0, len(data['Skill'][i]), data['Label'][i])]})

    train_data = list(zip(l1, l2))
    return train_data

def generate_model(train_data,
                    model_name,
                    lang='en',
                    pipe='ner',
                    batch_size=1,
                    drop=0.81):

    """This model takes a training train_data (dictionary of labels)
    and feeds it to a minibatch model."""

    # set blank 'en' model
    nlp = spacy.blank(lang) #create a blank model in english

    # set pipeline
    nlp.add_pipe(pipe) # ner is an entity recognizer, detects labels.

    # apply mini batch model
    optimizer = nlp.begin_training()
    for batch in spacy.util.minibatch(train_data, size=batch_size):
        np.random.shuffle(train_data)
        losses = {}
        for text, annotations in batch:
            doc = nlp.make_doc(text)
            example = Example.from_dict(doc, annotations)
            # Update the model
            nlp.update([example],
                        sgd = optimizer,
                        losses=losses,
                        drop=drop)

    # save model
    output_dir = Path(f"{PATH}/data/{model_name}")
    output_dir.mkdir()
    nlp.to_disk(output_dir)
    return nlp

def get_skills(model, text):
    """returns the list of skills detected, in the job position"""
    nlp = spacy.load(f"{PATH}/data/{model}")
    doc = nlp(text)
    ents = [(e.text, e.start, e.end, e.label_) for e in doc.ents]
    displacy.render(doc, style="ent")
    return ents
