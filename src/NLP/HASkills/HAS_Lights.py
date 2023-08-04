from __future__ import annotations
import NLP.HASkills.common.HAS_enums as HAS_enums
from typing import List, Dict, Any, TYPE_CHECKING
from .common.HAS_common import *
from .HAS_Base import HAS_Base
from ..NER.NER_result import NER_result
from ..NLP_common import NLP_result, NLP_result_status
from HomeAssistantAPI.homeassistant_api.errors import RequestTimeoutError

if TYPE_CHECKING:
    from VHOrchestator import VHOrchestator


class HAS_Lights(HAS_Base):
    """
    HA supported features bit
    """

    SUPPORT_BRIGHTNESS = 1
    SUPPORT_COLOR_TEMP = 2
    SUPPORT_EFFECT = 4
    SUPPORT_FLASH = 8
    SUPPORT_COLOR = 16
    SUPPORT_TRANSITION = 32
    SUPPORT_WHITE_VALUE = 128
    BRIGHNTESS_STEP = 25  # in %

    def __init__(self):
        super().__init__()

    def handle_utterance(
        self, orchst: "VHOrchestator", ner_result: NER_result, utterance: str
    ) -> NLP_result:
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
                (action == HAS_enums.Actions.ADJUST.name.lower() or action == HAS_enums.Actions.INCREASE.name.lower() or action == HAS_enums.Actions.DECREASE.name.lower())  # type: ignore
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()  # type: ignore
            ):
                self.handle_request_change_brightness(
                    request, winner_entity, VH_Orch
                )
            
            # Informational query
            elif (
                action == HAS_enums.Actions.INFORMATION_QUERY.name.lower() # type: ignore
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()  # type: ignore
            ):
                result = self.handle_req_iq_brgth(request, winner_entity, VH_Orch)

            else:
                result.set_state(NLP_result_status.UNKNOWN_ACTION)

        return result

    def get_req_score(self, ner_result: NER_result):
        if HAS_enums.Things.LIGHT.name.lower() == ner_result.thing:
            return 100
        else:
            return 0

    def handle_request_turn_onoff(
        self,
        ner_result: NER_result,
        winner_entity: Dict[str, Any],
        VH_orch: "VHOrchestator",
        dlg_result: NLP_result,
    ) -> None:
        entity_id = winner_entity["entity"].entity_id
        friendly_name = winner_entity['entity'].state.attributes['friendly_name']
        try:
            VH_orch.hass_instance.trigger_service(
                "light",
                "turn_" + str.lower(ner_result.action),
                entity_id=f"{entity_id}",
            )
            dlg_result.set_state(
                NLP_result_status.SUCCESS, f"Ok, I will turn on {friendly_name}"
            )
        except RequestTimeoutError:
            dlg_result.set_state(
                NLP_result_status.FAILURE, "No connection to Home Assistant server"
            )

    def handle_req_binary_query(
        self,
        winner_entity: Dict[str, Any],
        dlg_result: NLP_result,
    ) -> None:
        friendly_name = winner_entity['entity'].state.attributes['friendly_name']
        try:
            winner_entity["entity"].get_state()
            dlg_result.set_state(
                NLP_result_status.SUCCESS, f"{friendly_name} is {winner_entity['entity'].state.state}"
            )
        except RequestTimeoutError:
            dlg_result.set_state(
                NLP_result_status.FAILURE, "No connection to Home Assistant server"
            )

    def handle_request_change_brightness(
            self,
            ner_result: NER_result,
            winner_entity: Dict[str, Any],
            VH_orch: "VHOrchestator",
            dlg_result: NLP_result,
        ) -> None:
        ''' Handle changing brigtness to exact value'''
        entity_id = winner_entity["entity"].entity_id
        friendly_name = winner_entity['entity'].state.attributes['friendly_name']    
        # Check if found light support brightness
        if winner_entity.entity['attributes']['supported_features'] & self.SUPPORT_BRIGHTNESS:
            desired_brightness : float = 0
            if ner_result.action == HAS_enums.Actions.ADJUST.name.lower():
                desired_brightness = ner_result.value
            elif ner_result.action == HAS_enums.Actions.INCREASE.name.lower():
                desired_brightness = self.BRIGHNTESS_STEP
            elif ner_result.action == HAS_enums.Actions.DECREASE.name.lower():
                desired_brightness = self.BRIGHNTESS_STEP * -1

            try:
                VH_orch.hass_instance.trigger_service(  "light",
                                                        'turn_on',
                                                        entity_id=f"{entity_id}",
                                                        brightness_pct=f"{desired_brightness * 100}"
                
                dlg_result.set_state(
                    NLP_result_status.SUCCESS, f"Ok, I will change brightness of {friendly_name}"
                )
            except RequestTimeoutError:
                dlg_result.set_state(
                    NLP_result_status.FAILURE, "No connection to Home Assistant server"
                )
        else:
            dlg_result.set_state(
                NLP_result_status.FAILURE, "Light {friendly_name} does not support brightness feature."
            )           



    # def handle_req_iq_brgth(request, w_en, HAS_inst):
    #     entity_id = w_en.entity['entity_id']
    #     state = HAS_inst.HA._get_state(entity_id)
    #     HAS_inst.speak_dialog('LIGHT_IQ_BRIGHTNESS',
    #                           {'friendly_name':   entity_id,
    #                            'brg_level':   (float(state['attributes']['brightness']) * 100/256)
    #                            })
    #     return None

    # def handle_request_change_brightness(request, w_en, HAS_inst):
    #     ''' Handle changing brigtness to exact value'''
    #     # Check if found light support brightness
    #     if w_en.entity['attributes']['supported_features'] & self.SUPPORT_BRIGHTNESS:
    #         entity_id = w_en.entity['entity_id']
    #         HAS_inst.HA.execute_service('light',
    #                                     'turn_on',
    #                                     {'entity_id': f'{entity_id}',
    #                                      'brightness_pct': f'{request.value * 100}'})
    #         dialog_rtn = HMI_dlg_rtn.SUCCESS
    #     else:
    #         dialog_rtn = HMI_dlg_rtn.UF_BRIGHTNESS

    #     return dialog_rtn

    # def handle_request_increase_brightness(request, w_en, HAS_inst):
    #     entity_id = w_en.entity['entity_id']
    #     HAS_inst.HA.execute_service('light',
    #                                 'turn_on',
    #                                 {'entity_id': f'{entity_id}',
    #                                  'brightness_step_pct': f'{self.BRIGHNTESS_STEP}'})
    #     return HMI_dlg_rtn.SUCCESS

    # def handle_request_decrease_brightness(request, w_en, HAS_inst):
    #     entity_id = w_en.entity['entity_id']
    #     HAS_inst.HA.execute_service('light',
    #                                 'turn_on',
    #                                 {'entity_id': f'{entity_id}',
    #                                  'brightness_step_pct': f'{self.BRIGHNTESS_STEP * -1}'})
    #     return HMI_dlg_rtn.SUCCESS

    @staticmethod
    def choose_winner(candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
        return max(candidates, key=lambda x: x["similarity"])

    @staticmethod
    def build_suggest_entity_name(ner_result: NER_result):
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
