import spacy
import typing as T


class VH_NER:

    """
    A class for performing named entity recognition (NER) and numerical value extraction
    on text using Spacy.

    Attributes:
        nlp (spacy.language.Language): A Spacy NLP pipeline for performing NER.
        pretrained_nlp (spacy.language.Language): A Spacy NLP pipeline for extracting
            numerical values and fractions from text.

    Methods:
        get_named_entities(text: str) -> dict:
            Extracts named entities and their attributes from the given text using the
            Spacy NER model.

        extract_numerical_values(text: str) -> list:
            Extracts numerical values and fractions from the given text using a pretrained
            Spacy NLP pipeline.

        process_text(text: str) -> tuple:
            Processes the given text and returns a tuple containing the extracted named
            entities and numerical values as dictionaries. Returns (None, None) if no
            named entities or numerical values are found.
    """
    FRACTION_MAPPING = {
    "half": 0.5,
    "third": 1 / 3,
    "fourth": 0.25,
    "fifth": 0.2,
    "quarter": 0.25,
    }

    PRESET_MAPPING = {
        "eco": 0.3,
        "comfort": 0.7,
        "warm": 0.9,
        "bright": 0.8,
        "dark": 0.2,
    }

    def __init__(self, model_path: str) -> None:
        """
        Initializes a new instance of the VH_NER class.

        Args:
            model_path (str): The path to the Spacy NER model to use for entity extraction.
        """
        self.nlp = spacy.load(model_path)
        self.pretrained_nlp = spacy.load("en_core_web_sm")

    def _get_named_entities(self, text: str) -> dict:
        """
        Extracts named entities and their attributes from the given text using the Spacy
        NER model.

        Args:
            text (str): The text to process.

        Returns:
            dict: A dictionary containing the extracted named entities as keys and their
            attribute
        """
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            split_label = ent.label_.split("_", maxsplit=1)
            if len(split_label) == 2:
                entity_type, attribute = split_label
                entities[entity_type.rstrip("s")] = (attribute.replace("#", ""), ent.text)
        return entities if entities else None

    def _extract_numerical_values(self, text: str):
        """
        Extracts numerical values and fractions from the given text using a pretrained
        Spacy NLP pipeline.

        Args:
            text (str): The text to process.

        Returns:
            list: A list of extracted numerical values and fractions. Returns None if no
            numerical values are found.
        """
        doc = self.pretrained_nlp(text)
        numerical_values = []
        fraction_mapping = {
            "half": 0.5,
            "third": 1 / 3,
            "fourth": 0.25,
            "fifth": 0.2,
            "quarter": 0.25,
        }
        preset_mapping = {
            "eco": 0.3,
            "comfort": 0.7,
            "warm": 0.9,
            "bright": 0.8,
            "dark": 0.2,
        }

        for i, token in enumerate(doc):
            if token.is_digit or token.pos_ == "NUM":
                try:
                    if token.text[-1] == "%":
                        number = float(token.text[:-1].replace(",", "")) / 100
                    elif i + 1 < len(doc) and doc[i + 1].lower_ == "percent":
                        number = float(token.text.replace(",", "")) / 100
                    else:
                        number = float(token.text.replace(",", ""))

                    if i + 1 < len(doc) and doc[i + 1].lower_ == "celsius":
                        number = (number, "C") # TODO Make it more general

                    numerical_values.append(number)
                except ValueError:
                    pass
            elif token.lower_ in self.FRACTION_MAPPING:
                numerical_values.append(self.FRACTION_MAPPING[token.lower_])
            elif token.lower_ in self.PRESET_MAPPING:
                numerical_values.append(self.PRESET_MAPPING[token.lower_])

        return numerical_values if numerical_values else None

    def process_text(self, text: str) -> T.Tuple[dict, list]:
        """
        Processes the given text and returns a tuple containing the extracted named
        entities and numerical values as dictionaries. Returns (None, None) if no named
        entities or numerical values are found.

        Args:
            text (str): The text to process.

        Returns:
            tuple: A tuple containing two dictionaries. The first dictionary contains
            the extracted named entities as keys and their attributes and text as values.
            The second dictionary contains the extracted numerical values as keys and
            their units (if any) as values.
        """
        named_entities = self._get_named_entities(text)
        numerical_values = self._extract_numerical_values(text)
        return named_entities, numerical_values
