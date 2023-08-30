# pylint: disable=C0114
from typing import List, Dict, Any, Callable
from fuzzywuzzy import fuzz
from homeassistant_api import Entity


CANDIDATES_ADD_THRESHOLD: int = 50
"""Threshold above which entities are considered as valid candidates."""


class HasFind:
    """Helper class to find entities based on filters and similarity to a given query."""
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

    FilterFunc = Callable[[Dict[str, Any], str], bool]
    filters: Dict[str, FilterFunc] = {
        "entity_type": _filter_by_entity_type.__func__,
        "location": _filter_by_location.__func__,
    }
    """Dictionary of available filters to apply when searching for entities."""

    @staticmethod
    def find_candidates(
        query: str, list_of_entities: Dict[str, Entity], **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search for entities that match the given query and optional filters.

        This method identifies entities based on their similarity to a provided query string.
        The similarity is computed using the fuzz.ratio method. Entities with a similarity ratio 
        above the CANDIDATES_ADD_THRESHOLD are considered as candidates. Additional filters can 
        be applied using keyword arguments.

        Args:
            query (str): The query string to match entities against.
            list_of_entities (Dict[str, Any]): Dictionary of entities to search from.
            **kwargs: Filters to apply when searching for entities. Supported filters include 
                      'entity_type' and 'location'.

        Returns:
            List[Dict[str, Any]]: List of dictionaries representing the matching entities and their 
                                  similarity to the query.
        """
        candidates: List[Dict[str, Any]] = []

        for _, entity in list_of_entities.items():
            if not all(
                HasFind.filters[key](entity, value)
                for key, value in kwargs.items()
                if key in HasFind.filters
            ):
                continue

            ratio = fuzz.ratio(query, entity.entity_id)
            if ratio > CANDIDATES_ADD_THRESHOLD:
                candidates.append({"entity": entity, "similarity": ratio})

        return candidates
