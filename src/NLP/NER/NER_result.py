# pylint: disable=C0114
import itertools
from ner.vh_ner import VhProcessedText, VhNamedEntity, VhNumericalValue


class NerResult:
    '''
    Class to keep NER result of text processing.

    Attributes:
        text (str): The text input.
        ner_raw (VhProcessedText): A VhProcessedText object containing the named entities 
                                   and numerical values extracted from the text.

    Methods:
        _generate_description(text: str, ner_dict: Dict[str, Any]) -> str:
            Generate a description from the input text by excluding recognized entities 
            and prepositions.

        _extract_recognized_literals(ner_dict: Dict[str, Any]) -> List[str]:
            Extract recognized literals/entities from the NER dictionary.

        __str__() -> str:
            Provide a string representation of the NER_result instance.
    '''

    PREPOSITIONS = ["in", "on", "at"]
    NER_KEYS = ["thing", "attribute", "location", "state", "action"]

    def __init__(self, text: str, ner_raw: VhProcessedText) -> None:
        """
        Initialize a NER_Request instance with attributes based on the ner_raw.

        Args:
            text (str): The text input.
            ner_raw (VhProcessedText): A VhProcessedText object containing the named entities 
                                       and numerical values extracted from the text.

        """
        # Set default attributes
        for key in self.NER_KEYS:
            setattr(self, key, getattr(ner_raw.named_entities, key, None))

        # Handle value attributes
        self.values: list[VhNumericalValue] = ner_raw.numerical_values

        # Generate description based on the input text and NER_Dict
        self.description: str = self._generate_description(
            text, ner_raw.named_entities)

        # Store the original input
        self.input: str = text

    def _generate_description(self, text: str, ner_entities: list[VhNamedEntity]) -> str:
        """
        Generate a description from the input text by excluding recognized entities and prepositions.

        Args:
            text (str): The input text.
            ner_entities (List[VhNamedEntity]): A list of named entities extracted from the text.

        Returns:
            str: A description extracted from the text.
        """
        tokens = text.split()
        recognized_literals = self._extract_recognized_literals(ner_entities)
        return " ".join(token for token in tokens if token not in recognized_literals and token not in self.PREPOSITIONS).strip()

    def _extract_recognized_literals(self, ner_entities: list[VhNamedEntity]) -> list[str]:
        """
        Extract recognized literals/entities from the list of named entities.

        Args:
            ner_entities (List[VhNamedEntity]): A list of named entities extracted from the text.

        Returns:
            List[str]: A list of recognized literals/entities.
        """
        literals = [entity.entity_text.split() for entity in ner_entities]
        return list(itertools.chain(*literals))