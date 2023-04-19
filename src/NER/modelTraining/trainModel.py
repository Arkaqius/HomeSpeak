import spacy
import random
from spacy.util import minibatch, compounding
from spacy.training import Example
import typing as T
import json
import config as cfg

def load_spacy_json(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

def createModel(TRAIN_DATA) -> spacy.Language :
    nlp = spacy.blank("en")
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Add custom labels
    for _, annotations in TRAIN_DATA:
        for _, _, label in annotations["entities"]:
            ner.add_label(label)

    return nlp

def trainModel(nlp: spacy.Language,trainData : T.List[T.Tuple[str, T.Dict[str, T.List[T.Tuple[int, int, str]]]]]):

    # Shuffle the training data
    random.shuffle(trainData)

    # Convert the training data to the new Example format
    examples = []
    for text, annotations in trainData:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)

    # Split the data into training and validation sets
    train_examples = examples[:int(len(examples) * cfg.TRAIN_VAL_RATION)]
    val_examples = examples[int(len(examples) * cfg.TRAIN_VAL_RATION):]

    # Get the names of the model's other pipes (to disable during training)
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    # Train the model
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(cfg.NUMBER_OF_EPOCHS):  # Number of iterations (epochs)
            random.shuffle(train_examples)
            batches = minibatch(train_examples, size=compounding(4.0, 32.0, 1.001))
            losses = {}

            for batch in batches:
                nlp.update(batch, sgd=optimizer, drop=0.35, losses=losses)
            
            # Evaluate the model on the validation set
            val_metrics = nlp.evaluate(val_examples)
            print(f"Epoch: {itn + 1},\n Loss: {losses['ner']},\n Validation Metrics: {val_metrics}\n")

    nlp.to_disk(cfg.PATH_TRAINED_MODEL)

def main():
    train_data_path = cfg.PATH_TRAIN_DATA
    TRAIN_DATA = load_spacy_json(train_data_path)

    nlp = createModel(TRAIN_DATA)
    trainModel(nlp, TRAIN_DATA)

if __name__ == '__main__':
    main()
