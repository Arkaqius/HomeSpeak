'''
Module to test NER model
'''
import random
from vh_ner import VhNer, VhProcessedText
import nlp.ner.config as cfg

def main():
    '''
    Main function to perform NER model test
    '''
    ner = VhNer(cfg.PATH_TRAINED_MODEL)

    while True:
        user_input = input("Enter an utterance or type 'random' for random test sentence, or 'exit' to stop: ")

        if user_input.lower() == 'exit':
            break
        elif user_input.lower() == 'r':
            with open(cfg.PATH_TEST_SENTENCES, "r", encoding='UTF-8') as file:
                lines = file.readlines()
                user_input = random.choice(lines)
                print("\nSelected random line:", user_input)
        
        result: VhProcessedText = ner.process_text(user_input)

        # Displaying results
        print("Named entities:")
        for entity in result.named_entities:
            print(f"{entity.entity_type}: {entity.entity_default_name} : {entity.entity_text}")

        print("Numerical values:")
        for num_value in result.numerical_values:
            print(f"{num_value.value} {num_value.unit}")


if __name__ == "__main__":
    main()