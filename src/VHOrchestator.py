from NLP.NER.config import *
from NLP.NER.VH_NER import VH_NER
from NLP.HASkills.common.HAS_request import HAS_request
from homeassistant_api import Client
from NLP.HASkills.HAS_Base import HAS_Base
from typing import Type,AnyStr
import SECRETS as sec


class VHOrchestator():
    """
    The VHOrchestrator class is responsible for processing requests and orchestrating 
    actions between different parts of the system. This includes named entity recognition,
    handling user requests, and interacting with the Home Assistant API.
    """
    def __init__(self) -> None:
        """Initializes the VHOrchestrator."""
        self.ner: VH_NER = VH_NER(PATH_TRAINED_MODEL)  # Instance of VH_NER for Named Entity Recognition
        self.hass_instance: Client = Client(sec.URL, sec.TOKEN)    # Instance of Home Assistant Client
        self.allEntities: dict = self.hass_instance.get_entities()  # Dictionary containing all entities from Home Assistant
        self.HA_entity_group_lights: dict = self.allEntities['light']  # Dictionary containing all light entities

    
    def _find_skill(utterence: AnyStr):
        """
        PlaceHolder
        """
        pass

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

    def _run_requestTODO(self, request: HAS_request) -> None:
        """
        Processes the provided request, finds the appropriate handler for it and handles the utterance.

        Args:
            request (VH_Request): The request to be processed.

        """
        # Find a handler for the request and handle the utterance
        handler: Type[HAS_Base] = HAS_Base._find_handler(request)
        if handler is not None:
            result = handler().handle_utterance(request, self)
            print(result)  # TODO Debug
        else:
            print("Handler not found for the request.")

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
                "3": "set warm water to eco"
            }
            if user_input.strip() in predefined_inputs:
                user_input = predefined_inputs[user_input.strip()]

            # Process the user input using Named Entity Recognition
            named_entities, numerical_values = self.ner.process_text(user_input)
            print("Named entities:")
            for entity, label in named_entities.items():
                print(f"{entity}: {label}")

            print("Values:")
            if numerical_values:
                for val in numerical_values:
                    print(f"{val}")

            # Create a VH_Request object with the extracted named entities and numerical values
            req = HAS_request(user_input, named_entities, numerical_values)
            # Call the run_request method to handle the VH_Request using Home Assistant module
            self._run_requestTODO(req)
