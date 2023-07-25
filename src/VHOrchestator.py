import config as cfg
import typing as T

from NER.VH_NER import VH_NER
from tokenSkills.common.VH_Request import VH_Request
from homeassistant_api import Client
from tokenSkills.HA_direct.HMI.HMI_Common import HMI_ActionBase
from typing import Type
from tokenSkills.HA_direct.SECRETS import *


class VHOrchestator():
    """
    The VHOrchestrator class is responsible for processing requests and orchestrating 
    actions between different parts of the system. This includes named entity recognition,
    handling user requests, and interacting with the Home Assistant API.
    """
    def __init__(self) -> None:
        """Initializes the VHOrchestrator."""
        self.ner: VH_NER = VH_NER(cfg.PATH_TRAINED_MODEL)  # Instance of VH_NER for Named Entity Recognition
        self.hass_instance: Client = Client(URL, TOKEN)    # Instance of Home Assistant Client
        self.allEntities: dict = self.hass_instance.get_entities()  # Dictionary containing all entities from Home Assistant
        self.HA_entity_group_lights: dict = self.allEntities['light']  # Dictionary containing all light entities

    def run_request(self, request: VH_Request) -> None:
        """
        Processes the provided request, finds the appropriate handler for it and handles the utterance.

        Args:
            request (VH_Request): The request to be processed.

        """
        # Find a handler for the request and handle the utterance
        handler: Type[HMI_ActionBase] = HMI_ActionBase._find_handler(request)
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
            req = VH_Request(user_input, named_entities, numerical_values)
            # Call the run_request method to handle the VH_Request using Home Assistant module
            self.run_request(req)
