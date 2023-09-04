# pylint: disable=C0114
from typing import Optional, Tuple, NamedTuple
import spacy
from spacy.language import Language
from spacy.tokens.doc import Doc  # pylint: disable=E0611


class VhNumericalValue(NamedTuple):
    """
    A NamedTuple for representing numerical values extracted from text.

    Attributes:
        value (float): The numerical value extracted from the text.
        unit (str): The unit associated with the numerical value.
    """
    value: float
    unit: str


class VhNamedEntity(NamedTuple):
    """
    A NamedTuple for representing named entities extracted from text.

    Attributes:
        entity_type (str): The type of the named entity (e.g., thing, location, atttribute, etc.).
        entity_default_name (str): The default name of the entity.
        entity_text (str): The actual text of the entity extracted from the text.
    """
    entity_type: str
    entity_default_name: str
    entity_text: str


class VhProcessedText(NamedTuple):
    """
    A NamedTuple for representing the results of processing text for named entities and numerical values.

    Attributes:
        named_entities (list[VhNamedEntity]): A list of named entities extracted from the text.
        numerical_values (list[VhNumericalValue]): A list of numerical values extracted from the text.
    """
    named_entities: list['VhNamedEntity']
    numerical_values: list['VhNumericalValue']


class VhNer:

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
        self.nlp: Language = spacy.load(name=model_path)
        self.pretrained_nlp: Language = spacy.load(name="en_core_web_sm")

    def _get_named_entities(self, text: str) -> dict[str, list[Tuple[str, str]]]:
        """
        Extracts named entities and their attributes from the given text using the Spacy
        NER model.

        Args:
            text (str): The text to process.

        Returns:
            dict: A dictionary containing the extracted named entities as keys and their
            attribute
            Example:
            {
                'action': ('on', 'on'),
                'thing': ('plug', 'socket'),
                'location': ('backyard', 'backyard')
            }
        """
        doc: Doc = self.nlp(text)
        entities: dict[str, list[Tuple[str, str]]] = {}
        for ent in doc.ents:
            split_label = ent.label_.split("_", maxsplit=1)
            if len(split_label) == 2:
                entity_type, attribute = split_label
                entity_type = entity_type.rstrip("s")
                
                # If entity type not in dictionary, add it with an empty list
                if entity_type not in entities:
                    entities[entity_type] = []

                # Append the tuple (attribute, ent.text) to the list
                entities[entity_type].append(
                    (attribute.replace("#", ""), ent.text)
                )
        return entities

    def _extract_numerical_values(self, text: str) -> list[tuple[float, str]]:  # pylint: disable=C0301
        """
        Extracts numerical values and fractions from the given text using a pretrained
        Spacy NLP pipeline.

        Args:
            text (str): The text to process.

        Returns:
            list: A list of tuples, each containing a numerical value and a unit (if any).
            Returns None if no numerical values are found.

        Example:
            If the input text is "50% of the room is at 20 celsius and the other half is dark",
            the method would return:
                [(0.5, ""), (20.0, "C"), (0.5, ""), (0.2, "")]
        """
        doc: Doc = self.pretrained_nlp(text)
        numerical_values: list[tuple[float, str]] = []

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
                        number = (number, "C")  # TODO Make it more general!
                    else:
                        number = (number, "")  # No unit

                    numerical_values.append(number)
                except ValueError:
                    pass  # TODO Add some logging
            elif token.lower_ in self.FRACTION_MAPPING:
                numerical_values.append(
                    (self.FRACTION_MAPPING[token.lower_], ""))
            elif token.lower_ in self.PRESET_MAPPING:
                numerical_values.append(
                    (self.PRESET_MAPPING[token.lower_], ""))

        return numerical_values

    def process_text(self, text: str) -> VhProcessedText:  # pylint: disable=C0301
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
        return VhProcessedText(
            named_entities=[
                VhNamedEntity(entity_type, entity_default_name, entity_text)
                for entity_type, entity_list in named_entities.items()
                for (entity_default_name, entity_text) in entity_list
            ],
            numerical_values=[
                VhNumericalValue(value, unit)
                for value, unit in numerical_values
            ],
        )
