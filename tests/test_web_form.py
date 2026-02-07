import json
from pathlib import Path

from camp_registration.web_form import (
    CheckboxField,
    FormConfig,
    FormField,
    ActionStep,
    SelectField,
    _load_config,
    config_to_dict,
)


def test_config_to_dict_round_trip(tmp_path: Path):
    config = FormConfig(
        url="https://example.com/form",
        fields=[FormField(selector="#name", value="Alex")],
        checkboxes=[CheckboxField(selector="#agree", checked=True)],
        selects=[SelectField(selector="#session", value="archery")],
        submit_selector="button[type='submit']",
        wait_after_submit_ms=3000,
        actions=[ActionStep(kind="click", selector=".continue")],
    )

    payload = config_to_dict(config)
    path = tmp_path / "config.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    loaded = _load_config(path)

    assert loaded.url == config.url
    assert loaded.fields == config.fields
    assert loaded.checkboxes == config.checkboxes
    assert loaded.selects == config.selects
    assert loaded.submit_selector == config.submit_selector
    assert loaded.wait_after_submit_ms == config.wait_after_submit_ms
    assert loaded.actions == config.actions
