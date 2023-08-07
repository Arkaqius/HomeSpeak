from NLP.NER.config import *
from NLP.NER.VH_NER import VH_NER
from NLP.NER.NER_result import NER_result
from homeassistant_api import Client
from NLP.HASkills.HAS_Base import HAS_Base
from typing import Type, AnyStr
import SECRETS as sec
from NLP.NLP_skill import NLPSkill
from NLP.NLP_common import NLP_result, NLP_result_status

# Import all skills endpoint classes to register
from NLP.HASkills.HAS_Lights import HAS_Lights
from NLP.HASkills import HAS_Base


class VHOrchestator:
    """
    The VHOrchestrator class is responsible for processing requests and orchestrating
    actions between different parts of the system. This includes named entity recognition,
    handling user requests, and interacting with the Home Assistant API.
    """

    """
    Dialogs to say. Later, replace it with dialog files supported by voice OS.
    """
    UNKNOWN_DIALOG = "I'm sorry, I couldn't understand that."
    SUCCESS_DIALOG = "The operation was successful."
    FAILURE_DIALOG = "I'm sorry, there was a problem with the operation."
    NOT_FOUND_DIALOG = "I'm sorry, I couldn't find what you were looking for."
    NO_RESPONSE_DIALOG = "I'm sorry, I didn't receive a response."
    UNKNOWN_ENTITY_DIALOG = "I'm sorry, I couldn't identify the entity."
    UNKNOWN_ACTION_DIALOG = "I'm sorry, that action is not supported."
    NEED_MORE_INFO_DIALOG = "Can you provide more information?"
    DEFAULT_DIALOG = "I'm sorry, an unexpected error occurred."

    def __init__(self) -> None:
        """Initializes the VHOrchestrator."""
        # Instance of VH_NER for Named Entity Recognition
        self.ner: VH_NER = VH_NER(PATH_TRAINED_MODEL)
        # Instance of Home Assistant Client
        self.hass_instance: Client = Client(sec.URL, sec.TOKEN)
        # Dictionary containing all entities from Home Assistant
        self.all_entities: dict = self.hass_instance.get_entities()
        # Dictionary containing all light entities
        self.HA_entity_group_lights: dict = self.all_entities["light"]
        # All child classes instances that inherit from NLPSkills
        self.nlp_skills_dict = {
            skill.__name__: skill() for skill in NLPSkill.__subclasses__()
        }

        for skill in self.nlp_skills_dict.values():
            skill.init_own_children()

    def _find_skill(self, utterance: AnyStr, ner_result: NER_result):
        skills_score: dict = {}

        for skill_instance in self.nlp_skills_dict.values():
            result_skill, result_skill_score = skill_instance.request_handling_score(
                ner_result, utterance
            )
            skills_score[result_skill] = result_skill_score

        # Get the skill with the max score
        max_score_skill = max(skills_score, key=skills_score.get)

        return max_score_skill
    
    def _send_response(self,response: NLP_result):
        """
        PlaceHolder
        """
        
        # 10
        if response.status == NLP_result_status.UNKNOWN:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.UNKNOWN_DIALOG)
        elif response.status == NLP_result_status.SUCCESS:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.SUCCESS_DIALOG)
        elif response.status == NLP_result_status.FAILURE:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.FAILURE_DIALOG)
        elif response.status == NLP_result_status.NOT_FOUND:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.NOT_FOUND_DIALOG)
        elif response.status == NLP_result_status.NO_RESPONSE:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.NO_RESPONSE_DIALOG)
        elif response.status == NLP_result_status.UNKNOWN_ENTITY:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.UNKNOWN_ENTITY_DIALOG)
        elif response.status == NLP_result_status.UNKNOWN_ACTION:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.UNKNOWN_ACTION_DIALOG)
        elif response.status == NLP_result_status.NEED_MORE_INFO:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.NEED_MORE_INFO_DIALOG)
        else:
            VHOrchestator.say_dialog_stub(response.dialog_to_say if response.dialog_to_say else self.DEFAULT_DIALOG)

    @staticmethod
    def say_dialog_stub(dialog: str):
        print(f"Dialog stub: {dialog} ")

    def _run_request(self, utterance: str) -> None:
        """
        Processes the provided request,
        finds the appropriate handler for it and handles the utterance.

        Args:
            request (VH_Request): The request to be processed.

        """
        # 10. Perform NER analysis
        ner_raw_result = self.ner.process_text(utterance)
        ner_result: NER_result = NER_result(utterance, *ner_raw_result)
        print(f"ner_result:{ner_result}")

        # 20. Find best skill to handle utterance
        skill_to_call: NLPSkill = self._find_skill(utterance, ner_result)

        # 30. Call best skill to handle utterance
        action_to_perform: NLP_result = skill_to_call.handle_utterance(
            self, ner_result, utterance
        )

        # 50. Speak dialog
        self._send_response(action_to_perform)

    def testMode(self) -> None:
        """
        Enters a test mode where the user can manually enter utterances or predefined commands for processing.
        """
        while True:
            user_input: str = input("Enter an utterance or type 'quit' to exit: ")

            if user_input.lower() == "quit":
                break

            # Check if the user input matches any predefined inputs and set user_input to the corresponding sentence
            predefined_inputs = {
                "1": "turn on lights in office",
                "2": "turn off kitchen light",
                "3": "set warm water to eco",
            }
            if user_input.strip() in predefined_inputs:
                user_input = predefined_inputs[user_input.strip()]

            # Call the run_request method to handle utterence
            self._run_request(user_input)
