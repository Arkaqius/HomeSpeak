'''
Module contains common Nlp classes 
'''
from enum import Enum
from typing import Union


class NlpResultStatus(Enum):
    """
    Enum representing various statuses for NLP results.

    Attributes:
    - UNKNOWN: The result of the NLP process is unknown.
    - SUCCESS: The NLP process successfully extracted the required entities.
    - FAILURE: The NLP process failed to extract the required entities.
    - NOT_FOUND: The required entity was not found in the input.
    - NO_RESPONSE: The system did not provide a response.
    - UNKNOWN_ENTITY: An entity found is not recognized.
    - UNKNOWN_ACTION: The recognized entity does not support the identified action.
    - NEED_MORE_INFO: The system needs more information to proceed.
    """

    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILURE = "failure"
    NOT_FOUND = "not_found"
    NO_RESPONSE = "no_response"
    UNKNOWN_ENTITY = "unknown_entity"
    UNKNOWN_ACTION = "unknown_action"
    NEED_MORE_INFO = 'need_more_info'


class NlpResult:
    """
    Represents the result of an NLP process.

    Attributes:
    - status (NLP_result_status): The status of the NLP result.
    - dialog_to_say (str): The response dialog associated with the result.

    Methods:
    - is_successful: Checks if the NLP result status is successful.
    - set_state: Sets the state and associated dialog of the NLP result.
    """

    def __init__(self, status: NlpResultStatus, dialog_to_say: str):
        """
        Initializes a new instance of the NLP_result class.

        Args:
        - status (NLP_result_status): The status of the NLP result.
        - dialog_to_say (str): The response dialog associated with the result.
        """
        self.status: NlpResultStatus = status
        self.dialog_to_say: str = dialog_to_say

    def is_successful(self) -> bool:
        """
        Checks if the NLP result status is successful.

        Returns:
        - bool: True if the status is SUCCESS, False otherwise.
        """
        return self.status == NlpResultStatus.SUCCESS

    def set_state(self, status: NlpResultStatus, dialog: Union[str, None] = None):
        """
        Sets the state and associated dialog of the NLP result.

        Args:
        - status (NLP_result_status): The new status to set.
        - dialog (Union[str, None]): The associated dialog. Default is None.

        If no dialog is provided, the dialog will be set to a default message.
        """
        self.status = status
        self.dialog_to_say = dialog if dialog else "No dialog provided."
