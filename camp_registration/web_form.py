from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FormField:
    selector: str
    value: str


@dataclass
class CheckboxField:
    selector: str
    checked: bool = True


@dataclass
class SelectField:
    selector: str
    value: str


@dataclass
class ActionStep:
    kind: str
    selector: str | None = None
    wait_ms: int | None = None


@dataclass
class FormConfig:
    url: str
    fields: list[FormField] = field(default_factory=list)
    checkboxes: list[CheckboxField] = field(default_factory=list)
    selects: list[SelectField] = field(default_factory=list)
    submit_selector: str | None = None
    wait_after_submit_ms: int = 2000
    actions: list[ActionStep] = field(default_factory=list)


def _load_config(path: Path) -> FormConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    fields = [FormField(**item) for item in data.get("fields", [])]
    checkboxes = [CheckboxField(**item) for item in data.get("checkboxes", [])]
    selects = [SelectField(**item) for item in data.get("selects", [])]
    actions = [ActionStep(**item) for item in data.get("actions", [])]
    return FormConfig(
        url=data["url"],
        fields=fields,
        checkboxes=checkboxes,
        selects=selects,
        submit_selector=data.get("submit_selector"),
        wait_after_submit_ms=data.get("wait_after_submit_ms", 2000),
        actions=actions,
    )


def config_to_dict(config: FormConfig) -> dict[str, object]:
    return {
        "url": config.url,
        "fields": [field.__dict__ for field in config.fields],
        "checkboxes": [checkbox.__dict__ for checkbox in config.checkboxes],
        "selects": [select.__dict__ for select in config.selects],
        "submit_selector": config.submit_selector,
        "wait_after_submit_ms": config.wait_after_submit_ms,
        "actions": [action.__dict__ for action in config.actions],
    }


def _fill_form(page, config: FormConfig) -> None:
    page.goto(config.url, wait_until="domcontentloaded")

    for field in config.fields:
        page.fill(field.selector, field.value)

    for checkbox in config.checkboxes:
        if checkbox.checked:
            page.check(checkbox.selector)
        else:
            page.uncheck(checkbox.selector)

    for select in config.selects:
        page.select_option(select.selector, select.value)

    for action in config.actions:
        if action.kind == "click" and action.selector:
            page.click(action.selector)
        elif action.kind == "wait":
            page.wait_for_timeout(action.wait_ms or 0)

    if config.submit_selector:
        page.click(config.submit_selector)
        page.wait_for_timeout(config.wait_after_submit_ms)


def run(config_path: Path, headless: bool) -> None:
    from playwright.sync_api import sync_playwright

    config = _load_config(config_path)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=headless)
        page = browser.new_page()
        _fill_form(page, config)
        browser.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Automate filling a camp registration website form."
    )
    parser.add_argument("config", type=Path, help="Path to form config JSON")
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser in headed mode (default is headless).",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    run(args.config, headless=not args.headed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
