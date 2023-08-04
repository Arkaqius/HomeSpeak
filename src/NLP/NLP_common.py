from enum import Enum

class NLP_result_status(Enum):
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILURE = "failure"
    NOT_FOUND = "not_found"
    NO_RESPONSE = "no_response"
    UNKNOWN_ENTITY = "entity_not_found"
    UNKNOWN_ACTION = "entity_not_support_action"
    NEED_MORE_INFO = 'need_more_informations'


class NLP_result:
    def __init__(self, status: NLP_result_status, dialog_to_say : str):
        self.status : NLP_result_status = status
        self.dialog_to_say : str = dialog_to_say

    def is_successful(self) -> bool:
        return self.status == NLP_result_status.SUCCESS
    
    def set_state(self,status : NLP_result_status , dialog : str | None = None):
        self.status = status
        self.dialog_to_say = dialog