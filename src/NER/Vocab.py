import os
import glob
import json
import config as cfg

class Vocab:

    def __init__(self):
        self.label_entity_dict = {}
        self.synonyms_dict = {}
    
    def readData(self):
        for label_dir in glob.glob(os.path.join(cfg.PATH_VOCAB, '*')):
            label = os.path.basename(label_dir)
            label = label.lower()
            self.label_entity_dict[label] = []

            # Iterate through each entity file in the current label directory
            for entity_file in glob.glob(os.path.join(label_dir, '*.voc')):
                entity = os.path.splitext(os.path.basename(entity_file))[0]
                entity = entity.lower()
                self.label_entity_dict[label].append(entity)

                # Read synonyms from the entity file
                with open(entity_file, 'r') as f:
                    synonyms = [line.strip() for line in f.readlines()]
                    self.synonyms_dict[entity] = [string.lower() for string in synonyms]

        del self.label_entity_dict['helpers']
        
    def __str__(self) -> str:
        return json.dumps(self.label_entity_dict)
        