
import VH_NER
import config as cfg
from HA_UtHan import VH_Request
import HA_UtHan

def main():
    ner = VH_NER(cfg.PATH_TRAINED_MODEL)
    utterenceHandler = HA_UtHan()  # Replace this with the initialization of your Home Assistant module

    while True:
        user_input = input("Enter an utterance or type 'quit' to exit: ")

        if user_input.lower() == "quit":
            break

        named_entities, numerical_values = ner.process_text(user_input)
        print("Named entities:")
        for entity, label in named_entities.items():
            print(f"{entity}: {label}")

        print("Named entities:")
        for entity, label in numerical_values.items():
            print(f"{entity}: {label}")

        req = VH_Request(named_entities, numerical_values)
        # Call your Home Assistant module with the extracted named entities
        utterenceHandler.run_request(req)

if __name__ == '__main__':
    main()