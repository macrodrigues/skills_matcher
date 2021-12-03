from spacy import displacy
from spacy.training import Example
from spacy.training import biluo_tags_to_offsets
from pathlib import Path
from tqdm import tqdm
import numpy as np
import shutil
import spacy
import os

#set a random seed
#np.random.seed(42)

PATH = os.path.dirname(os.getcwd())

def get_train_data(data):
    """Convert the data into a training format for spacy"""
    l1 = []
    l2 = []
    for i in range(0, len(data['Skill'])):
        #print(biluo_tags_to_offsets(data['Skill'][i], data['Label'][i]))
        l1.append(data['Skill'][i])
        l2.append({'entities': [(np.random.randint(100), np.random.randint(100), data['Label'][i])]})

    train_data = list(zip(l1, l2))
    return train_data

def minibatch_model(train_data,
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
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for batch in tqdm(spacy.util.minibatch(train_data, size=batch_size)):
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
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to ", output_dir)

def niter_model(train_data,
                    model_name,
                    lang='en',
                    pipe='ner',
                    n_iter=30,
                    drop=0.81):

    # set blank 'en' model
    nlp = spacy.blank(lang)  #create a blank model in english

    # set pipeline
    nlp.add_pipe(pipe)  # ner is an entity recognizer, detects labels.

    # apply n_iter model
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            np.random.shuffle(train_data)
            losses = {}
            for text, annotations in tqdm(train_data):
                doc = nlp.make_doc(text)
                example = Example.from_dict(doc, annotations)
                # Update the model
                nlp.update([example], sgd=optimizer, losses=losses, drop=drop)

    # save model
    output_dir = Path(f"{PATH}/data/{model_name}")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    nlp.to_disk(output_dir)
    print("Saved model to ", output_dir)

def get_skills(model, text):
    """returns the list of skills detected, in the job position"""
    nlp = spacy.load(f"{PATH}/data/{model}")
    doc = nlp(text)
    ents = [(e.text, e.start, e.end, e.label_) for e in doc.ents]
    tags = offsets_to_biluo_tags(doc, ents)
    displacy.render(doc, style="ent")
    return ents
