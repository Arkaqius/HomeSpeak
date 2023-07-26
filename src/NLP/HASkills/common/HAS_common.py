from __future__ import annotations
from enum import Enum, auto
from fuzzywuzzy import fuzz
from typing import List, Dict, Any
from homeassistant_api import Entity


class HAS_find:
    @staticmethod
    def _filter_by_entity_type(entity: Dict[str, Any], entity_type: str) -> bool:
        """Filter by entity type.

        Args:
            entity (Dict[str, Any]): The entity to check.
            entity_type (str): The entity type to filter by.

        Returns:
            bool: True if the entity matches the specified entity type, False otherwise.
        """
        return entity.get("entity_type") == entity_type

    @staticmethod
    def _filter_by_location(entity: Dict[str, Any], location: str) -> bool:
        """Filter by location.

        Args:
            entity (Dict[str, Any]): The entity to check.
            location (str): The location to filter by.

        Returns:
            bool: True if the entity matches the specified location, False otherwise.
        """
        return entity.get("location") == location

    filters = {
        'entity_type': _filter_by_entity_type.__func__,
        'location': _filter_by_location.__func__,
    }

    @staticmethod
    def find_candidates(query: str, list_of_entities:Dict[str,Entity], **kwargs) -> None:
        """Populate the candidates list with optional filters.

        Args:
            query (str): The query to match.
            **kwargs: Keyword arguments with filters.
        """
        candidates: List[Dict[str, Any]] = []

        for _,entity in list_of_entities.items():
            
            if not all(HAS_find.filters[key](entity, value) for key, value in kwargs.items() if key in HAS_Find.filters):
                continue

            ratio = fuzz.ratio(query, entity.entity_id)
            if ratio > 50:
                candidates.append({"entity": entity, "similarity": ratio})

        return candidates
    
class HAS_requestStatus(Enum):
    UNKNOWN = "unknown"
    SUCCESS = "success"
    FAILURE = "failure"
    NOT_FOUND = "not_found"
    NO_RESPONSE = "no_response"
    UNKNOWN_ENTITY = "entity_not_found"
    UNKNOWN_ACTION = "entity_not_support_action"

class HAS_result:
    def __init__(self, status: HAS_requestStatus, data: dict = None):
        self.status = status
        self.data = data if data is not None else {}

    def is_successful(self) -> bool:
        return self.status == HAS_requestStatus.SUCCESS
    
    def set_state(self, status: HAS_requestStatus) -> None:
        self.status = status

    def set_entitiy_state(self,state):
        self.data['state'] = state

    def __str__(self) -> str:
        return f"Status: {self.status.value}, Data: {self.data}"
    
