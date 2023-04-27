from homeassistant_api import Client
import SECRETS
from VH_Request import VH_request 
import VH_Enums
import UtterenceHandler.HMI_Lights as HMI_Lights

class HA_UtHan:
    def __init__(self):
        self.hass_instace= Client(SECRETS.URL, SECRETS.TOKEN)

        self.allEntities = self.hass_instace.get_entities()
        self.HA_entity_group_ligts  = self.allEntities['light']

    def run_request(self, request: VH_request):
        if(VH_Enums.Things.LIGHT.name.lower() == request.thing):
            HMI_Lights.handle_request(request,self)



