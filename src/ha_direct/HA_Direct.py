from homeassistant_api import Client
from ha_direct.SECRETS import *
from VHCommon import VH_Request 
from typing import Type
from ha_direct.HMI.HMI_Common import HMI_ActionBase

class HA_Direct():

    def __init__(self):
        self.hass_instace= Client(URL, TOKEN)
        self.allEntities = self.hass_instace.get_entities()
        self.HA_entity_group_ligts  = self.allEntities['light']

    def run_request(self, request: VH_Request):
        handler: Type[HMI_ActionBase]  = HMI_ActionBase._find_handler(request)
        if(handler is not None):
            handler().handle_utterance(request,self)



