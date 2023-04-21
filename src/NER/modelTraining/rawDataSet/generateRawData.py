import random
import json
import os
import glob
from Vocab import Vocab
import typing
import config as cfg


class TrainingDataGenerator:
    @staticmethod
    def find_substring(substring: str, string: str) -> list:
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

    def __init__(self, predefined_entities: dict, synonyms: dict, helpDescriptor: dict, helpswitchableThing: dict) -> None:
        self.helper = {}

        self.predefined_entities = predefined_entities
        self.synonyms = synonyms
        self.helper['descriptor'] = helpDescriptor
        self.helper['switchableThing'] = helpswitchableThing

    def getRandomEntities(self, label: str) -> str:
        entityName = random.choice(self.predefined_entities[label])
        return self.getRandomSynonym(entityName)

    def getRandomSynonym(self, enititName: str) -> str:
        retVal = ''
        synonym = self.synonyms.get(enititName, enititName)
        if type(synonym) is list:
            retVal = random.choice(synonym)
        else:
            retVal = synonym
        return retVal

    def getAllSynonyms(self, enititName: str) -> str:
        retVal = []
        for element in enititName:
            retVal.append(self.synonyms[element])

        return retVal

    def getRandomHelper(self, helperName: str) -> str:
        return self.getRandomSynonym(random.choice(self.helper[helperName]))
    
    def get_random_value_string(self):

        value_strings = [
            "50 percent", "half", "full", "minimum", "maximum", "economy", "comfort", "bath"
        ]
        
        # Add random percent values
        value_strings.extend([f"{random.randint(1, 100)} percent" for _ in range(10)])
        
        # Add temperature values in Celsius
        value_strings.extend([f"{random.uniform(15, 30):.1f} Celsius degree" for _ in range(10)])

        return random.choice(value_strings)

    def generate_sentence(self, sentence_type=0) -> typing.Tuple[str, dict]:
        """
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
        entitiesList = {}

        if sentence_type == 1:
            switchableThing = self.getRandomHelper('switchableThing')
            action = random.choice([self.getRandomSynonym(
                'on'), self.getRandomSynonym('off'), self.getRandomSynonym('toggle')])
            location = self.getRandomEntities('location')

            entitiesList['actions'], entitiesList['things'], entitiesList['location'] = action, switchableThing, location
            sentence = f"{action} the {switchableThing} in {location}"

        elif sentence_type == 2:
            switchableThing = self.getRandomHelper('switchableThing')
            action = random.choice([self.getRandomSynonym(
                'on'), self.getRandomSynonym('off'), self.getRandomSynonym('toggle')])
            location = self.getRandomEntities('location')
            desc = self.getRandomHelper('descriptor')

            entitiesList['actions'], entitiesList['things'], entitiesList['location'] = action, switchableThing, location
            sentence = f"{action} the {desc} {switchableThing} in {location}"

        elif sentence_type == 3:
            thing = self.getRandomEntities('things')
            adjust = self.getRandomSynonym('adjust')
            location = self.getRandomEntities('location')
            attribute = self.getRandomEntities('attributes')
            desc = self.getRandomHelper('descriptor')

            entitiesList['actions'], entitiesList['attributes'], entitiesList[
                'things'], entitiesList['location'] = adjust, attribute, thing, location
            sentence = f"{adjust} {attribute} of {desc} {thing} in {location}"

        elif sentence_type == 4:
            thing = self.getRandomEntities('things')
            adjust = self.getRandomSynonym('adjust')
            attribute = self.getRandomEntities('attributes')
            desc = self.getRandomHelper('descriptor')

            entitiesList['actions'], entitiesList['attributes'], entitiesList['things'] = adjust, attribute, thing
            sentence = f"{adjust} {attribute} of {desc} {thing}"

        elif sentence_type == 5:
            action = random.choice([self.getRandomSynonym(
                'increase'), self.getRandomSynonym('decrease')])
            thing = self.getRandomEntities('things')
            location = self.getRandomEntities('location')
            attribute = self.getRandomEntities('attributes')
            desc = self.getRandomHelper('descriptor')

            entitiesList['actions'], entitiesList['attributes'], entitiesList[
                'things'], entitiesList['location'] = action, attribute, thing, location
            sentence = f"{action} {attribute} of {desc} {thing} in {location}"

        elif sentence_type == 6:
            action = random.choice([self.getRandomSynonym(
                'increase'), self.getRandomSynonym('decrease')])
            thing = self.getRandomEntities('things')
            attribute = self.getRandomEntities('attributes')
            desc = self.getRandomHelper('descriptor')

            entitiesList['actions'], entitiesList['attributes'], entitiesList['things'] = action, attribute, thing
            sentence = f"{action} {attribute} of {desc} {thing}"

        elif sentence_type == 7:
            action = self.getRandomSynonym('binary_query')
            thing = self.getRandomEntities('things')
            state = self.getRandomEntities('states')
            location = self.getRandomEntities('location')

            entitiesList['actions'], entitiesList['things'], entitiesList['location'], entitiesList['state'] = action, thing, location, state
            sentence = f"{action} {thing} in {location} {state}"

        elif sentence_type == 8:
            action = self.getRandomSynonym('binary_query')
            thing = self.getRandomEntities('things')
            state = self.getRandomEntities('states')
            location = self.getRandomEntities('location')
            desc = self.getRandomHelper('descriptor')

            entitiesList['actions'], entitiesList['things'], entitiesList['location'], entitiesList['state'] = action, thing, location, state
            sentence = f"{action} {desc} {thing} in {location} {state}"

        elif sentence_type == 9:
            action = self.getRandomSynonym('information_query')
            attribute = self.getRandomEntities('attributes')
            desc = self.getRandomHelper('descriptor')
            thing = self.getRandomEntities('things')
            location = self.getRandomEntities('location')

            entitiesList['actions'], entitiesList['attributes'], entitiesList['things'], entitiesList['location'] = action, attribute, thing, location,
            sentence = f"{action} {attribute} of {desc} {thing} in {location}"

        elif sentence_type == 10:
            action = self.getRandomSynonym('set')
            attribute = self.getRandomEntities('attributes')
            desc = self.getRandomHelper('descriptor')
            thing = self.getRandomEntities('things')
            location = self.getRandomEntities('location')
            value = self.get_random_value_string()

            entitiesList['actions'], entitiesList['attributes'], entitiesList['things'], entitiesList['location'] = action, attribute, thing, location,
            sentence = f"{action} {attribute} of {desc} {thing} in {location} to {value}"

        # Switch the switch case
        elif sentence_type == 101:
            thing = 'switch'
            action = 'switch'
            location = self.getRandomEntities('location')

            entitiesList['actions'], entitiesList['things'], entitiesList['location'] = action, thing, location
            sentence = f"{action} the {thing} in {location}"

        sentence = sentence.lower()
        entities = []
        for key, value in entitiesList.items():
            slice = TrainingDataGenerator.find_substring(value, sentence)
            if (len(slice) > 1):
                print(sentence)
            entities.extend(slice)

        entity_data = []
        for entity in entities:
            start, end = entity
            entity_text = sentence[start:end]
            entity_label = [
                key for key, value in entitiesList.items() if entity_text == value][0]
            entity_name = [
                key for key, value in self.synonyms.items() if entity_text in value][0]
            entity_data.append((start, end, f'{entity_label}_#{entity_name}'))

        return sentence, {"entities": entity_data}

    def generate_training_data(self, n=cfg.SIZE_OF_TRAIN_DATA, sentence_type=0) -> typing.Tuple[list, list]:
        training_data = []
        sentences_data = []
        for _ in range(n):
            sentence, entities = self.generate_sentence(
                sentence_type=sentence_type)
            training_data.append((sentence, entities))
            sentences_data.append(sentence)
        return sentences_data, training_data


def main() -> None:
    vocab = Vocab()
    vocab.readData()
    print(vocab)

    generator = TrainingDataGenerator(vocab.label_entity_dict, dict(sorted(vocab.synonyms_dict.items(
    ))), vocab.synonyms_dict['descriptor'], vocab.synonyms_dict['switchable_thing'])

    sentences_data, generated_data = generator.generate_training_data()

    geneareted_file_path = cfg.PATH_TRAIN_DATA
    sentances_file_path = cfg.PATH_TEST_SENTENCES

    with open(geneareted_file_path, "w", encoding="utf-8") as file:
        json.dump(generated_data, file, ensure_ascii=False, indent=2)

    with open(sentances_file_path, "w", encoding="utf-8") as file:
        file.writelines(line + "\n" for line in sentences_data)


if __name__ == "__main__":
    main()
