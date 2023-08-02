from abc import ABC, abstractmethod
from typing import Tuple,TYPE_CHECKING
from .HASkills.common.HAS_common import HAS_result # TODO Move HAS_result to NLP as NLP_result

if TYPE_CHECKING:
    from VHOrchestator import VHOrchestator

class NLPSkill(ABC):
    
    @abstractmethod
    def request_handling_score(self,ner,utterance) -> Tuple:
        pass

    @abstractmethod
    def handle_utterance(self, orchst : 'VHOrchestator', utterance : str) -> HAS_result:
        pass

    @abstractmethod
    def init_own_childs(self):
        pass