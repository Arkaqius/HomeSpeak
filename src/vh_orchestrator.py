# pylint: disable=C0114
from typing import Optional
from vh_ner import VhNer, VhProcessedText
from homeassistant_api import Client
from ner_result import NerResult
from NLP.NER.config import PATH_TRAINED_MODEL
from nlp_skill import NLPSkill
from nlp_common import NlpResult, NlpResultStatus
import SECRETS as sec

# Import all skills endpoint classes to register
from NLP.HASkills.HAS_Lights import HAS_Lights  # pylint: disable=C0412, disable=W0611

# Custom exceptions
class NERProcessingError(Exception):
    pass


class SkillNotFoundError(Exception):
    pass


class VHOrchestator:
    """
    The VHOrchestrator class is responsible for processing requests and orchestrating
    actions between different parts of the system. This includes named entity recognition,
    handling user requests, and interacting with the Home Assistant API.
    """

    # Dialogs to say. Later, replace it with dialog files supported by voice OS.
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
        """
        Initializes the VHOrchestrator with instances of VH_NER for Named Entity Recognition,
        Home Assistant Client, and setups dictionaries for entities and skills.
        """
        # Instance of VH_NER for Named Entity Recognition
        self.ner: VhNer = VhNer(PATH_TRAINED_MODEL)
        # Instance of Home Assistant Client
        self.hass_instance: Client = Client(sec.URL, sec.TOKEN)
        # Dictionary containing all entities from Home Assistant
        self.all_entities: dict = self.hass_instance.get_entities()
        # Dictionary containing all light entities
        self.ha_entity_group_lights: dict = self.all_entities["light"]
        # All child classes instances that inherit from NLPSkills
        self.nlp_skills_dict = {
            skill.__name__: skill() for skill in NLPSkill.__subclasses__() # type: ignore We are instanting subclasses not parent, abstract class, pylint: disable=C0301
        }

        for skill in self.nlp_skills_dict.values():
            skill.init_own_children()

    def _find_skill(self, utterance: str, ner_result: NerResult) -> Optional[NLPSkill]:
        """
        Evaluates the user's utterance and NER results to determine which skill is best
        suited to handle the request.

        Args:
            utterance (str): The user's spoken phrase.
            ner_result (NER_result): The results of the Named Entity Recognition process on the utterance.

        Returns:
            Optional[NLPSkill]: The skill determined to be the best fit for the utterance or None if no skill is found.
        """
        skills_score: dict[NLPSkill, float] = {}

        for skill_instance in self.nlp_skills_dict.values():
            result_skill, result_skill_score = skill_instance.request_handling_score(
                ner_result, utterance)

            # Only add to the dictionary if result_skill is not None
            if result_skill is not None:
                skills_score[result_skill] = result_skill_score

        # Get the skill with the max score
        max_score_skill = max(
            skills_score, key=lambda skill: skills_score[skill], default=None)

        return max_score_skill

    def _send_response(self, response: NlpResult):
        """
        Evaluates the result of the skill's processing to determine and send the appropriate
        dialog response.

        Args:
            response (NLP_result): The results after processing by the selected skill.
        """

        # 10
        if response.status == NlpResultStatus.UNKNOWN:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.UNKNOWN_DIALOG)
        elif response.status == NlpResultStatus.SUCCESS:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.SUCCESS_DIALOG)
        elif response.status == NlpResultStatus.FAILURE:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.FAILURE_DIALOG)
        elif response.status == NlpResultStatus.NOT_FOUND:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.NOT_FOUND_DIALOG)
        elif response.status == NlpResultStatus.NO_RESPONSE:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.NO_RESPONSE_DIALOG)
        elif response.status == NlpResultStatus.UNKNOWN_ENTITY:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.UNKNOWN_ENTITY_DIALOG)
        elif response.status == NlpResultStatus.UNKNOWN_ACTION:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.UNKNOWN_ACTION_DIALOG)
        elif response.status == NlpResultStatus.NEED_MORE_INFO:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.NEED_MORE_INFO_DIALOG)
        else:
            VHOrchestator.say_dialog_stub(
                response.dialog_to_say if response.dialog_to_say else self.DEFAULT_DIALOG)

    @staticmethod
    def say_dialog_stub(dialog: str):
        """
        Simulates the system's verbal response by printing the dialog.

        Args:
            dialog (str): The text to be "spoken" by the system.
        """
        print(f"Dialog stub: {dialog} ")

    def _run_request(self, utterance: str) -> None:
        """
        Processes the provided request,
        finds the appropriate handler for it and handles the utterance.

        Args:
            utterance (str): The utterance to be processed.

        Raises:
            NERProcessingError: If the NER processing fails.
            SkillNotFoundError: If the skill was not found.

        """
        try:
            # 10. Perform NER analysis
            ner_raw_result: VhProcessedText = self.ner.process_text(utterance)
            if not ner_raw_result.named_entities:
                raise NERProcessingError("NER processing failed")

            text_process_result: NerResult = NerResult(
                utterance, ner_raw_result)
            print(f"ner_result: {text_process_result}")

            # 20. Find best skill to handle utterance
            skill_to_call: Optional[NLPSkill] = self._find_skill(
                utterance, text_process_result)
            if not skill_to_call:
                raise SkillNotFoundError("Skill was not found")

            # 30. Call best skill to handle utterance
            action_to_perform: NlpResult = skill_to_call.handle_utterance(
                self, text_process_result, utterance
            )

            # 50. Speak dialog
            self._send_response(action_to_perform)

        except (NERProcessingError, SkillNotFoundError) as exception:
            print(exception)

    def test_mode(self) -> None:
        """
        Enters a test mode where the user can manually enter utterances or predefined commands for processing.
        """
        while True:
            user_input: str = input(
                "Enter an utterance or type 'quit' to exit: ")

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
