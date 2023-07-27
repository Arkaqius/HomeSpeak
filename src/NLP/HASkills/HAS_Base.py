from abc import abstractmethod
from .common.HAS_request import HAS_request
from HomeAssistantAPI.homeassistant_api import Client
from .common.HAS_common import HAS_result
from ..NLP_skill import NLPSkill
from .HAS_Lights import HMI_Lights

class HAS_Base(NLPSkill):
    @staticmethod
    def request_handling_score(utterance):
        handler = HAS_Base._find_handler(utterance)
        if handler is not None:
            # here you may want to get a score from the handler or 
            # just return a static score
            return 1  # or any other scoring mechanism
        return 0  # return 0 if no handler is found
    
    @staticmethod
    def _find_handler(request: HAS_request):
        for subclass in HAS_Base.__subclasses__():
            if subclass().can_handle(request):
                return subclass
        return None

    @abstractmethod
    def handle_utterance(self,request: HAS_request, HA_Client : Client) -> HAS_result:
        pass

    @abstractmethod
    def can_handle(self,request) -> bool:
        return False


    