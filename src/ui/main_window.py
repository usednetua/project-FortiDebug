"""Main application window."""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import pyperclip

from ui.tabs.sessions import SessionsTab
from ui.tabs.ping import PingTab


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FortiDebug Builder")
        self.geometry("1100x720")
        self.minsize(900, 600)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        self.logo = ctk.CTkLabel(
            self.sidebar, text="FortiDebug", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.nav_buttons = {}
        sections = [
            ("sessions", "Sessions"),
            ("ping", "Ping"),
            ("traceroute", "Traceroute"),
            ("sniffer", "Sniffer"),
            ("flows", "Flows"),
            ("vpn", "VPN"),
            ("system_top", "System Top"),
            ("ha", "HA"),
            ("routing", "Routing"),
            ("saved", "Saved Commands"),
        ]

        for i, (key, label) in enumerate(sections, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                command=lambda k=key: self.show_tab(k),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
            )
            btn.grid(row=i, column=0, padx=10, pady=4, sticky="ew")
            self.nav_buttons[key] = btn

        # Content area
        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        # Preview + actions
        self.bottom = ctk.CTkFrame(self)
        self.bottom.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.bottom.grid_columnconfigure(0, weight=1)

        self.preview = ctk.CTkTextbox(
            self.bottom, height=140, font=ctk.CTkFont(family="Consolas", size=13)
        )
        self.preview.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=(5, 8))

        self.btn_copy = ctk.CTkButton(self.bottom, text="Copy", width=100, command=self.copy_commands)
        self.btn_copy.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.btn_save_txt = ctk.CTkButton(self.bottom, text="Save .txt", width=100, command=self.save_txt)
        self.btn_save_txt.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.btn_save_later = ctk.CTkButton(
            self.bottom, text="Save for Later", width=130, command=self.save_for_later, state="disabled"
        )
        self.btn_save_later.grid(row=1, column=2, padx=5, pady=5, sticky="w")

        # Tabs
        self.tabs = {}
        self.current_tab = None

        self.tabs["sessions"] = SessionsTab(self.content, on_change=self.on_tab_change)
        self.tabs["ping"] = PingTab(self.content, on_change=self.on_tab_change)

        # Placeholders
        for key in ["traceroute", "sniffer", "flows", "vpn", "system_top", "ha", "routing", "saved"]:
            frame = ctk.CTkFrame(self.content)
            ctk.CTkLabel(
                frame,
                text=f"{key.replace('_', ' ').title()} — coming soon",
                font=ctk.CTkFont(size=16),
            ).pack(expand=True)
            self.tabs[key] = frame

        self.show_tab("sessions")

    def show_tab(self, key: str):
        if self.current_tab is not None:
            self.tabs[self.current_tab].grid_forget()

        for k, btn in self.nav_buttons.items():
            if k == key:
                btn.configure(fg_color=("gray75", "gray25"))
            else:
                btn.configure(fg_color="transparent")

        tab = self.tabs[key]
        tab.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.current_tab = key

        if hasattr(tab, "generate_commands"):
            self.on_tab_change()
        else:
            self.preview.delete("1.0", "end")

    def on_tab_change(self):
        tab = self.tabs.get(self.current_tab)
        if tab and hasattr(tab, "generate_commands"):
            cmds = tab.generate_commands()
            self.preview.delete("1.0", "end")
            self.preview.insert("1.0", cmds)

    def copy_commands(self):
        text = self.preview.get("1.0", "end-1c").strip()
        if text:
            pyperclip.copy(text)
            messagebox.showinfo("Copied", "Commands copied to clipboard.")

    def save_txt(self):
        text = self.preview.get("1.0", "end-1c").strip()
        if not text:
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Save commands",
        )
        if path:
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            messagebox.showinfo("Saved", f"Saved to {path}")

    def save_for_later(self):
        messagebox.showinfo("Soon", "Saved Commands module will be available later.")
