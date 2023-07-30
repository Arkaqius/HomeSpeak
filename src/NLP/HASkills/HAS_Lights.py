from __future__ import annotations
import NLP.HASkills.common.HAS_enums as HAS_enums
from typing import List, Dict, Any
from .common.HAS_request import HAS_request
from .common.HAS_common import *
from .HAS_Base import HAS_Base

class HAS_Lights(HAS_Base):
    '''
    HA supported features bit
    '''
    SUPPORT_BRIGHTNESS = 1
    SUPPORT_COLOR_TEMP = 2
    SUPPORT_EFFECT = 4
    SUPPORT_FLASH = 8
    SUPPORT_COLOR = 16
    SUPPORT_TRANSITION = 32
    SUPPORT_WHITE_VALUE = 128
    BRIGHNTESS_STEP = 25  # in %

    def __init__(self):
        pass

    def get_req_score(self, request):
        if (HAS_enums.Things.LIGHT.name.lower() == request.thing):
            return 100
        else:
            return 0

    def handle_utterence(self,utterance : str, ner = None, ner_data = None) -> HAS_result:
        
        dlg_result = HAS_result(HAS_requestStatus.UNKNOWN)

        request_to_handle =  self.latest_utterance_data['ner_result']

        # Everything to TODO below!
        
        # Create queary and find matchign candidates
        candidates = HAS_find.find_candidates(HAS_Lights.build_suggest_entity_name(request_to_handle),
                                              VH_Orch.HA_entity_group_lights.entities)
        # Choose one or ask for more specific information
        w_en = HMI_Lights.choose_winner(candidates)
        if w_en is None:
           dlg_result.set_state(HAS_requestStatus.UNKNOWN_ENTITY)
        else:
            # Determinate which action shall be run
            # Simple ON/OFF
            if (request.action == HAS_enums.Actions.ON.name.lower() or request.action == HAS_enums.Actions.OFF.name.lower()):
                dlg_result = self.handle_request_turn_onoff(request, w_en, VH_Orch)
            #Change brightness to exact value
            elif(request.action == HAS_enums.Actions.ADJUST.name.lower() and request.attribute == HAS_enums.Attributes.BRIGTHNESS.name.lower()):
                dlg_result = self.handle_request_change_brightness(request,w_en,VH_Orch)
            #Increase brightness
            elif((request.action == HAS_enums.Actions.INCREASE.name.lower() and HAS_enums.Attributes.BRIGTHNESS.name.lower())):
                dlg_result = self.handle_request_increase_brightness(request,w_en,VH_Orch)
            #Decrease brightness
            elif((request.action == HAS_enums.Actions.DECREASE.name.lower() and HAS_enums.Attributes.BRIGTHNESS.name.lower())):
                dlg_result = self.handle_request_decrease_brightness(request,w_en,VH_Orch)
            #Binary queary
            elif((request.action == HAS_enums.Actions.BINARY_QUERY.name.lower() and request.state == HAS_enums.States.POWERED.name.lower())):
                dlg_result =self. handle_req_bq(request,w_en,VH_Orch)
            #Information queary - brightness
            elif((request.action == HAS_enums.Actions.INFORMATION_QUERY.name.lower() and HAS_enums.Attributes.BRIGTHNESS.name.lower())):
                dlg_result = self.handle_req_iq_brgth(request,w_en,VH_Orch)
            else:
                dlg_result.set_state(HAS_requestStatus.UNKNOWN_ACTION)

        return dlg_result
    
    def handle_request_turn_onoff(self,request, w_en, VH_Orch : 'VHOrchestator') -> HAS_result:
        entity_id = w_en['entity'].entity_id
        dlg_result = HAS_result(HAS_requestStatus.SUCCESS)
        try:
            VH_Orch.hass_instance.trigger_service(
                'light', 'turn_'+str.lower(request.action), entity_id=f'{entity_id}')
        except Exception as e:
            print(str(e))
            dlg_result.set_state(HAS_requestStatus.FAILURE)

        return dlg_result

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
    def choose_winner(candidates):
        return max(candidates, key=lambda x: x['similarity'])

    @staticmethod
    def build_suggest_entity_name(request: HAS_request):
        description = ''
        location = ''
        if request.description:
            description = '_'.join(list(request.description))
        if request.location:
            location = request.location
        
        if(description):
            description = '_'+description
        # Common pattern: light.<location>_<description>_light
        query = 'light.' + location.lower() + description + '_light'

        return query
