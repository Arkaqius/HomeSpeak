from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from VHOrchestator import VHOrchestator


class NLPSkill(ABC):
    @abstractmethod
    def request_handling_score(self, ner_result: NER_result, utterance: str) -> Tuple:
        pass

    @abstractmethod
    def handle_utterance(
        self, orchst: "VHOrchestator", ner_result: NER_result, utterance: str
    ) -> HAS_result:
        pass

    @abstractmethod
    def init_own_childs(self):
        pass
