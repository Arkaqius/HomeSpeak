# pylint: disable=C0114
import os
import glob
import json
from NLP.NER.config import PATH_VOCAB


class Vocab:
    """
    A class representing the vocabulary and synonyms for labels and entities.
    It reads data from the vocabulary files and populates dictionaries for label-entity
    relationships and synonyms.
    """

    def __init__(self):
        """Initialize the Vocab class with empty dictionaries for label-entity and synonyms."""
        self.label_entity_dict = {}
        self.synonyms_dict = {}

    def read_data(self):
        """
        Read data from the vocabulary files and populate the label_entity_dict and
        synonyms_dict with the appropriate information.
        """
        for label_dir in glob.glob(os.path.join(PATH_VOCAB, '*')):
            label = os.path.basename(label_dir)
            label = label.lower()
            self.label_entity_dict[label] = []

            # Iterate through each entity file in the current label directory
            for entity_file in glob.glob(os.path.join(label_dir, '*.voc')):
                entity = os.path.splitext(os.path.basename(entity_file))[0]
                entity = entity.lower()
                self.label_entity_dict[label].append(entity)

                # Read synonyms from the entity file
                with open(entity_file, 'r', encoding='UTF-8') as file:
                    synonyms = [line.strip() for line in file.readlines()]
                    self.synonyms_dict[entity] = [string.lower()
                                                  for string in synonyms]

        del self.label_entity_dict['helpers']

    def __str__(self) -> str:
        """
        Returns a string representation of the label_entity_dict in JSON format.

        Returns:
            str: A JSON-formatted string representation of the label_entity_dict.
        """
        return json.dumps(self.label_entity_dict)
