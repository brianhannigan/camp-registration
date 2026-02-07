from __future__ import annotations

import json
import sys
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[1]))

from camp_registration.web_form import (
    CheckboxField,
    FormConfig,
    FormField,
    SelectField,
    config_to_dict,
)


@dataclass
class BuilderItem:
    kind: str
    selector: str
    value: str
    checked: bool


class FormBuilderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Form Config Builder")
        self.root.geometry("720x520")
        self.root.minsize(640, 480)
        self.items: list[BuilderItem] = []

        self._build_layout()

    def _build_layout(self) -> None:
        header = ttk.Label(
            self.root, text="Registration Form Config Builder", font=("Helvetica", 16, "bold")
        )
        header.pack(pady=(16, 8))

        content = ttk.Frame(self.root, padding=(16, 8))
        content.pack(fill=tk.BOTH, expand=True)

        url_frame = ttk.LabelFrame(content, text="Form details")
        url_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(url_frame, text="Form URL").grid(row=0, column=0, sticky=tk.W, padx=8)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=6)

        ttk.Label(url_frame, text="Submit selector").grid(
            row=1, column=0, sticky=tk.W, padx=8
        )
        self.submit_entry = ttk.Entry(url_frame)
        self.submit_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=6)

        ttk.Label(url_frame, text="Wait after submit (ms)").grid(
            row=2, column=0, sticky=tk.W, padx=8
        )
        self.wait_entry = ttk.Entry(url_frame)
        self.wait_entry.insert(0, "2000")
        self.wait_entry.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=6)

        url_frame.columnconfigure(1, weight=1)

        entry_frame = ttk.LabelFrame(content, text="Add form element")
        entry_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(entry_frame, text="Type").grid(row=0, column=0, sticky=tk.W, padx=8)
        self.kind_value = tk.StringVar(value="field")
        kind_menu = ttk.OptionMenu(
            entry_frame, self.kind_value, "field", "field", "checkbox", "select"
        )
        kind_menu.grid(row=0, column=1, sticky=tk.W, padx=8, pady=6)

        ttk.Label(entry_frame, text="Selector").grid(row=1, column=0, sticky=tk.W, padx=8)
        self.selector_entry = ttk.Entry(entry_frame)
        self.selector_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=6)

        ttk.Label(entry_frame, text="Value").grid(row=2, column=0, sticky=tk.W, padx=8)
        self.value_entry = ttk.Entry(entry_frame)
        self.value_entry.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=6)

        self.checked_value = tk.BooleanVar(value=True)
        checked = ttk.Checkbutton(entry_frame, text="Checked", variable=self.checked_value)
        checked.grid(row=3, column=1, sticky=tk.W, padx=8, pady=(0, 6))

        add_button = ttk.Button(entry_frame, text="Add", command=self._add_item)
        add_button.grid(row=4, column=0, columnspan=2, pady=(4, 8))

        entry_frame.columnconfigure(1, weight=1)

        list_frame = ttk.LabelFrame(content, text="Form elements")
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.items_list = tk.Listbox(list_frame, height=8)
        self.items_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.items_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=8)
        self.items_list.config(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(self.root, padding=(16, 8))
        actions.pack(fill=tk.X)

        ttk.Button(actions, text="Remove selected", command=self._remove_selected).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(actions, text="Save config", command=self._save_config).pack(
            side=tk.RIGHT, padx=4
        )

        self.status_value = tk.StringVar(value="Ready")
        status = ttk.Label(self.root, textvariable=self.status_value, anchor=tk.W)
        status.pack(fill=tk.X, padx=16, pady=(0, 12))

    def _add_item(self) -> None:
        selector = self.selector_entry.get().strip()
        if not selector:
            messagebox.showerror("Missing selector", "Please provide a selector.")
            return
        kind = self.kind_value.get()
        value = self.value_entry.get().strip()
        checked = self.checked_value.get()

        if kind in {"field", "select"} and not value:
            messagebox.showerror("Missing value", "Please provide a value.")
            return

        item = BuilderItem(kind=kind, selector=selector, value=value, checked=checked)
        self.items.append(item)
        self.items_list.insert(
            tk.END, f"{item.kind}: {item.selector} -> {item.value or item.checked}"
        )
        self.selector_entry.delete(0, tk.END)
        self.value_entry.delete(0, tk.END)
        self.checked_value.set(True)
        self.selector_entry.focus_set()

    def _remove_selected(self) -> None:
        selection = self.items_list.curselection()
        if not selection:
            return
        index = selection[0]
        self.items_list.delete(index)
        self.items.pop(index)

    def _save_config(self) -> None:
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Missing URL", "Please provide the form URL.")
            return

        try:
            wait_ms = int(self.wait_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid wait", "Wait time must be a number.")
            return

        submit_selector = self.submit_entry.get().strip() or None

        config = FormConfig(url=url, submit_selector=submit_selector, wait_after_submit_ms=wait_ms)
        for item in self.items:
            if item.kind == "field":
                config.fields.append(FormField(selector=item.selector, value=item.value))
            elif item.kind == "checkbox":
                config.checkboxes.append(
                    CheckboxField(selector=item.selector, checked=item.checked)
                )
            elif item.kind == "select":
                config.selects.append(SelectField(selector=item.selector, value=item.value))

        payload = config_to_dict(config)
        path = filedialog.asksaveasfilename(
            title="Save config",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*")],
        )
        if not path:
            return

        try:
            Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except OSError as exc:
            messagebox.showerror("Unable to save", str(exc))
            return

        self.status_value.set(f"Saved config to {path}.")


def main() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    FormBuilderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
