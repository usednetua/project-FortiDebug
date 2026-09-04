"""Debug Flow tab — diagnose debug flow (Fortinet recommended sequence)."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue


class FlowsTab(BaseTab):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Debug Flow", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 12))

        warn = ctk.CTkLabel(
            self,
            text="⚠ Debug навантажує CPU — завжди використовуй фільтри",
            text_color="#e67e22",
        )
        warn.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))

        self.reset = ctk.CTkCheckBox(self, text="Reset debug state first", command=self.notify_change)
        self.reset.select()
        self.reset.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.clear_filter = ctk.CTkCheckBox(
            self, text="Clear flow filter first", command=self.notify_change
        )
        self.clear_filter.select()
        self.clear_filter.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.debug_info = ctk.CTkCheckBox(
            self, text="Show diagnose debug info", command=self.notify_change
        )
        self.debug_info.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Source address").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.src = ctk.CTkEntry(self, placeholder_text="10.1.1.10")
        self.src.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.src.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination address").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.dst = ctk.CTkEntry(self, placeholder_text="8.8.8.8")
        self.dst.grid(row=6, column=1, sticky="ew", padx=10, pady=4)
        self.dst.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Port").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.port = ctk.CTkEntry(self, placeholder_text="")
        self.port.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.port.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Protocol").grid(row=8, column=0, sticky="w", padx=10, pady=4)
        self.proto = ctk.CTkOptionMenu(
            self,
            values=["any", "1 (ICMP)", "6 (TCP)", "17 (UDP)"],
            command=lambda _: self.notify_change(),
        )
        self.proto.set("any")
        self.proto.grid(row=8, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self, text="Trace count").grid(row=9, column=0, sticky="w", padx=10, pady=4)
        self.trace_count = ctk.CTkEntry(self, placeholder_text="1000")
        self.trace_count.insert(0, "1000")
        self.trace_count.grid(row=9, column=1, sticky="ew", padx=10, pady=4)
        self.trace_count.bind("<KeyRelease>", self.notify_change)

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=10, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.fn_name = ctk.CTkCheckBox(
            self, text="Show function-name", command=self.notify_change
        )
        self.fn_name.select()
        self.fn_name.grid(row=11, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.stop_debug = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_debug.select()
        self.stop_debug.grid(row=12, column=0, columnspan=2, sticky="w", padx=10, pady=4)

    def generate_commands(self) -> str:
        lines = preamble(
            reset=bool(self.reset.get()),
            clear_flow_filter=bool(self.clear_filter.get()),
            timestamps=bool(self.timestamps.get()),
            debug_info=bool(self.debug_info.get()),
        )

        src = self.src.get().strip()
        if src:
            lines.append(f"diagnose debug flow filter saddr {src}")

        dst = self.dst.get().strip()
        if dst:
            lines.append(f"diagnose debug flow filter daddr {dst}")

        port = self.port.get().strip()
        if port:
            lines.append(f"diagnose debug flow filter port {port}")

        proto = self.proto.get()
        if proto and proto != "any":
            lines.append(f"diagnose debug flow filter proto {proto.split()[0]}")

        if self.fn_name.get():
            lines.append("diagnose debug flow show function-name enable")

        lines.append("diagnose debug flow show console enable")
        lines.append("diagnose debug enable")

        count = self.trace_count.get().strip() or "1000"
        lines.append(f"diagnose debug flow trace start {count}")

        lines.extend(epilogue(stop=bool(self.stop_debug.get())))
        return "\n".join(lines)
