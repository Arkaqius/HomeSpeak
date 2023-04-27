import config as cfg
import typing as T

from NER.VH_NER import VH_NER
from UtterenceHandler.VH_Request import VH_request
from UtterenceHandler.HA_UtHan import HA_UtHan

def main():
    ner : VH_NER = VH_NER(cfg.PATH_TRAINED_MODEL)
    utterenceHandler : HA_UtHan = HA_UtHan()  # Replace this with the initialization of your Home Assistant module

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

        req = VH_request(user_input, named_entities, numerical_values)
        # Call your Home Assistant module with the extracted named entities
        utterenceHandler.run_request(req)

if __name__ == '__main__':
    main()