from __future__ import annotations
import tokenSkills.common.VH_Enums as VH_Enums
from typing import List, Dict, Any
from ...common.VH_Request import VH_Request
from .HMI_Common import *


class HMI_Lights(HMI_ActionBase):
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

    def can_handle(self, request):
        if (VH_Enums.Things.LIGHT.name.lower() == request.thing):
            return True
        else:
            return False

    def handle_utterance(self, request: VH_Request, HAS_inst : 'HA_Direct') -> HAResult:
        dlg_result = HAResult(HARequestStatus.UNKNOWN)
        # Create queary and find matchign candidates
        candidates = HMI_Find.find_candidates(HMI_Lights.build_suggest_entity_name(request),
                                              HAS_inst.HA_entity_group_ligts.entities)
        # Choose one or ask for more specific information
        w_en = HMI_Lights.choose_winner(candidates)
        if w_en is None:
           dlg_result.set_state(HARequestStatus.UNKNOWN_ENTITY)
        else:
            # Determinate which action shall be run
            # Simple ON/OFF
            if (request.action == VH_Enums.Actions.ON.name.lower() or request.action == VH_Enums.Actions.OFF.name.lower()):
                dlg_result = self.handle_request_turn_onoff(request, w_en, HAS_inst)
            #Change brightness to exact value
            elif(request.action == VH_Enums.Actions.ADJUST.name.lower() and request.attribute == VH_Enums.Attributes.BRIGTHNESS.name.lower()):
                dlg_result = self.handle_request_change_brightness(request,w_en,HAS_inst)
            #Increase brightness
            elif((request.action == VH_Enums.Actions.INCREASE.name.lower() and VH_Enums.Attributes.BRIGTHNESS.name.lower())):
                dlg_result = self.handle_request_increase_brightness(request,w_en,HAS_inst)
            #Decrease brightness
            elif((request.action == VH_Enums.Actions.DECREASE.name.lower() and VH_Enums.Attributes.BRIGTHNESS.name.lower())):
                dlg_result = self.handle_request_decrease_brightness(request,w_en,HAS_inst)
            #Binary queary
            elif((request.action == VH_Enums.Actions.BINARY_QUERY.name.lower() and request.state == VH_Enums.States.POWERED.name.lower())):
                dlg_result =self. handle_req_bq(request,w_en,HAS_inst)
            #Information queary - brightness
            elif((request.action == VH_Enums.Actions.INFORMATION_QUERY.name.lower() and VH_Enums.Attributes.BRIGTHNESS.name.lower())):
                dlg_result = self.handle_req_iq_brgth(request,w_en,HAS_inst)
            else:
                dlg_result.set_state(HARequestStatus.UNKNOWN_ACTION)

        return dlg_result

    def handle_req_bq(request, w_en, HAS_inst : 'HA_Direct'):
        dlg_result = HAResult(HARequestStatus.SUCCESS)
        w_en['entity'].get_state()
        dlg_result.set_entitiy_state(w_en['entity'].state.state)
        return dlg_result

    def handle_req_iq_brgth(request, w_en, HAS_inst):
        entity_id = w_en.entity['entity_id']
        state = HAS_inst.HA._get_state(entity_id)
        HAS_inst.speak_dialog('LIGHT_IQ_BRIGHTNESS',
                              {'friendly_name':   entity_id,
                               'brg_level':   (float(state['attributes']['brightness']) * 100/256)
                               })
        return HMI_dlg_rtn.NO_RESPONSE

    def handle_request_turn_onoff(self,request, w_en, HAS_inst : 'HA_Direct') -> HAResult:
        entity_id = w_en['entity'].entity_id
        dlg_result = HAResult(HARequestStatus.SUCCESS)
        try:
            HAS_inst.hass_instace.trigger_service(
                'light', 'turn_'+str.lower(request.action), entity_id=f'{entity_id}')
        except:
            dlg_result.set_state(HARequestStatus.FAILURE)

        return dlg_result

    def handle_request_change_brightness(request, w_en, HAS_inst):
        ''' Handle changing brigtness to exact value'''
        # Check if found light support brightness
        if w_en.entity['attributes']['supported_features'] & self.SUPPORT_BRIGHTNESS:
            entity_id = w_en.entity['entity_id']
            HAS_inst.HA.execute_service('light',
                                        'turn_on',
                                        {'entity_id': f'{entity_id}',
                                         'brightness_pct': f'{request.value * 100}'})
            dialog_rtn = HMI_dlg_rtn.SUCCESS
        else:
            dialog_rtn = HMI_dlg_rtn.UF_BRIGHTNESS

        return dialog_rtn

    def handle_request_increase_brightness(request, w_en, HAS_inst):
        entity_id = w_en.entity['entity_id']
        HAS_inst.HA.execute_service('light',
                                    'turn_on',
                                    {'entity_id': f'{entity_id}',
                                     'brightness_step_pct': f'{self.BRIGHNTESS_STEP}'})
        return HMI_dlg_rtn.SUCCESS

    def handle_request_decrease_brightness(request, w_en, HAS_inst):
        entity_id = w_en.entity['entity_id']
        HAS_inst.HA.execute_service('light',
                                    'turn_on',
                                    {'entity_id': f'{entity_id}',
                                     'brightness_step_pct': f'{self.BRIGHNTESS_STEP * -1}'})
        return HMI_dlg_rtn.SUCCESS

    @staticmethod
    def choose_winner(candidates):
        return max(candidates, key=lambda x: x['similarity'])

    @staticmethod
    def build_suggest_entity_name(request: VH_Request):
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
