from typing import Optional, Literal
import itertools

class NerResult:
    '''
    CLass to keep NER result of text processing.
    '''
    PREPOSITIONS = ["in", "on", "at"]
    NER_KEYS = ["thing", "attribute", "location", "state", "action"]

    def __init__(self, text: str, ner_dict: Optional[dict[str, tuple[str, str]]], values_dict: Optional[list[tuple[float, Literal['C']] | float]]) -> None:
        """
        Initialize a NER_Request instance with attributes based on the NER_Dict.

        Args:
            text (str): The text input.
            NER_Dict (Dict[str, Any]): A dictionary containing keys and values for various NER categories.
            values_dict (Dict[str, Any]): A dictionary containing values.
        """
        # Set default attributes
        for key in self.NER_KEYS:
            setattr(self, key, ner_dict.get(key, [None])[0])
            
        # Handle value attributes
        self.value = values_dict.get(0, None) if values_dict else None
        self.value_type = values_dict.get(1, None) if values_dict else None

        # Generate description based on the input text and NER_Dict
        self.description = self._generate_description(text, ner_dict)

        # Store the original input
        self.input = text

    def _generate_description(self, text: str, ner_dict: Dict[str, Any]) -> str:
        """
        Generate a description from the input text by excluding recognized entities and prepositions.

        Args:
            text (str): The input text.
            ner_dict (Dict[str, Any]): The named entity recognition dictionary.

        Returns:
            str: A description extracted from the text.
        """
        tokens = text.split()
        recognized_literals = self._extract_recognized_literals(ner_dict)
        return " ".join(token for token in tokens if token not in recognized_literals and token not in self.PREPOSITIONS).strip()

    def _extract_recognized_literals(self, ner_dict: Dict[str, Any]) -> List[str]:
        """
        Extract recognized literals/entities from the NER dictionary.

        Args:
            ner_dict (Dict[str, Any]): The named entity recognition dictionary.

        Returns:
            List[str]: A list of recognized literals/entities.
        """
        literals = [literal.split() for _, literal in ner_dict.values()]
        return list(itertools.chain(*literals))

    def __str__(self) -> str:
        """
        Provide a string representation of the NER_result instance.

        Returns:
            str: A string representation of the instance.
        """
        values = [f"{key.capitalize()}: {getattr(self, key) or 'None'}" for key in self.NER_KEYS]
        values.append(f"Value: {self.value or 'None'}")
        return ", ".join(values)