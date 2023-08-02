from spacy.util import minibatch, compounding
from spacy.training import Example
import NLP.NER.config as cfg
import spacy
import random
import typing as T
import json


def load_spacy_json(file_path: str) -> list:
    """
    Load a JSON file containing spaCy training data.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        list: A list containing the training data loaded from the JSON file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def create_model(
    train_data: T.List[T.Tuple[str, T.Dict[str, T.List[T.Tuple[int, int, str]]]]]
) -> spacy.Language:
    """
    Create a spaCy NER model with custom labels from the training data.

    Args:
        train_data (List[Tuple[str, Dict[str, List[Tuple[int, int, str]]]]]): A list of training data.

    Returns:
        spacy.Language: A spaCy language model with a custom NER pipe.
    """
    nlp = spacy.blank("en")

    if "ner" not in nlp.pipe_names:
        ner = nlp.add_pipe("ner", last=True)
    else:
        ner = nlp.get_pipe("ner")

    # Add custom labels
    for _, annotations in train_data:
        for _, _, label in annotations["entities"]:
            ner.add_label(label)

    return nlp


def train_model(
    nlp: spacy.Language,
    train_data: T.List[T.Tuple[str, T.Dict[str, T.List[T.Tuple[int, int, str]]]]],
):
    """
    Train the NER model using the provided training data.

    Args:
        nlp (spacy.Language): The spaCy language model with a custom NER pipe.
        train_data (List[Tuple[str, Dict[str, List[Tuple[int, int, str]]]]]): A list of training data.
    """

    # Shuffle the training data
    random.shuffle(train_data)

    # Convert the training data to the new Example format
    examples = []
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        examples.append(example)

    # Split the data into training and validation sets
    train_examples = examples[: int(len(examples) * cfg.TRAIN_VAL_RATION)]
    val_examples = examples[int(len(examples) * cfg.TRAIN_VAL_RATION) :]

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
            print(
                f"Epoch: {itn + 1},\n Loss: {losses['ner']},\n Validation Metrics: {val_metrics}\n"
            )

    nlp.to_disk(cfg.PATH_TRAINED_MODEL)


def main():
    """
    The main function to train a Named Entity Recognition (NER) model using spaCy.
    """
    train_data_path = cfg.PATH_TRAIN_DATA
    train_data = load_spacy_json(train_data_path)

    nlp = create_model(train_data)
    train_model(nlp, train_data)


if __name__ == "__main__":
    main()
