import spacy
import random
import config as cfg

class VH_NER:
    def __init__(self, model_path: str):
        self.nlp = spacy.load(model_path)
        self.pretrained_nlp = spacy.load("en_core_web_sm")

    def get_named_entities(self, text: str) -> dict:
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            entities[ent.text] = ent.label_
        return entities

    def extract_numerical_values(self, text: str):
        doc = self.pretrained_nlp(text)
        numerical_values = []
        fraction_mapping = {
            "half": 0.5,
            "third": 1/3,
            "fourth": 0.25,
            "fifth": 0.2,
            "quarter": 0.25,
        }

        for i, token in enumerate(doc):
            if token.is_digit or token.pos_ == "NUM":
                try:
                    if token.text[-1] == "%":
                        number = float(token.text[:-1].replace(',', '')) / 100
                    elif i + 1 < len(doc) and doc[i + 1].lower_ == "percent":
                        number = float(token.text.replace(',', '')) / 100
                    else:
                        number = float(token.text.replace(',', ''))
                    
                    if i + 1 < len(doc) and doc[i + 1].lower_ == "celsius":
                        number = (number, "C")
                    
                    numerical_values.append(number)
                except ValueError:
                    pass
            elif token.lower_ in fraction_mapping:
                numerical_values.append(fraction_mapping[token.lower_])

        return numerical_values

    def process_text(self, text: str):
        named_entities = self.get_named_entities(text)
        numerical_values = self.extract_numerical_values(text)
        return named_entities, numerical_values