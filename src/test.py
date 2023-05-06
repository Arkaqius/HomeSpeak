import config as cfg
import typing as T

from NER.VH_NER import VH_NER
from VHCommon.VH_Request import VH_Request
from ha_direct.HA_Direct import HA_Direct

def main():
    ner : VH_NER = VH_NER(cfg.PATH_TRAINED_MODEL)
    hass_instace : HA_Direct = HA_Direct()
    
    while True:
        user_input : str = input("Enter an utterance or type 'quit' to exit: ")

        if user_input.lower() == "quit":
            break
        
        # Check if the user input matches any predefined inputs and set user_input to the corresponding sentence
        predefined_inputs = {
            "1": "turn on office light",
            "2": "turn off kitchen light",
            "3": "set warm water to eco"
        }
        if user_input.strip() in predefined_inputs:
            user_input = predefined_inputs[user_input.strip()]

        named_entities , numerical_values = ner.process_text(user_input)
        print("Named entities:")
        for entity, label in named_entities.items():
            print(f"{entity}: {label}")

        print("Values:")
        if numerical_values:
            for val in numerical_values:
                print(f"{val}")

        req = VH_Request(user_input, named_entities, numerical_values)
        # Call your Home Assistant module with the extracted named entities
        
        hass_instace.run_request(req)

if __name__ == '__main__':
    main()