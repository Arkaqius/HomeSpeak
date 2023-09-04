# pylint: disable=C0114
import itertools
from ner.vh_ner import VhProcessedText, VhNamedEntity, VhNumericalValue


class NerResult:
    '''
    Class to hold the NER results of text processing.

    Attributes:
        text (str): The text input.
        ner_raw (VhProcessedText): Raw NER processing results containing named entities
                                   and numerical values extracted from the text.
        description (str): A description extracted from the text excluding recognized entities.
        input (str): The original text input.

    Methods:
        _generate_description(text: str, ner_entities: list[VhNamedEntity]) -> str:
            Generate a description by excluding recognized entities and prepositions from the input text.
        
        _extract_recognized_literals(ner_entities: list[VhNamedEntity]) -> list[str]:
            Extract and return the literals/entities recognized from the input text.

        to_single_by_indexes(description: str, indexes: dict[str, int]) -> 'NerResultSingle':
            Construct and return a NerResultSingle instance using specified indexes.

        split_by(description: str, entity_type: str) -> list['NerResultSingle']:
            Split the NER results by a specific entity type and return a list of NerResultSingle instances.
    '''

    PREPOSITIONS = ["in", "on", "at"]
    NER_KEYS = ["thing", "attribute", "location", "state", "action"]

    def __init__(self, text: str, ner_raw: VhProcessedText | None = None, desc : str | None = None) -> None:
        """
        Initialize a NER_Request instance with attributes based on the ner_raw.

        Args:
            text (str): The text input.
            ner_raw (VhProcessedText): A VhProcessedText object containing the named entities
                                       and numerical values extracted from the text.

        """
        if ner_raw: # If None, we are spliting multirequest to single one
            # Set default attributes
            for key in self.NER_KEYS:
                matching_entities = [
                    named_entity.entity_default_name
                    for named_entity in ner_raw.named_entities
                    if named_entity.entity_type == key
                ]
                setattr(self, key, matching_entities)

            # Handle value attributes
            self.values: list[VhNumericalValue] = ner_raw.numerical_values

        if ner_raw and not desc:
            # Generate description based on the input text and NER_Dict
            self.description: str = self._generate_description(
                text, ner_raw.named_entities)
        else:
            self.description: str = desc

        # Store the original input
        self.input: str = text

    def _generate_description(self, text: str, ner_entities: list[VhNamedEntity]) -> str:
        """
        Generate a description from the input text by excluding recognized entities and prepositions.

        Args:
            text (str): The input text.
            ner_entities (List[VhNamedEntity]): A list of named entities extracted from the text.

        Returns:
            str: A description extracted from the text.
        """
        tokens = text.split()
        recognized_literals = self._extract_recognized_literals(ner_entities)
        return " ".join(token for token in tokens if token not in recognized_literals and token not in self.PREPOSITIONS).strip()

    def _extract_recognized_literals(self, ner_entities: list[VhNamedEntity]) -> list[str]:
        """
        Extract recognized literals/entities from the list of named entities.

        Args:
            ner_entities (List[VhNamedEntity]): A list of named entities extracted from the text.

        Returns:
            List[str]: A list of recognized literals/entities.
        """
        literals = [entity.entity_text.split() for entity in ner_entities]
        return list(itertools.chain(*literals))

    def to_single_by_indexes(self, description, indexes: dict[str, int]) -> 'NerResultSingle':
        """Construct a NerResultSingle instance using the specified indexes."""
        extracted_entities = {}

        for key, index in indexes.items():
            entities = getattr(self, key, [])
            if 0 <= index < len(entities):
                extracted_entities[key] = entities[index]

        return NerResultSingle(self.input,description, extracted_entities)
    
    def to_single_first_occurrences(self) -> 'NerResultSingle':
        """
        Construct a NerResultSingle instance using the first occurrence of each entity.
            
        Returns:
            NerResultSingle: A single instance containing the first occurrence of each recognized entity.
        """
        extracted_entities = {}

        for key in self.NER_KEYS:
            entities = getattr(self, key, [])
            if entities:  # Checks if the entity list is not empty
                extracted_entities[key] = entities[0]

        return NerResultSingle(self.input, self.description, extracted_entities)

    def split_by(self, description: str,  entity_type: str) -> list['NerResultSingle']:
        """Split the NerResult by a specific entity type."""
        entities = getattr(self, entity_type, [])
        split_results = []

        for index, _ in enumerate(entities):
            split_results.append(
                self.to_single_by_indexes(description, {entity_type: index},))

        return split_results


class NerResultSingle(NerResult):
    '''
    A derived class from NerResult to represent NER results for single-entity requests.

    Attributes:
        Inherits attributes from NerResult.

    Methods:
        to_single() -> 'NerResultSingle':
            Return a single instance of itself.
    '''
    def __init__(self, text: str, description : str,  entities: dict[str, str | list[str]]) -> None:
        """
        Initialize a NerResultSingle instance.

        Args:
            text (str): The original text input.
            description (str): A description extracted from the text.
            entities (dict[str, str | list[str]]): A dictionary of named entities extracted from the text.

        Attributes:
            Inherits attributes and methods from NerResult.
        """
        super().__init__(text, desc = description)  # Passing None as we will copy from parent
        for key, value in entities.items():
            setattr(self, key, value)  # Ensure the value is in a list format

    def to_single(self) -> 'NerResultSingle':
        """Returns a single instance of itself."""
        return self