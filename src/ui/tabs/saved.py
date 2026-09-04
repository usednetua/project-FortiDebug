"""Saved Commands tab."""

import customtkinter as ctk
from tkinter import messagebox, simpledialog
import pyperclip

from ui.tabs.base_tab import BaseTab
from core.storage import list_commands, delete_command, update_command


class SavedTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._items = []
        self._build_ui()
        self.refresh()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Saved Commands", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 10))

        self.search = ctk.CTkEntry(self, placeholder_text="Search...")
        self.search.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=4)
        self.search.bind("<KeyRelease>", lambda e: self.refresh())

        self.btn_refresh = ctk.CTkButton(self, text="Refresh", width=80, command=self.refresh)
        self.btn_refresh.grid(row=1, column=2, padx=5, pady=4)

        self.listbox = ctk.CTkScrollableFrame(self, height=280)
        self.listbox.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=8)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=5)

        self.btn_copy = ctk.CTkButton(btn_frame, text="Copy", width=90, command=self.copy_selected)
        self.btn_copy.pack(side="left", padx=4)

        self.btn_edit = ctk.CTkButton(btn_frame, text="Edit", width=90, command=self.edit_selected)
        self.btn_edit.pack(side="left", padx=4)

        self.btn_delete = ctk.CTkButton(
            btn_frame, text="Delete", width=90, fg_color="#c0392b", hover_color="#e74c3c", command=self.delete_selected
        )
        self.btn_delete.pack(side="left", padx=4)

        self._selected_id = None
        self._selected_cmd = ""

    def refresh(self):
        for w in self.listbox.winfo_children():
            w.destroy()

        self._items = list_commands(self.search.get())
        self._selected_id = None
        self._selected_cmd = ""

        if not self._items:
            ctk.CTkLabel(self.listbox, text="No saved commands", text_color="gray").pack(pady=20)
            return

        for item in self._items:
            frame = ctk.CTkFrame(self.listbox)
            frame.pack(fill="x", pady=3, padx=2)

            label = f"{item['title']}"
            if item["category"]:
                label += f"  [{item['category']}]"

            btn = ctk.CTkButton(
                frame,
                text=label,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda i=item: self._select(i),
            )
            btn.pack(side="left", fill="x", expand=True, padx=4, pady=2)

            ctk.CTkLabel(frame, text=item["created_at"][:16], text_color="gray", width=110).pack(
                side="right", padx=6
            )

    def _select(self, item: dict):
        self._selected_id = item["id"]
        self._selected_cmd = item["command"]
        if self.on_change:
            # show command in preview
            self.on_change()

    def generate_commands(self) -> str:
        return self._selected_cmd or "# select a saved command"

    def copy_selected(self):
        if self._selected_cmd:
            pyperclip.copy(self._selected_cmd)
            messagebox.showinfo("Copied", "Command copied to clipboard.")

    def edit_selected(self):
        if self._selected_id is None:
            return
        item = next((i for i in self._items if i["id"] == self._selected_id), None)
        if not item:
            return

        title = simpledialog.askstring("Edit", "Title:", initialvalue=item["title"])
        if title is None:
            return
        category = simpledialog.askstring("Edit", "Category:", initialvalue=item["category"] or "")
        if category is None:
            category = item["category"] or ""
        notes = simpledialog.askstring("Edit", "Notes:", initialvalue=item["notes"] or "")
        if notes is None:
            notes = item["notes"] or ""

        update_command(self._selected_id, title.strip(), category.strip(), notes.strip())
        self.refresh()

    def delete_selected(self):
        if self._selected_id is None:
            return
        if messagebox.askyesno("Delete", "Delete this saved command?"):
            delete_command(self._selected_id)
            self._selected_id = None
            self._selected_cmd = ""
            self.refresh()
            if self.on_change:
                self.on_change()
