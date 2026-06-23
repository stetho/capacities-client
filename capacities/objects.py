from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capacities.client import CapacitiesClient


@dataclass
class CapacitiesObject:
    id: str
    title: str
    structure_id: str
    properties: dict[str, Any] = field(default_factory=dict)
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


class ObjectsAPI:
    def __init__(self, client: CapacitiesClient):
        self._client = client

    def search(
        self,
        space_id: str,
        query: str,
        structure_ids: list[str] | None = None,
        limit: int = 20,
    ) -> list[CapacitiesObject]:
        body: dict[str, Any] = {
            "spaceId": space_id,
            "searchTerm": query,
            "limit": limit,
        }
        if structure_ids:
            body["filters"] = {"structureIds": structure_ids}

        data = self._client._post("/search", body=body)
        return [self._parse_object(item) for item in data.get("results", [])]

    def get_by_structure(
        self,
        space_id: str,
        structure_id: str,
        limit: int = 100,
    ) -> list[CapacitiesObject]:
        body: dict[str, Any] = {
            "spaceId": space_id,
            "filters": {"structureIds": [structure_id]},
            "limit": limit,
        }
        data = self._client._post("/search", body=body)
        return [self._parse_object(item) for item in data.get("results", [])]

    def _parse_object(self, item: dict[str, Any]) -> CapacitiesObject:
        return CapacitiesObject(
            id=item.get("id", ""),
            title=item.get("title", "Untitled"),
            structure_id=item.get("structureId", ""),
            properties=item.get("properties", {}),
            raw=item,
        )
