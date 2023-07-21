from typing import Any, Dict
import itertools

class VH_Request:

    PREPOSITIONS = ['in','on','at']

    def __init__(self, text: str, NER_Dict: Dict[str, Any], values_dict: Dict[str, Any]) -> None:
        """
        Initialize a VH_request instance with attributes based on the NER_Dict.

        Args:
            text (str): The text input (not used in the current implementation).
            NER_Dict (Dict[str, Any]): A dictionary containing keys and values for various NER categories.
            values_dict (Dict[str, Any]): A dictionary containing values.
        """
        self.thing = ''
        self.attribute = ''
        self.location = ''
        self.state = ''
        self.action = ''
        ner_keys = ['thing', 'attribute', 'location', 'state', 'action']

        for key in ner_keys:
            setattr(self, key, NER_Dict.get(key, [None])[0])

        if(values_dict):
            self.value = values_dict.get(0,None) #TODO
            self.value_type  = values_dict.get(1,None)
        
        # Initialize an empty description
        self.description : str = ""

        # Tokenize the input text using split
        tokens = text.split(' ')

        # self.text is not yet initialized, otherwise whole utterances will be ommited
        fields = list(self.__dict__.values())
        found_literals = [t[1] for t in NER_Dict.values() if t[0] in fields]
        found_literals = list(itertools.chain(*[a.split(' ') for a in found_literals]))
        # Check if each token is not in the NER entities, value, or value type
        for token in tokens:
            if (token not in found_literals and token not in self.PREPOSITIONS):
                self.description += token + " "

        # Remove the trailing whitespace
        self.description = self.description.strip()

        # Add whole utterance at end
        self.input = text

    def __str__(self) -> str:
        """
        Provide a string representation of the VH_request instance.

        Returns:
            str: A string representation of the instance.
        """
        return f"Thing: {self.thing}, Attribute: {self.attribute}, Location: {self.location}, Value: {self.value}, Action: {self.action}"
