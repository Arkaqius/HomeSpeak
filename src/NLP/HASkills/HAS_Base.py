from abc import abstractmethod
from .common.HAS_request import HAS_request
from HomeAssistantAPI.homeassistant_api import Client
from .common.HAS_common import HAS_result
from ..NLP_skill import NLPSkill
from typing import Dict
import inspect,sys
from NLP.NER.VH_NER import VH_NER

class HAS_Base(NLPSkill):
    @staticmethod
    def request_handling_score(ner : VH_NER,utterance : str):
        req : HAS_request = HAS_request(utterance,*ner.process_text(utterance))
        handler, best_score = HAS_Base._find_handler(req)
        if handler is not None:
            return best_score
        return 0
    
    @staticmethod
    def _find_handler(request: HAS_request):
        score_dict: dict = {}
        for subclass in HAS_Base.__subclasses__():
            score = subclass().get_req_score(request)
            score_dict[subclass] = score
        max_score_subclass = max(score_dict, key=score_dict.get)
        max_score = score_dict[max_score_subclass]
        if max_score == 0:
            return None, 0
        else:
            return max_score_subclass, max_score

    @abstractmethod
    def handle_utterance(self,request: HAS_request, HA_Client : Client) -> HAS_result:
        pass

    @staticmethod
    def get_subclasses():
        subclasses = []
        for name, obj in inspect.getmembers(sys.modules[__name__]):
            if inspect.isclass(obj) and issubclass(obj, HAS_Base) and obj != HAS_Base:
                subclasses.append(obj)
        return subclasses


    