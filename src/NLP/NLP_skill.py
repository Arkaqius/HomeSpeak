from abc import ABC, abstractmethod

class NLPSkill(ABC):
    
    @abstractmethod
    def request_handling_score(self,ner,utterance):
        pass