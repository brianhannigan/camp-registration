# camp-registration

A simple camp registration program with a CLI and registry utilities.

## Usage

```bash
python -m camp_registration.cli register "Alex" 12 archery
python -m camp_registration.cli list
python -m camp_registration.cli export campers.json
```

## Interactive UI

Launch the Tkinter-based UI to register campers and manage JSON exports:

```bash
python -m camp_registration.gui
```

## Website form automation

To automatically fill a website registration form (including option boxes, check boxes,
session selections, and payment fields), use the Playwright-based helper. Provide a JSON
config with selectors and values, then run:

```bash
python -m camp_registration.web_form path/to/form_config.json
```

### Config builder GUI

If you'd like a visual way to create the JSON config, launch the builder UI:

```bash
python -m camp_registration.form_builder
```

Use the form to add fields, checkboxes, and select options, then save the JSON file.

Example config:

```json
{
  "url": "https://example.com/register",
  "fields": [
    {"selector": "#camper-name", "value": "Alex Camper"},
    {"selector": "#credit-card-number", "value": "4111111111111111"},
    {"selector": "#credit-card-expiry", "value": "12/30"},
    {"selector": "#credit-card-cvv", "value": "123"}
  ],
  "checkboxes": [
    {"selector": "#agree-terms", "checked": true},
    {"selector": "input[name='sessions'][value='archery']", "checked": true},
    {"selector": "input[name='sessions'][value='hiking']", "checked": true}
  ],
  "selects": [
    {"selector": "#shirt-size", "value": "M"}
  ],
  "submit_selector": "button[type='submit']",
  "wait_after_submit_ms": 3000
}
```

This script uses Playwright, so make sure Playwright and browsers are installed before
running it (for example, `pip install playwright` and `playwright install`). Keep payment
data secure and avoid committing secrets to the repo.

## Development

```bash
python -m pytest
```
