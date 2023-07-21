from homeassistant_api import Client
# TODO
from tokenSkills.HA_direct.SECRETS import *
from tokenSkills.common.VH_Request import VH_Request 
from tokenSkills.HA_direct.HMI.HMI_Common import HMI_ActionBase
from typing import Type

class HA_Direct():

    def __init__(self):
        self.hass_instace= Client(URL, TOKEN)
        self.allEntities = self.hass_instace.get_entities()
        self.HA_entity_group_ligts  = self.allEntities['light']
        
    def run_request(self, request: VH_Request):
        handler: Type[HMI_ActionBase]  = HMI_ActionBase._find_handler(request)
        if(handler is not None):
            result = handler().handle_utterance(request,self)
        
        print(result) # TODO Debug



