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

## Development

```bash
python -m pytest
```
