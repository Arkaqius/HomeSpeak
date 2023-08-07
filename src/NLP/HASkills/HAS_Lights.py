from __future__ import annotations
import NLP.HASkills.common.HAS_enums as HAS_enums
from typing import List, Dict, Any, TYPE_CHECKING
from .common.HAS_common import HAS_find
from .HAS_Base import HAS_Base
from ..NER.NER_result import NER_result
from ..NLP_common import NLP_result, NLP_result_status
from HomeAssistantAPI.homeassistant_api.errors import RequestTimeoutError

if TYPE_CHECKING:
    from VHOrchestator import VHOrchestator


class HAS_Lights(HAS_Base):
    """
    A class used to handle voice request to lights thing type.

    Attributes:
    SUPPORT_BRIGHTNESS, SUPPORT_COLOR_TEMP, SUPPORT_EFFECT, SUPPORT_FLASH,
    SUPPORT_COLOR, SUPPORT_TRANSITION, SUPPORT_WHITE_VALUE, BRIGHNTESS_STEP:
    These constants represent bitfield of different supported features of lights.
    """

    SUPPORT_BRIGHTNESS = 1
    SUPPORT_COLOR_TEMP = 2
    SUPPORT_EFFECT = 4
    SUPPORT_FLASH = 8
    SUPPORT_COLOR = 16
    SUPPORT_TRANSITION = 32
    SUPPORT_WHITE_VALUE = 128
    BRIGHNTESS_STEP = 25  # in %

    def handle_utterance(
        self, orchst: "VHOrchestator", ner_result: NER_result, utterance: str
    ) -> NLP_result | None:
        """
        Handles a given utterance by checking for matching entities, choosing a winner, and delegating action handling
        to dedicated functions.

        Args:
            orchst (VHOrchestator): The orchestator object to use.
            ner_result (NER_result): The result of named entity recognition.
            utterance (str): The utterance to handle.

        Returns:
            NLP_result: The result of NLP skill, overall outcome
        """

        # 10. Prepare object to return
        result = NLP_result(
            NLP_result_status.UNKNOWN, "ERROR : HAS lights skill failed"
        )

        # 20. Looking for matching entities
        candidates: List[Dict[str, Any]] = HAS_find.find_candidates(
            HAS_Lights.build_suggest_entity_name(ner_result),
            orchst.HA_entity_group_lights.entities,
        )

        # 30. Choose winner
        winner_entity: Dict[str, Any] = HAS_Lights.choose_winner(candidates)

        # 40. If winner was not found decide to fail execution or ask user for more details
        if winner_entity is None:
            result.set_state(NLP_result_status.NEED_MORE_INFO)

        # 50. Delegation of action handling to dedicated functions
        else:
            action = ner_result.action.lower() if ner_result.action else None
            attribute = ner_result.action.lower() if ner_result.action else None

            # ON/OFF
            if action in [
                HAS_enums.Actions.ON.name.lower(),  # type: ignore
                HAS_enums.Actions.OFF.name.lower(),  # type: ignore
            ]:
                self.handle_request_turn_onoff(
                    ner_result, winner_entity, orchst, result
                )

            # Binary query
            elif (
                action == HAS_enums.Actions.BINARY_QUERY.name.lower()  # type: ignore
                and attribute == HAS_enums.States.POWERED.name.lower()  # type: ignore
            ):
                self.handle_req_binary_query(winner_entity, result)

            # Brightness
            elif (
                (action == HAS_enums.Actions.ADJUST.name.lower() or action == HAS_enums.Actions.INCREASE.name.lower( # type: ignore
                ) or action == HAS_enums.Actions.DECREASE.name.lower())  # type: ignore
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()  # type: ignore
            ):
                self.handle_request_change_brightness(
                    ner_result, winner_entity, orchst, result)

            # Informational query
            elif (
                action == HAS_enums.Actions.INFORMATION_QUERY.name.lower()  # type: ignore
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()  # type: ignore
            ):
                self.handle_req_info_query_brgth(winner_entity, result)

            else:
                result.set_state(NLP_result_status.UNKNOWN_ACTION)

        return result

    def get_req_score(self, ner_result: NER_result):
        """
        Returns a score how good request can be handled by that skill.
        TODO Add more logic

        Args:
            ner_result (NER_result): The result of named entity recognition.

        Returns:
            int: 100 if the NER result is a light, 0 otherwise. - Simple logic
        """

        if HAS_enums.Things.LIGHT.name.lower() == ner_result.thing:  # type: ignore
            return 100
        else:
            return 0

    def handle_request_turn_onoff(
        self,
        ner_result: NER_result,
        winner_entity: Dict[str, Any],
        VH_orch: "VHOrchestator",
        result: NLP_result,
    ) -> None:
        """
        Handles a request to turn the light on or off.

        Args:
            ner_result (NER_result): The result of named entity recognition.
            winner_entity (Dict[str, Any]): The winning entity to use.
            VH_orch (VHOrchestator): The orchestator object to use.
            result (NLP_result): The dialogue result to modify.
        """
        entity_id = winner_entity["entity"].entity_id
        friendly_name = winner_entity["entity"].state.attributes["friendly_name"]
        try:
            VH_orch.hass_instance.trigger_service(
                "light",
                "turn_" + str.lower(ner_result.action),
                entity_id=f"{entity_id}",
            )
            result.set_state(
                NLP_result_status.SUCCESS, f"Ok, I will turn on {friendly_name}"
            )
        except RequestTimeoutError:
            result.set_state(
                NLP_result_status.FAILURE, "No connection to Home Assistant server"
            )

    def handle_req_binary_query(
        self,
        winner_entity: Dict[str, Any],
        result: NLP_result,
    ) -> None:
        """
        Handles a binary query by getting the state of the winner entity and updating the dialogue result.

        Args:
            winner_entity (Dict[str, Any]): The winning entity to use.
            result (NLP_result): The dialogue result to modify.
        """
        friendly_name = winner_entity["entity"].state.attributes["friendly_name"]
        try:
            winner_entity["entity"].get_state()
            result.set_state(
                NLP_result_status.SUCCESS,
                f"{friendly_name} is {winner_entity['entity'].state.state}",
            )
        except RequestTimeoutError:
            result.set_state(
                NLP_result_status.FAILURE, "No connection to Home Assistant server"
            )

    def handle_request_change_brightness(
        self,
        ner_result: NER_result,
        winner_entity: Dict[str, Any],
        VH_orch: "VHOrchestator",
        result: NLP_result,
    ) -> None:
        """
        Handles a request to change the brightness of the light.

        Args:
            ner_result (NER_result): The result of named entity recognition.
            winner_entity (Dict[str, Any]): The winning entity to use.
            VH_orch (VHOrchestator): The orchestator object to use.
            result (NLP_result): The dialogue result to modify.
        """
        entity_id = winner_entity["entity"].entity_id
        friendly_name = winner_entity["entity"].state.attributes["friendly_name"]

        # Check if found light support brightness
        if (
            winner_entity.entity["attributes"]["supported_features"]
            & self.SUPPORT_BRIGHTNESS
        ):
            desired_brightness: float = 0
            brightness_type = ""
            if ner_result.action == HAS_enums.Actions.ADJUST.name.lower():  # type: ignore
                desired_brightness = ner_result.value
                brightness_type = "brightness_pct"
            elif ner_result.action == HAS_enums.Actions.INCREASE.name.lower():  # type: ignore
                desired_brightness = self.BRIGHNTESS_STEP
                brightness_type = "brightness_step_pct"
            elif ner_result.action == HAS_enums.Actions.DECREASE.name.lower():  # type: ignore
                desired_brightness = self.BRIGHNTESS_STEP * -1
                brightness_type = "brightness_step_pct"

            try:
                VH_orch.hass_instance.trigger_service(
                    "light",
                    "turn_on",
                    entity_id=f"{entity_id}",
                    **{brightness_type: f"{desired_brightness * 100}"},
                )
                result.set_state(
                    NLP_result_status.SUCCESS,
                    f"Ok, I will change brightness of {friendly_name}",
                )
            except RequestTimeoutError:
                result.set_state(
                    NLP_result_status.FAILURE, "No connection to Home Assistant server"
                )
        else:
            result.set_state(
                NLP_result_status.FAILURE,
                f"Light {friendly_name} does not support brightness feature.",
            )

    def handle_req_info_query_brgth(
        self,
        winner_entity: Dict[str, Any],
        result: NLP_result,
    ) -> None:
        """
        Handles an information query by getting the brightness of the winner entity and updating the dialogue result.

        Args:
            winner_entity (Dict[str, Any]): The winning entity to use.
            result (NLP_result): The dialogue result to modify.
        """
        friendly_name = winner_entity["entity"].state.attributes["friendly_name"]
        try:
            winner_entity["entity"].get_state()
            result.set_state(
                NLP_result_status.SUCCESS,
                f"{friendly_name} brightness level is set to {(float(winner_entity['entity'].state.attributes['brightness']) * 100/256)}",
            )
        except RequestTimeoutError:
            result.set_state(
                NLP_result_status.FAILURE, "No connection to Home Assistant server"
            )

    @staticmethod
    def choose_winner(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Choose the best candidate based on the highest similarity score.

        Args:
            candidates (List[Dict[str, Any]]): A list of candidate entities.

        Returns:
            Dict[str, Any]: The candidate with the highest similarity score.
        """

        return max(candidates, key=lambda x: x["similarity"])

    @staticmethod
    def build_suggest_entity_name(ner_result: NER_result):
        """
        Build a name to suggest an entity, based on the named entity recognition result. 
        This method constructs an expected light name using the NER result, which is 
        then used to find the closest match in the database.

        Args:
            ner_result (NER_result): The result of named entity recognition.

        Returns:
            str: A string that suggests an entity name, to be used in database search.
        """
        description = ""
        location = ""
        if ner_result.description:
            description = "_".join(list(ner_result.description))
        if ner_result.location:
            location = ner_result.location

        if description:
            description = "_" + description
        # Common pattern: light.<location>_<description>_light
        query = "light." + location.lower() + description + "_light"

        return query
