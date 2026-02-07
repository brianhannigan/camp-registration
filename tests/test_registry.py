from pathlib import Path
import json

import pytest

from camp_registration.registry import CampRegistry, Camper


def test_register_camper_success():
    registry = CampRegistry()

    camper = registry.register_camper("Alex", 12, "Archery")

    assert camper == Camper("Alex", 12, "archery")
    assert registry.list_campers() == [camper]


def test_register_camper_validation():
    registry = CampRegistry()

    with pytest.raises(ValueError, match="name is required"):
        registry.register_camper(" ", 10, "archery")

    with pytest.raises(ValueError, match="between 7 and 17"):
        registry.register_camper("Sam", 6, "archery")

    with pytest.raises(ValueError, match="not available"):
        registry.register_camper("Sam", 10, "unknown")


def test_export_and_load(tmp_path: Path):
    registry = CampRegistry()
    registry.seed([Camper("Alex", 12, "archery"), Camper("Sam", 14, "hiking")])

    output_path = tmp_path / "campers.json"
    registry.export_json(output_path)

    loaded = CampRegistry()
    loaded.load_from_json(output_path)

    assert loaded.list_campers() == registry.list_campers()
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload[0]["name"] == "Alex"
