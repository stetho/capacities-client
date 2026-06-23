from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LabelOption:
    id: str
    name: str
    color: str


@dataclass
class PropertyDefinition:
    id: str
    name: str
    type: str
    writable: bool
    multiple: bool = False
    allowed_structures: list[str] = field(default_factory=list)
    label_set: list[LabelOption] = field(default_factory=list)
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


@dataclass
class Collection:
    id: str
    title: str


@dataclass
class Structure:
    id: str
    title: str
    plural_name: str
    label_color: str
    properties: list[PropertyDefinition] = field(default_factory=list)
    collections: list[Collection] = field(default_factory=list)
    raw: dict[str, Any] = field(repr=False, default_factory=dict)


@dataclass
class Space:
    id: str
    title: str
    structures: list[Structure] = field(default_factory=list)

    def get_structure(self, title: str) -> Structure | None:
        """Look up a structure by title (case-insensitive)."""
        title_lower = title.lower()
        return next(
            (s for s in self.structures if s.title.lower() == title_lower),
            None,
        )

    def structure_ids(self) -> dict[str, str]:
        """Return a mapping of title → id for all structures."""
        return {s.title: s.id for s in self.structures}
