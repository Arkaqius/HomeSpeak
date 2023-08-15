from abc import ABC, abstractmethod
from typing import Tuple, TYPE_CHECKING
from .NER.NER_result import NER_result
from .NLP_common import NLP_result

if TYPE_CHECKING:
    from VHOrchestator import VHOrchestator


class NLPSkill(ABC):
    """
    Abstract base class representing an NLP skill. Any specific NLP skill should subclass
    this class and implement its abstract methods.

    This class provides a framework for:
    1. Scoring a request to determine the suitability of the skill for handling it.
    2. Handling an utterance based on extracted entities.
    3. Initializing the child elements or processes specific to the skill.

    Methods:
    - request_handling_score: Returns a score indicating the suitability of the skill for handling a request.
    - handle_utterance: Processes the utterance and returns the result.
    - init_own_children: Initializes the child elements or processes specific to the skill.
    """

    @abstractmethod
    def request_handling_score(self, ner_result: NER_result, utterance: str) -> Tuple[float, str]:
        """
        Calculates and returns a score indicating the suitability of the skill for 
        handling the given request based on the named entity recognition result and 
        the utterance itself.

        Args:
        - ner_result (NER_result): The result of named entity recognition.
        - utterance (str): The original user input.

        Returns:
        - Tuple[float, str]: A tuple containing a score (float) and a debug message (str).
        """
        pass

    @abstractmethod
    def handle_utterance(
        self, orchst: "VHOrchestator", ner_result: NER_result, utterance: str
    ) -> NLP_result:
        """
        Processes the utterance based on extracted entities and returns the result.

        Args:
        - orchst (VHOrchestator): An instance of the orchestrator that manages multiple NLP skills.
        - ner_result (NER_result): The result of named entity recognition.
        - utterance (str): The original user input.

        Returns:
        - NLP_result: The result of processing the utterance.
        """
        pass

    @abstractmethod
    def init_own_children(self) -> None:
        """
        Initializes the child elements or processes specific to the skill. This method 
        should be overridden to set up any child processes or data structures that 
        are unique to the specific NLP skill.
        """
        pass