import random
import json
import os
import glob
from Vocab import Vocab
import typing

class TrainingDataGenerator:

    @staticmethod
    def find_substring(substring, string):
        indices = [i for i in range(len(string)) if string.startswith(substring, i)]
        whole_word_indices = []

        for index in indices:
            # Check if the character before the substring is a word boundary
            if index == 0 or string[index - 1].isspace():
                end_index = index + len(substring)
                
                # Check if the character after the substring is a word boundary
                if end_index == len(string) or string[end_index].isspace():
                    whole_word_indices.append((index, end_index))

        return whole_word_indices

    def __init__(self,predefined_entities, synonyms, helpDescriptor,helpswitchableThing):
        self.helper = {}

        self.predefined_entities = predefined_entities
        self.synonyms = synonyms
        self.helper['descriptor'] = helpDescriptor
        self.helper['switchableThing'] = helpswitchableThing

    def getRandomEntities(self, label : str):
        entityName = random.choice(self.predefined_entities[label])
        return self.getRandomSynonym(entityName)


    def getRandomSynonym(self,enititName : str):
        retVal = ''

        synonym = self.synonyms.get(enititName,enititName)
        if type(synonym) is list:
            retVal = random.choice(synonym)
        else:
            retVal = synonym
        return retVal


    def getAllSynonyms(self,enititName : str):
        retVal = []

        for element in enititName:
            retVal.append(self.synonyms[element])

        return retVal


    def getRandomHelper(self,helperName : str):
        return self.getRandomSynonym(random.choice(self.helper[helperName]))
    

    def generate_sentence(self):

        """
        1. ON the {switchableThing} in {location}
        2. OFF the {switchableThing} in {location}
        3. ON the {descriptor} {switchableThing} in {location}
        4. OFF the {descriptor} {switchableThing} in {location}
        """

        sentence_type = random.randint(1, 4)
        entitiesList = []

        if sentence_type == 1:
            switchableThing = self.getRandomHelper('switchableThing')
            action = self.getRandomSynonym('on')
            location = self.getRandomEntities('location')

            entitiesList.extend([switchableThing,action,location])
            sentence = f"{action} the {switchableThing} in {location}"
        elif sentence_type == 2:
            switchableThing = self.getRandomHelper('switchableThing')
            action = self.getRandomSynonym('off')
            location = self.getRandomEntities('location')

            entitiesList.extend([switchableThing,action,location])
            sentence = f"{action} the {switchableThing} in {location}"
        elif sentence_type == 3:    
            switchableThing = self.getRandomHelper('switchableThing')
            action = self.getRandomSynonym('on')
            location = self.getRandomEntities('location')
            desc = self.getRandomHelper('descriptor')

            entitiesList.extend([switchableThing,action,location])
            sentence = f"{action} the {desc} {switchableThing} in {location}"     
        elif sentence_type == 4:    
            switchableThing = self.getRandomHelper('switchableThing')
            action = self.getRandomSynonym('off')
            location = self.getRandomEntities('location')
            desc = self.getRandomHelper('descriptor')

            entitiesList.extend([switchableThing,action,location])
            sentence = f"{action} the {desc} {switchableThing} in {location}"

        sentence = sentence.lower()
        entities = []
        for ent in entitiesList:
            entities.extend(TrainingDataGenerator.find_substring(ent, sentence))

        entity_data = []
        for entity in entities:
            start, end = entity
            entity_text = sentence[start:end]
            entity_label = [key for key, value in self.predefined_entities.items() if entity_text in sum(self.getAllSynonyms(value),[]) ][0]
            entity_name = [key for key, value in self.synonyms.items() if entity_text in value][0]
            entity_data.append((start, end, f'{entity_label}_#{entity_name}'))

        return sentence, {"entities": entity_data}


    def generate_training_data(self,n=250):
        training_data = []
        sentences_data = []
        for _ in range(n):
            sentence, entities = self.generate_sentence()
            training_data.append((sentence, entities))
            sentences_data.append(sentence)
        return sentences_data,training_data

vocab = Vocab()
vocab.readData()
print(vocab)

generator = TrainingDataGenerator(vocab.label_entity_dict,dict(sorted(vocab.synonyms_dict.items())),vocab.synonyms_dict['descriptor'],vocab.synonyms_dict['switchable_thing'])

sentences_data, generated_data = generator.generate_training_data()
geneareted_file_path = "./src/NER/modelTraining/rawDataSet/spacy_training_data_generated.json"
sentances_file_path = "./src/NER/modelTraining/rawDataSet/sentances.txt"

with open(geneareted_file_path, "w", encoding="utf-8") as file:   
    json.dump(generated_data, file, ensure_ascii=False, indent=2)

with open(sentances_file_path, "w", encoding="utf-8") as file:   
    file.writelines(line + "\n" for line in sentences_data)


