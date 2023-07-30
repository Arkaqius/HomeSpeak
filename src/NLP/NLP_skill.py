from abc import ABC, abstractmethod
from typing import Tuple

class NLPSkill(ABC):
    
    @abstractmethod
    def request_handling_score(self,ner,utterance) -> Tuple:
        pass

    @abstractmethod
    def handle_utterence(self,utterance,ner = None, ner_data = None):
        pass