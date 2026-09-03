"""Base class for all command tabs."""

import customtkinter as ctk
from typing import Callable, Optional


class BaseTab(ctk.CTkFrame):
    def __init__(self, master, on_change: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_change = on_change
        self.grid_columnconfigure(1, weight=1)

    def notify_change(self, *args):
        if self.on_change:
            self.on_change()

    def generate_commands(self) -> str:
        raise NotImplementedError
