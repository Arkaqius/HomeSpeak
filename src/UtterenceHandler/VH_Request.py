import VH_Enums
from typing import Any, Dict, Optional

class VH_request:
    def __init__(self, text: str, NER_Dict: Dict[str, Any], values_dict: Dict[str, Any]) -> None:
        """
        Initialize a VH_request instance with attributes based on the NER_Dict.

        Args:
            text (str): The text input (not used in the current implementation).
            NER_Dict (Dict[str, Any]): A dictionary containing keys and values for various NER categories.
            values_dict (Dict[str, Any]): A dictionary containing values (not used in the current implementation).
        """
        ner_keys = ['thing', 'attribute', 'location', 'state', 'value', 'action', 'value_type']
        for key in ner_keys:
            setattr(self, key, NER_Dict.get(key, [None])[0])

    def __str__(self) -> str:
        """
        Provide a string representation of the VH_request instance.

        Returns:
            str: A string representation of the instance.
        """
        return f"Thing: {self.thing}, Attribute: {self.attribute}, Location: {self.location}, Value: {self.value}, Action: {self.action}"
