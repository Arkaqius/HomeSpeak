from NLP.NER.config import *
from NLP.NER.VH_NER import VH_NER
from NLP.HASkills.common.HAS_request import HAS_request
from homeassistant_api import Client
from NLP.HASkills.HAS_Base import HAS_Base
from typing import Type, AnyStr
import SECRETS as sec
from NLP.NLP_skill import NLPSkill
from NLP.NLP_action import NLP_action
from NLP.NER.NER_result import NER_result

# Import all skills endpoint classes to register
from NLP.HASkills.HAS_Lights import HAS_Lights
from NLP.HASkills import HAS_Base


class VHOrchestator:
    """
    The VHOrchestrator class is responsible for processing requests and orchestrating
    actions between different parts of the system. This includes named entity recognition,
    handling user requests, and interacting with the Home Assistant API.
    """

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
            skill.init_own_childs()

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

    def _execute_results(utterence: AnyStr):
        """
        PlaceHolder
        """
        pass

    def _send_response():
        """
        PlaceHolder
        """
        pass

    def _run_request(self, utterance: str) -> None:
        """
        Processes the provided request,
        finds the appropriate handler for it and handles the utterance.

        Args:
            request (VH_Request): The request to be processed.

        """
        # 10. Perform NER analysis
        ner_raw_result = ner.process_text(utterance)
        ner_result: NER_result = NER_request(utterance, *ner_raw_result)

        # 20. Find best skill to handle utterance
        skill_to_call: NLPSkill = self._find_skill(utterance, ner_result)

        # 30. Call best skill to handle utterance
        action_to_perform: NLP_action = skill_to_call.handle_utterance(
            self, ner_result, utterance
        )

        # 40. Perform actions
        # TODO

        # 50. Speak dialog
        # TODO

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
