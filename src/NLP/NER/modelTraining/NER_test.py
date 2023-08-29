from vh_ner import VhNer
import NLP.NER.config as cfg
import random


def main():
    ner = VhNer(cfg.PATH_TRAINED_MODEL)

    with open(cfg.PATH_TEST_SENTENCES, "r") as f:
        lines = f.readlines()
        for _ in range(1, 50):
            random_line = random.choice(lines)
            print("\n" + random_line)

            named_entities, numerical_values = ner.process_text(random_line)
            print("Named entities:")
            for entity, label in named_entities.items():
                print(f"{entity}: {label}")

            print("Numerical values:")
            print(numerical_values)


if __name__ == "__main__":
    main()
