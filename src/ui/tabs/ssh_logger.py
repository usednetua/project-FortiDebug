"""SSH Session Logger — generate command to start SSH with auto-logging."""

import customtkinter as ctk
from datetime import datetime
from ui.tabs.base_tab import BaseTab


class SshLoggerTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="SSH Session Logger", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 15))

        ctk.CTkLabel(self, text="Host / IP").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.host = ctk.CTkEntry(self, placeholder_text="192.168.1.99")
        self.host.grid(row=1, column=1, sticky="ew", padx=10, pady=4)
        self.host.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Username").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.user = ctk.CTkEntry(self, placeholder_text="admin")
        self.user.insert(0, "admin")
        self.user.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.user.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Port").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.port = ctk.CTkEntry(self, placeholder_text="22")
        self.port.insert(0, "22")
        self.port.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.port.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Log folder").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.log_dir = ctk.CTkEntry(self, placeholder_text="C:\\Logs\\FortiGate")
        self.log_dir.insert(0, "C:\\Logs\\FortiGate")
        self.log_dir.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.log_dir.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Shell").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        shell_values = sorted(
            ["PowerShell (Tee-Object)", "CMD (tee if available)", "Git Bash / WSL"],
            key=str.casefold,
        )
        self.shell = ctk.CTkOptionMenu(
            self,
            values=shell_values,
            command=lambda _: self.notify_change(),
        )
        self.shell.set("PowerShell (Tee-Object)")
        self.shell.grid(row=5, column=1, sticky="ew", padx=10, pady=4)

        self.include_mkdir = ctk.CTkCheckBox(
            self, text="Create log folder if missing", command=self.notify_change
        )
        self.include_mkdir.select()
        self.include_mkdir.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=8)

        note = ctk.CTkLabel(
            self,
            text="Скопіюй команду → встав у термінал. Сесія пишеться в файл з timestamp.",
            text_color="gray",
            wraplength=450,
        )
        note.grid(row=7, column=0, columnspan=2, sticky="w", padx=10, pady=10)

    def generate_commands(self) -> str:
        host = self.host.get().strip() or "<host>"
        user = self.user.get().strip() or "admin"
        port = self.port.get().strip() or "22"
        log_dir = self.log_dir.get().strip() or "C:\\Logs\\FortiGate"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_dir}\\ssh_{host.replace('.', '_')}_{ts}.log"

        shell = self.shell.get()
        lines = []

        if self.include_mkdir.get():
            if "PowerShell" in shell:
                lines.append(f'New-Item -ItemType Directory -Force -Path "{log_dir}" | Out-Null')
            else:
                lines.append(f'mkdir "{log_dir}" 2>nul')

        ssh_cmd = f"ssh -p {port} {user}@{host}"

        if "PowerShell" in shell:
            lines.append(f'{ssh_cmd} | Tee-Object -FilePath "{log_file}"')
        elif "CMD" in shell:
            lines.append(f'{ssh_cmd} | tee "{log_file}"')
        else:  # Git Bash / WSL
            lines.append(f'{ssh_cmd} | tee "{log_file}"')

        lines.append("")
        lines.append(f"# Log file: {log_file}")
        return "\n".join(lines)
