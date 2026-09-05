"""Recipes / Workflows — incident playbooks for FortiGate debug."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import DEFAULT_VERSION
from ui.widgets.tooltip import tip


class RecipesTab(BaseTab):
    """Temporary stub — full 42 playbooks being restored."""

    RECIPES = [
        "First steps connectivity",
        "Traffic not passing",
        "(restoring full list — see CHANGELOG)",
    ]

    def __init__(self, master, on_change=None, get_version=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Recipes / Workflows", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))
        ctk.CTkLabel(
            self,
            text="⚠ Full recipes temporarily unavailable — restoring…",
            text_color="orange",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))
        ctk.CTkLabel(self, text="Scenario").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.recipe = ctk.CTkOptionMenu(
            self, values=self.RECIPES, command=lambda _: self.notify_change(), width=280
        )
        self.recipe.set(self.RECIPES[0])
        self.recipe.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.grid_columnconfigure(1, weight=1)

    def generate_commands(self) -> str:
        return (
            "# Recipes temporarily stubbed during expansion.\n"
            "# Full 42 playbooks will be restored shortly.\n"
            "# See CHANGELOG.md [Unreleased].\n"
        )
