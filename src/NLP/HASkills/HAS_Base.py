from abc import abstractmethod
from ..NLP_skill import NLPSkill
from typing import Tuple, TYPE_CHECKING, Optional
from ..NER.ner_result import NerResult
from ..NLP_common import NLP_result

if TYPE_CHECKING:
    from vh_orchestrator import VHOrchestator


class HAS_Base(NLPSkill):
    """
    Base class for Home Assistant Skills.

    Represents the foundation for all Home Assistant-related skills and provides methods
    for handling natural language processing (NLP) results and invoking the appropriate
    skills based on NLP/NER results.

    Attributes:
        child_skills_dict (dict): A dictionary containing all child classes that inherit 
                                  from `HAS_Base` indexed by their class names.
    """

    def __init__(self):
        """
        Initializes a new instance of the `HAS_Base` class.
        """
        self.child_skills_dict: dict[str, 'HAS_Base'] = {}

    def init_own_children(self):
        """
        Initializes the `child_skills_dict` attribute with instances of all subclasses of `HAS_Base`.
        """
        self.child_skills_dict = {
            skill.__name__: skill() for skill in HAS_Base.__subclasses__()
        }  # All child classes instances that inherit from HAS_Base

    def request_handling_score(self, ner_result: NerResult, _: str) -> Tuple[Optional['HAS_Base'], float]:
        """
        Determine the best handler for a given NER result.

        Args:
            ner_result (NER_result): The NER result to find a handler for.
            _ (str): An unused argument. [Consider providing more details if it has potential use in future.]

        Returns:
            Tuple[Optional[HAS_Base], int]: A tuple containing the handler (or None) and the score.
        """
        handler, best_score = self._find_handler(ner_result)
        if handler is not None:
            return (handler, best_score)
        return (None, 0)

    def _find_handler(self, ner_result: NerResult) -> Tuple[Optional['HAS_Base'], float]:
        """
        Internal method to find the most suitable handler for a given NER result.

        Args:
            ner_result (NER_result): The NER result to evaluate.

        Returns:
            Tuple[Optional[HAS_Base], int]: A tuple containing the best handler and its associated score.
                                          Returns (None, 0) if no suitable handler is found.
        """
        best_score = 0
        best_handler = None
        for subclass_inst in self.child_skills_dict.values():
            score = subclass_inst.get_req_score(ner_result)
            if score > best_score:
                best_score = score
                best_handler = subclass_inst
        return best_handler, best_score

    def get_req_score(self, ner_result: NerResult):
        """
        Get the request score for a given NER result.

        This method should be implemented in subclasses to provide specific scoring mechanisms.

        Args:
            ner_result (NER_result): The NER result to score.

        Raises:
            NotImplementedError: This method needs to be implemented in subclasses.
        """
        raise NotImplementedError(
            "This method should be overridden in subclasses.")

    def handle_utterance(
        self, orchst: "VHOrchestator", ner_result: NerResult, utterance: str
    ) -> NLP_result:
        """
        Handles the provided utterance based on the NER result.

        This method should be implemented in subclasses to provide specific action based on the user's utterance 
        and the derived NER result.

        Args:
            orchst (VHOrchestator): The orchestration instance to use.
            ner_result (NER_result): The NER result associated with the utterance.
            utterance (str): The user's utterance.

        Raises:
            NotImplementedError: This method needs to be implemented in subclasses.
        """
        raise NotImplementedError(
            "This method should be overridden in subclasses.")
