from __future__ import annotations

from capacities.client import CapacitiesClient
from capacities.models import (
    Collection,
    LabelOption,
    PropertyDefinition,
    Space,
    Structure,
)


class SpaceAPI:
    def __init__(self, client: CapacitiesClient):
        self._client = client

    def get_spaces(self) -> list[Space]:
        data = self._client._get("/spaces")
        return [
            Space(id=s["id"], title=s.get("title", "Untitled"))
            for s in data.get("spaces", [])
        ]

    def get_space_info(self, space_id: str) -> Space:
        spaces = self.get_spaces()
        title = next((s.title for s in spaces if s.id == space_id), space_id)

        data = self._client._get("/space-info", params={"spaceid": space_id})

        structures = []
        for s in data.get("structures", []):
            props = [
                PropertyDefinition(
                    id=p["id"],
                    name=p.get("name", ""),
                    type=p.get("type", "unknown"),
                    writable=p.get("writable", False),
                    multiple=p.get("multiple", False),
                    allowed_structures=p.get("allowedStructures", []),
                    label_set=[
                        LabelOption(
                            id=l["id"],
                            name=l["name"],
                            color=l["color"],
                        )
                        for l in p.get("labelSet", [])
                    ],
                    raw=p,
                )
                for p in s.get("propertyDefinitions", [])
            ]
            collections = [
                Collection(id=c["id"], title=c["title"])
                for c in s.get("collections", [])
            ]
            structures.append(
                Structure(
                    id=s["id"],
                    title=s.get("title", "Untitled"),
                    plural_name=s.get("pluralName", ""),
                    label_color=s.get("labelColor", "neutral"),
                    properties=props,
                    collections=collections,
                    raw=s,
                )
            )

        return Space(id=space_id, title=title, structures=structures)
