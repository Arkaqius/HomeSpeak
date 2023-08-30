'''
Module to test NER model
'''
import random
from vh_ner import VhNer, VhProcessedText
import NLP.NER.config as cfg


def main():
    '''
    Main function to perform NER model test
    '''
    ner = VhNer(cfg.PATH_TRAINED_MODEL)

    with open(cfg.PATH_TEST_SENTENCES, "r", encoding='UTF-8') as file:
        lines = file.readlines()
        for _ in range(1, 50):
            random_line = random.choice(lines)
            print("\n" + random_line)

            result:  VhProcessedText = ner.process_text(random_line)
            print("Named entities:")
            for entity in result.named_entities:
                print(
                    f"{entity.entity_type}: {entity.entity_default_name} : {entity.entity_text}")

            print("Numerical values:")
            for num_value in result.numerical_values:
                print(f"{num_value.value} {num_value.unit}")


if __name__ == "__main__":
    main()
