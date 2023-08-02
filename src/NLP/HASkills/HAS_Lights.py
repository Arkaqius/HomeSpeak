from __future__ import annotations
import NLP.HASkills.common.HAS_enums as HAS_enums
from typing import List, Dict, Any, TYPE_CHECKING
from .common.HAS_common import *
from .HAS_Base import HAS_Base
from ..NER.NER_result import NER_result
from ..NLP_common import NLP_result, NLP_result_status

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
            result.set_state(NLP_result_status.NEED_MORE_INFO, None)

        # 50. Delegation of action handling to dedicated functions
        else:
            action = ner_result.action.lower() if ner_result.action else None
            attribute = ner_result.action.lower() if ner_result.action else None

            # ON/OFF
            if action in [
                HAS_enums.Actions.ON.name.lower(),
                HAS_enums.Actions.OFF.name.lower(),
            ]:
                self.handle_request_turn_onoff(
                    ner_result, winner_entity, orchst, result
                )

            # Brightness
            elif (
                action == HAS_enums.Actions.ADJUST.name.lower()
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()
            ):
                dlg_result = self.handle_request_change_brightness(
                    request, winner_entity, VH_Orch
                )

            elif (
                action == HAS_enums.Actions.INCREASE.name.lower()
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()
            ):
                dlg_result = self.handle_request_increase_brightness(
                    request, winner_entity, VH_Orch
                )

            elif (
                action == HAS_enums.Actions.DECREASE.name.lower()
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()
            ):
                dlg_result = self.handle_request_decrease_brightness(
                    request, winner_entity, VH_Orch
                )

            elif (
                action == HAS_enums.Actions.BINARY_QUERY.name.lower()
                and attribute == HAS_enums.States.POWERED.name.lower()
            ):
                dlg_result = self.handle_req_bq(request, winner_entity, VH_Orch)

            elif (
                action == HAS_enums.Actions.INFORMATION_QUERY.name.lower()
                and attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()
            ):
                dlg_result = self.handle_req_iq_brgth(request, winner_entity, VH_Orch)

            else:
                dlg_result.set_state(HAS_requestStatus.UNKNOWN_ACTION)

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
        VH_Orch: "VHOrchestator",
        dlg_result: NLP_result,
    ) -> None:
        entity_id = winner_entity["entity"].entity_id
        try:
            VH_Orch.hass_instance.trigger_service(
                "light",
                "turn_" + str.lower(ner_result.action),
                entity_id=f"{entity_id}",
            )
            dlg_result.set_state(
                NLP_result_status.SUCCESS, "The operation was successful"
            )
        except:
            dlg_result.set_state(
                NLP_result_status.FAILURE, "No connection to Home Assistant server"
            )

    # def handle_req_bq(request, w_en, VH_Orch : 'VHOrchestator'):
    #     dlg_result = HAResult(HARequestStatus.SUCCESS)
    #     w_en['entity'].get_state()
    #     dlg_result.set_entitiy_state(w_en['entity'].state.state)
    #     return dlg_result

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
