'''
Module conatins main function and is used to generate NER model training data.
'''
import random
import json
from vocab import Vocab
import nlp.ner.config as cfg


class TrainingDataGenerator:
    """
    A utility class for generating training data.
    """
    @staticmethod
    def find_substring(substring: str, string: str) -> list:
        """
        Find all occurrences of a substring in a given string, considering word boundaries.

        Args:
            substring (str): The substring to search for.
            string (str): The string to search within.

        Returns:
            list: A list of tuples, each containing the start and end indices of the substring's occurrences.
        """
        indices = [i for i in range(len(string))
                   if string.startswith(substring, i)]
        whole_word_indices = []

        for index in indices:
            # Check if the character before the substring is a word boundary
            if index == 0 or string[index - 1].isspace():
                end_index = index + len(substring)

                # Check if the character after the substring is a word boundary
                if end_index == len(string) or string[end_index].isspace():
                    whole_word_indices.append((index, end_index))

        return whole_word_indices

    def __init__(
        self,
        predefined_entities: dict[str, list[str]],
        synonyms: dict[str, str | list[str]],
        help_descriptor: dict[str, str],
        help_switchable_thing: dict[str, str],
    ) -> None:
        """
        Initialize the TrainingDataGenerator with predefined entities, synonyms, and helper dictionaries.

        Args:
            predefined_entities (dict): A dictionary containing entity labels and their corresponding entities.
            synonyms (dict): A dictionary containing synonyms for the entities.
            helpDescriptor (dict): A dictionary containing descriptor helpers.
            helpswitchableThing (dict): A dictionary containing switchable thing helpers.
        """
        self.helper = {}

        self.predefined_entities = predefined_entities
        self.synonyms = synonyms
        self.helper["descriptor"] = help_descriptor
        self.helper["switchableThing"] = help_switchable_thing

    def get_random_entities(self, label: str) -> str:
        """
        Get a random entity from the predefined entities list based on the given label and find a random synonym for it.

        Args:
            label (str): The label for the entity.

        Returns:
            str: A random synonym for the selected entity.
        """
        entity_name = random.choice(self.predefined_entities[label])
        return self.get_random_synonym(entity_name)

    def get_random_synonym(self, entity_name: str) -> str:
        """
        Get a random synonym for the given entity name.

        Args:
            enititName (str): The name of the entity.

        Returns:
            str: A random synonym for the given entity name.
        """
        ret_val = ""
        synonym = self.synonyms.get(entity_name, entity_name)
        if isinstance(synonym, list):
            ret_val = random.choice(synonym)
        else:
            ret_val = synonym
        return ret_val

    def get_all_synonyms(self, enitity_name: str) -> list[str]:
        """
        Get all synonyms for the given entity names.

        Args:
            enititName (str): The names of the entities.

        Returns:
            str: A list containing all synonyms for the given entity names.
        """
        ret_val = []
        for element in enitity_name:
            ret_val.append(self.synonyms[element])

        return ret_val

    def get_random_helper(self, helper_name: str) -> str:
        """
        Get a random helper for the given helper name and find a random synonym for it.

        Args:
            helperName (str): The name of the helper.

        Returns:
            str: A random synonym for the selected helper.
        """
        return self.get_random_synonym(random.choice(self.helper[helper_name]))

    def get_random_value_string(self):
        """
        Get a random value string for attributes.

        Returns:
            str: A random value string.
        """
        value_strings = [
            "50 percent",
            "half",
            "full",
            "minimum",
            "maximum",
            "economy",
            "comfort",
            "bath",
        ]

        # Add random percent values
        value_strings.extend(
            [f"{random.randint(1, 100)} percent" for _ in range(10)])

        # Add temperature values in Celsius
        value_strings.extend(
            [f"{random.uniform(15, 30):.1f} Celsius degree" for _ in range(10)]
        )

        return random.choice(value_strings)

    def generate_sentence_type_1(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 1 and its corresponding entities list.

        Type 1 Sentence: "<action> the <switchable_thing> in <location>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        switchable_thing = self.get_random_helper("switchableThing")
        action = random.choice(
            [
                self.get_random_synonym("on"),
                self.get_random_synonym("off"),
                self.get_random_synonym("toggle"),
            ]
        )
        location = self.get_random_entities("location")

        entities_list = {
            "actions": action,
            "things": switchable_thing,
            "location": location,
        }
        sentence = f"{action} the {switchable_thing} in {location}"
        return sentence, entities_list

    def generate_sentence_type_2(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 2 and its corresponding entities list.

        Type 2 Sentence: "<action> the <descriptor> <switchable_thing> in <location>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        switchable_thing = self.get_random_helper("switchableThing")
        action = random.choice(
            [
                self.get_random_synonym("on"),
                self.get_random_synonym("off"),
                self.get_random_synonym("toggle"),
            ]
        )
        location = self.get_random_entities("location")
        desc = self.get_random_helper("descriptor")

        entities_list = {
            "actions": action,
            "things": switchable_thing,
            "location": location,
        }
        sentence = f"{action} the {desc} {switchable_thing} in {location}"
        return sentence, entities_list

    def generate_sentence_type_3(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 3 and its corresponding entities list.

        Type 3 Sentence: "<adjust> <attribute> of <descriptor> <thing> in <location>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        thing = self.get_random_entities("things")
        adjust = self.get_random_synonym("adjust")
        location = self.get_random_entities("location")
        attribute = self.get_random_entities("attributes")
        desc = self.get_random_helper("descriptor")

        entities_list = {
            "actions": adjust,
            "attributes": attribute,
            "things": thing,
            "location": location,
        }
        sentence = f"{adjust} {attribute} of {desc} {thing} in {location}"
        return sentence, entities_list

    def generate_sentence_type_4(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 4 and its corresponding entities list.

        Type 4 Sentence: "<adjust> <attribute> of <descriptor> <thing>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        thing = self.get_random_entities("things")
        adjust = self.get_random_synonym("adjust")
        attribute = self.get_random_entities("attributes")
        desc = self.get_random_helper("descriptor")

        entities_list = {"actions": adjust,
                         "attributes": attribute, "things": thing}
        sentence = f"{adjust} {attribute} of {desc} {thing}"
        return sentence, entities_list

    def generate_sentence_type_5(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 5 and its corresponding entities list.

        Type 5 Sentence: "<action> <attribute> of <descriptor> <thing> in <location>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        action = random.choice(
            [self.get_random_synonym("increase"),
             self.get_random_synonym("decrease")]
        )
        thing = self.get_random_entities("things")
        location = self.get_random_entities("location")
        attribute = self.get_random_entities("attributes")
        desc = self.get_random_helper("descriptor")

        entities_list = {
            "actions": action,
            "attributes": attribute,
            "things": thing,
            "location": location,
        }
        sentence = f"{action} {attribute} of {desc} {thing} in {location}"
        return sentence, entities_list

    def generate_sentence_type_6(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 6 and its corresponding entities list.

        Type 6 Sentence: "<action> <attribute> of <descriptor> <thing>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        action = random.choice(
            [self.get_random_synonym("increase"),
             self.get_random_synonym("decrease")]
        )
        thing = self.get_random_entities("things")
        attribute = self.get_random_entities("attributes")
        desc = self.get_random_helper("descriptor")

        entities_list = {"actions": action,
                         "attributes": attribute, "things": thing}
        sentence = f"{action} {attribute} of {desc} {thing}"
        return sentence, entities_list

    def generate_sentence_type_7(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 7 and its corresponding entities list.

        Type 7 Sentence: "<binary_query> <thing> in <location> <state>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        action = self.get_random_synonym("binary_query")
        thing = self.get_random_entities("things")
        state = self.get_random_entities("states")
        location = self.get_random_entities("location")

        entities_list = {
            "actions": action,
            "things": thing,
            "location": location,
            "state": state,
        }
        sentence = f"{action} {thing} in {location} {state}"
        return sentence, entities_list

    def generate_sentence_type_8(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 8 and its corresponding entities list.

        Type 8 Sentence: "<binary_query> <descriptor> <thing> in <location> <state>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        action = self.get_random_synonym("binary_query")
        thing = self.get_random_entities("things")
        state = self.get_random_entities("states")
        location = self.get_random_entities("location")
        desc = self.get_random_helper("descriptor")

        entities_list = {
            "actions": action,
            "things": thing,
            "location": location,
            "state": state,
        }
        sentence = f"{action} {desc} {thing} in {location} {state}"
        return sentence, entities_list

    def generate_sentence_type_9(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 9 and its corresponding entities list.

        Type 9 Sentence: "<information_query> <attribute> of <descriptor> <thing> in <location>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        action = self.get_random_synonym("information_query")
        attribute = self.get_random_entities("attributes")
        desc = self.get_random_helper("descriptor")
        thing = self.get_random_entities("things")
        location = self.get_random_entities("location")

        entities_list = {
            "actions": action,
            "attributes": attribute,
            "things": thing,
            "location": location,
        }
        sentence = f"{action} {attribute} of {desc} {thing} in {location}"
        return sentence, entities_list

    def generate_sentence_type_10(self) -> tuple[str, dict]:
        """
        Generate a sentence of type 10 and its corresponding entities list.

        Type 10 Sentence: "<set> <attribute> of <descriptor> <thing> in <location> to <value>"

        Returns:
            tuple: A tuple containing the generated sentence and a dictionary of entities.
        """
        action = self.get_random_synonym("set")
        attribute = self.get_random_entities("attributes")
        descriptor = self.get_random_helper("descriptor")
        thing = self.get_random_entities("things")
        location = self.get_random_entities("location")
        value = self.get_random_value_string()

        entities_list = {
            "actions": action,
            "attributes": attribute,
            "things": thing,
            "location": location,
        }
        sentence = (
            f"{action} {attribute} of {descriptor} {thing} in {location} to {value}"
        )
        return sentence, entities_list

    def generate_sentence(
        self, sentence_type: int = 0
    ) -> tuple[str, dict[str, list[tuple[int, int, str]]]]:
        """
        Generate a sentence and its entity data for the given sentence type.

        Args:
            sentence_type (int, optional): The sentence type to generate. Default is 0 (random).

        Returns:
            tuple[str, dict]: A tuple containing the generated sentence and its entity data.

        Implemented cases:    
        1. ON/OFF/TOGGLE the {switchableThing} in {location}
        2. ON/OFF/TOGGLE the {descriptor} {switchableThing} in {location}

        3. ADJUST {attribute} of {descriptor} {thing} in {location}
        4. ADJUST {attribute} of {descriptor} {thing}

        5. Decrease/Increase {attribute} of {descriptor} {thing} in {location}
        6. Decrease/Increase {attribute} of {descriptor} {thing}

        7. IS {thing} in {location} {state} 
        8. IS {desc} {thing} in {location} {state} 

        9. What is {attribute} of {desc} {thing} in {location}

        10. SET {atribute} of {thing} in {location} to {value}
        """

        if sentence_type == 0:
            sentence_type = random.randint(1, 10)
        entities_list = {}

        sentence_type_mapping = {
            1: self.generate_sentence_type_1,
            2: self.generate_sentence_type_2,
            3: self.generate_sentence_type_3,
            4: self.generate_sentence_type_4,
            5: self.generate_sentence_type_5,
            6: self.generate_sentence_type_6,
            7: self.generate_sentence_type_7,
            8: self.generate_sentence_type_8,
            9: self.generate_sentence_type_9,
            10: self.generate_sentence_type_10,
        }

        sentence, entities_list = sentence_type_mapping[sentence_type]()
        sentence = sentence.lower()

        entities = []
        for _, value in entities_list.items():
            slice_of_entity = TrainingDataGenerator.find_substring(
                value, sentence)
            if len(slice_of_entity) > 1:
                print(sentence)
            entities.extend(slice_of_entity)

        entity_data = []
        for entity in entities:
            start, end = entity
            entity_text = sentence[start:end]
            entity_label = [
                key for key, value in entities_list.items() if entity_text == value
            ][0]
            entity_name = [
                key for key, value in self.synonyms.items() if entity_text in value
            ][0]
            entity_data.append((start, end, f"{entity_label}_#{entity_name}"))

        return sentence, {"entities": entity_data}

    def generate_training_data(
        self, nbr: int = cfg.SIZE_OF_TRAIN_DATA, sentence_type: int = 0
    ) -> tuple[list[str], list[tuple[str, dict[str, list[tuple[int, int, str]]]]]]:
        """
        Generate a specified number of training data samples with sentences and their corresponding entity data.

        Args:
            n (int, optional): The number of training samples to generate. Default is the value of cfg.SIZE_OF_TRAIN_DATA.
            sentence_type (int, optional): The sentence type to generate. Default is 0 (random).

        Returns:
            tuple[list, list]: A tuple containing lists of generated sentences and training data.
        """
        training_data = []
        sentences_data = []
        for _ in range(nbr):
            sentence, entities = self.generate_sentence(
                sentence_type=sentence_type)
            training_data.append((sentence, entities))
            sentences_data.append(sentence)
        return sentences_data, training_data


def main() -> None:
    """
    Main function to generate training data and test sentences using the TrainingDataGenerator.
    Save the generated data and sentences to their respective files.
    """
    try:
        vocab = Vocab()
        vocab.read_data()
        print(vocab)

        generator = TrainingDataGenerator(
            vocab.label_entity_dict,
            dict(sorted(vocab.synonyms_dict.items())),
            vocab.synonyms_dict["descriptor"],
            vocab.synonyms_dict["switchable_thing"],
        )

        sentences_data, generated_data = generator.generate_training_data()

        geneareted_file_path = cfg.PATH_TRAIN_DATA
        sentances_file_path = cfg.PATH_TEST_SENTENCES

        try:
            with open(geneareted_file_path, "w", encoding="utf-8") as file:
                json.dump(generated_data, file, ensure_ascii=False, indent=2)
        except IOError as exception:
            print(
                f"An error occurred while writing to {geneareted_file_path}: {exception}")

        try:
            with open(sentances_file_path, "w", encoding="utf-8") as file:
                file.writelines(line + "\n" for line in sentences_data)
        except IOError as exception:
            print(
                f"An error occurred while writing to {sentances_file_path}: {exception}")

    except Exception as exception:
        print(f"An error occurred during the execution: {exception}")


if __name__ == "__main__":
    main()
