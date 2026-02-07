from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Iterable


DEFAULT_SESSIONS = ("archery", "canoeing", "hiking", "arts")


@dataclass(frozen=True)
class Camper:
    name: str
    age: int
    session: str


@dataclass
class CampRegistry:
    allowed_sessions: set[str] = field(default_factory=lambda: set(DEFAULT_SESSIONS))
    campers: list[Camper] = field(default_factory=list)

    def register_camper(self, name: str, age: int, session: str) -> Camper:
        cleaned_name = name.strip()
        if not cleaned_name:
            raise ValueError("Camper name is required.")
        if age < 7 or age > 17:
            raise ValueError("Camper age must be between 7 and 17.")
        normalized_session = session.strip().lower()
        if normalized_session not in self.allowed_sessions:
            raise ValueError(
                f"Session '{session}' is not available."
            )

        camper = Camper(cleaned_name, age, normalized_session)
        self.campers.append(camper)
        return camper

    def list_campers(self) -> list[Camper]:
        return list(self.campers)

    def export_json(self, path: Path) -> None:
        payload = [asdict(camper) for camper in self.campers]
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def load_from_json(self, path: Path) -> None:
        data = json.loads(path.read_text(encoding="utf-8"))
        self.campers = [Camper(**entry) for entry in data]

    def seed(self, campers: Iterable[Camper]) -> None:
        self.campers.extend(campers)
