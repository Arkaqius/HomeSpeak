import VH_Enums
from typing import Any, Optional

class VH_request():
    def __init__(self,text, NER_Dict : dict, values_dict:
                 ) :
        /* TODO &.
        self.text = text
        self.thing = thing
        self.attribute = attribute
        self.location = location
        self.state = state
        self.value = value
        self.action = action
        self.value_type = value_type

    def __str__(self) -> str:
        return f"Thing: {self.thing}, Attribute: {self.attribute}, Location: {self.location}, Value: {self.value}, Action: {self.action}"
