from __future__ import annotations

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from camp_registration.registry import CampRegistry, DEFAULT_SESSIONS


class CampRegistrationApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.registry = CampRegistry()
        self.root.title("Camp Registration")
        self.root.geometry("640x420")
        self.root.minsize(560, 380)

        self._build_layout()

    def _build_layout(self) -> None:
        header = ttk.Label(
            self.root, text="Camp Registration", font=("Helvetica", 18, "bold")
        )
        header.pack(pady=(16, 8))

        content = ttk.Frame(self.root, padding=(16, 8))
        content.pack(fill=tk.BOTH, expand=True)

        form_frame = ttk.LabelFrame(content, text="Register a camper")
        form_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Label(form_frame, text="Name").grid(row=0, column=0, sticky=tk.W, padx=8)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky=tk.EW, padx=8, pady=6)

        ttk.Label(form_frame, text="Age").grid(row=1, column=0, sticky=tk.W, padx=8)
        self.age_entry = ttk.Entry(form_frame)
        self.age_entry.grid(row=1, column=1, sticky=tk.EW, padx=8, pady=6)

        ttk.Label(form_frame, text="Session").grid(
            row=2, column=0, sticky=tk.W, padx=8
        )
        self.session_value = tk.StringVar(value=DEFAULT_SESSIONS[0])
        session_menu = ttk.OptionMenu(
            form_frame, self.session_value, DEFAULT_SESSIONS[0], *DEFAULT_SESSIONS
        )
        session_menu.grid(row=2, column=1, sticky=tk.EW, padx=8, pady=6)

        form_frame.columnconfigure(1, weight=1)

        register_button = ttk.Button(
            form_frame, text="Register camper", command=self._register_camper
        )
        register_button.grid(row=3, column=0, columnspan=2, pady=(6, 12))

        list_frame = ttk.LabelFrame(content, text="Registered campers")
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.campers_list = tk.Listbox(list_frame, height=8)
        self.campers_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=8, pady=8)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        scrollbar.config(command=self.campers_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=8)
        self.campers_list.config(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(self.root, padding=(16, 8))
        actions.pack(fill=tk.X)

        ttk.Button(actions, text="Load from JSON", command=self._load_json).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(actions, text="Export to JSON", command=self._export_json).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(actions, text="Clear", command=self._clear_list).pack(
            side=tk.RIGHT, padx=4
        )

        self.status_value = tk.StringVar(value="Ready")
        status = ttk.Label(self.root, textvariable=self.status_value, anchor=tk.W)
        status.pack(fill=tk.X, padx=16, pady=(0, 12))

    def _register_camper(self) -> None:
        name = self.name_entry.get()
        age_text = self.age_entry.get()
        session = self.session_value.get()

        try:
            age = int(age_text)
        except ValueError:
            messagebox.showerror("Invalid age", "Please enter a valid age number.")
            return

        try:
            camper = self.registry.register_camper(name, age, session)
        except ValueError as exc:
            messagebox.showerror("Unable to register", str(exc))
            return

        self._add_camper_to_list(camper)
        self.status_value.set(f"Registered {camper.name} for {camper.session}.")
        self.name_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.name_entry.focus_set()

    def _add_camper_to_list(self, camper) -> None:
        self.campers_list.insert(
            tk.END, f"{camper.name} (age {camper.age}) - {camper.session}"
        )

    def _load_json(self) -> None:
        path = filedialog.askopenfilename(
            title="Load campers",
            filetypes=[("JSON files", "*.json"), ("All files", "*")],
        )
        if not path:
            return

        try:
            self.registry.load_from_json(path)
        except (OSError, ValueError) as exc:
            messagebox.showerror("Unable to load", str(exc))
            return

        self.campers_list.delete(0, tk.END)
        for camper in self.registry.list_campers():
            self._add_camper_to_list(camper)
        self.status_value.set(f"Loaded {len(self.registry.campers)} campers.")

    def _export_json(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Export campers",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*")],
        )
        if not path:
            return

        try:
            self.registry.export_json(path)
        except OSError as exc:
            messagebox.showerror("Unable to export", str(exc))
            return

        self.status_value.set(f"Exported {len(self.registry.campers)} campers.")

    def _clear_list(self) -> None:
        self.registry.campers.clear()
        self.campers_list.delete(0, tk.END)
        self.status_value.set("Cleared all campers.")


def main() -> None:
    root = tk.Tk()
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    CampRegistrationApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
