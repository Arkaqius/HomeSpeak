from abc import ABC, abstractmethod
from .common.HAS_request import HAS_request
from ...HomeAssistantAPI.homeassistant_api import Client
from .common.HAS_common import HAS_result

class HAS_Base(ABC):
    @abstractmethod
    def handle_utterance(self,request: HAS_request, HA_Client : Client) -> HAS_result:
        pass

    @abstractmethod
    def can_handle(self,request) -> bool:
        return False
    
    @staticmethod
    def _find_handler(request: HAS_request):
        for subclass in HAS_Base.__subclasses__():
            if subclass().can_handle(request):
                return subclass
        return None