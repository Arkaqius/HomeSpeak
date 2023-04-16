
import spacy

class VH_Ner:

    # constructor
    def __init__(self):
        pass



def load_trained_model(model_path: str) -> spacy.Language:
    nlp = spacy.load(model_path)
    return nlp

def process_text(nlp: spacy.Language, text: str):
    doc = nlp(text)
    for ent in doc.ents:
        print(f"{ent.text}: {ent.label_}")

def get_named_entities(nlp: spacy.Language, text: str) -> dict:
    doc = nlp(text)
    entities = {}
    for ent in doc.ents:
        entities[ent.text] = ent.label_
    return entities

def main():
    model_path = "./src/NER/modelTraining/trainedModel"
    nlp = load_trained_model(model_path)

    text = "Turn on the light in the living room"
    named_entities = get_named_entities(nlp, text)
    
    print("Named entities:")
    for entity, label in named_entities.items():
        print(f"{entity}: {label}")

if __name__ == '__main__':
    main()