"""Debug Flow tab v2 — iprope, IPv6, presets (Fortinet recommended)."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.safety import preamble, epilogue
from core.vdom import resolve_vd_index
from ui.widgets.tooltip import tip


class FlowsTab(BaseTab):
    PRESETS = {
        "": None,
        "Traffic denied": {"fn": True, "iprope": True, "count": "200"},
        "NAT check": {"fn": True, "iprope": False, "count": "100"},
        "Policy match": {"fn": True, "iprope": True, "count": "100"},
    }

    def __init__(
        self,
        master,
        on_change=None,
        get_vdom_mode=None,
        get_vdom_name=None,
        get_vdom_map=None,
        **kwargs,
    ):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_vdom_mode = get_vdom_mode or (lambda: False)
        self.get_vdom_name = get_vdom_name or (lambda: "root")
        self.get_vdom_map = get_vdom_map or (lambda: {})
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Debug Flow", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))

        warn = ctk.CTkLabel(
            self,
            text="⚠ Debug навантажує CPU — завжди використовуй фільтри",
            text_color="#e67e22",
        )
        warn.grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 6))

        ctk.CTkLabel(self, text="Preset").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        preset_values = [""] + sorted(
            [k for k in self.PRESETS.keys() if k], key=str.casefold
        )
        self.preset = ctk.CTkOptionMenu(
            self, values=preset_values, command=self._apply_preset
        )
        self.preset.set("")
        self.preset.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        tip(self.preset, "Готові набори опцій: denied / NAT / policy match")

        self.reset = ctk.CTkCheckBox(self, text="Reset debug state first", command=self.notify_change)
        self.reset.select()
        self.reset.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=2)
        tip(self.reset, "diagnose debug reset — очищає попередній debug state")

        self.clear_filter = ctk.CTkCheckBox(
            self, text="Clear flow filter first", command=self.notify_change
        )
        self.clear_filter.select()
        self.clear_filter.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=2)
        tip(self.clear_filter, "diagnose debug flow filter clear")

        self.debug_info = ctk.CTkCheckBox(
            self, text="Show diagnose debug info", command=self.notify_change
        )
        self.debug_info.grid(row=5, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        self.ipv6 = ctk.CTkCheckBox(self, text="IPv6 (filter6 / start6)", command=self.notify_change)
        self.ipv6.grid(row=6, column=0, columnspan=2, sticky="w", padx=10, pady=2)

        ctk.CTkLabel(self, text="Addr (any side)").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.addr = ctk.CTkEntry(self, placeholder_text="optional bidirectional")
        self.addr.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.addr.bind("<KeyRelease>", self.notify_change)
        tip(self.addr, "filter addr — збіг з будь-якої сторони")

        ctk.CTkLabel(self, text="Source address").grid(row=8, column=0, sticky="w", padx=10, pady=4)
        self.src = ctk.CTkEntry(self, placeholder_text="10.1.1.10")
        self.src.grid(row=8, column=1, sticky="ew", padx=10, pady=4)
        self.src.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Destination address").grid(row=9, column=0, sticky="w", padx=10, pady=4)
        self.dst = ctk.CTkEntry(self, placeholder_text="8.8.8.8")
        self.dst.grid(row=9, column=1, sticky="ew", padx=10, pady=4)
        self.dst.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Port").grid(row=10, column=0, sticky="w", padx=10, pady=4)
        self.port = ctk.CTkEntry(self, placeholder_text="")
        self.port.grid(row=10, column=1, sticky="ew", padx=10, pady=4)
        self.port.bind("<KeyRelease>", self.notify_change)

        ctk.CTkLabel(self, text="Protocol").grid(row=11, column=0, sticky="w", padx=10, pady=4)
        proto_values = sorted(["any", "1 (ICMP)", "6 (TCP)", "17 (UDP)"], key=str.casefold)
        self.proto = ctk.CTkOptionMenu(
            self,
            values=proto_values,
            command=lambda _: self.notify_change(),
        )
        self.proto.set("any")
        self.proto.grid(row=11, column=1, sticky="ew", padx=10, pady=4)

        ctk.CTkLabel(self, text="Trace count").grid(row=12, column=0, sticky="w", padx=10, pady=4)
        self.trace_count = ctk.CTkEntry(self, placeholder_text="1000")
        self.trace_count.insert(0, "1000")
        self.trace_count.grid(row=12, column=1, sticky="ew", padx=10, pady=4)
        self.trace_count.bind("<KeyRelease>", self.notify_change)
        tip(self.trace_count, "Ліміт пакетів trace start N — обов’язково на production")

        self.timestamps = ctk.CTkCheckBox(
            self, text="Console timestamps", command=self.notify_change
        )
        self.timestamps.select()
        self.timestamps.grid(row=13, column=0, columnspan=2, sticky="w", padx=10, pady=4)

        self.fn_name = ctk.CTkCheckBox(
            self, text="Show function-name", command=self.notify_change
        )
        self.fn_name.select()
        self.fn_name.grid(row=14, column=0, columnspan=2, sticky="w", padx=10, pady=2)
        tip(self.fn_name, "Показує імена функцій у flow output")

        self.iprope = ctk.CTkCheckBox(
            self, text="Show iprope (policy match detail)", command=self.notify_change
        )
        self.iprope.grid(row=15, column=0, columnspan=2, sticky="w", padx=10, pady=2)
        tip(self.iprope, "Деталі policy match (iprope) — корисно для denied/NAT")

        self.stop_debug = ctk.CTkCheckBox(
            self, text="Append stop-debug block", command=self.notify_change
        )
        self.stop_debug.select()
        self.stop_debug.grid(row=16, column=0, columnspan=2, sticky="w", padx=10, pady=4)
        tip(self.stop_debug, "diagnose debug disable + reset після тесту")

    def _apply_preset(self, name: str):
        cfg = self.PRESETS.get(name)
        if not cfg:
            self.notify_change()
            return
        if cfg.get("fn"):
            self.fn_name.select()
        else:
            self.fn_name.deselect()
        if cfg.get("iprope"):
            self.iprope.select()
        else:
            self.iprope.deselect()
        count = cfg.get("count", "1000")
        self.trace_count.delete(0, "end")
        self.trace_count.insert(0, count)
        self.notify_change()

    def generate_commands(self) -> str:
        ipv6 = bool(self.ipv6.get())
        filt = "diagnose debug flow filter6" if ipv6 else "diagnose debug flow filter"

        lines = preamble(
            reset=bool(self.reset.get()),
            clear_flow_filter=bool(self.clear_filter.get()),
            timestamps=bool(self.timestamps.get()),
            debug_info=bool(self.debug_info.get()),
        )

        if self.clear_filter.get() and ipv6:
            lines = [l for l in lines if l != "diagnose debug flow filter clear"]
            if bool(self.reset.get()):
                try:
                    idx = lines.index("diagnose debug reset") + 1
                except ValueError:
                    idx = 0
                lines.insert(idx, "diagnose debug flow filter6 clear")

        vd = resolve_vd_index(
            self.get_vdom_mode(), self.get_vdom_name(), "", self.get_vdom_map()
        )
        if vd:
            lines.append(f"{filt} vd {vd}")

        addr = self.addr.get().strip()
        if addr:
            lines.append(f"{filt} addr {addr}")

        src = self.src.get().strip()
        if src:
            lines.append(f"{filt} saddr {src}")

        dst = self.dst.get().strip()
        if dst:
            lines.append(f"{filt} daddr {dst}")

        port = self.port.get().strip()
        if port:
            lines.append(f"{filt} port {port}")

        proto = self.proto.get()
        if proto and proto != "any":
            lines.append(f"{filt} proto {proto.split()[0]}")

        if self.fn_name.get():
            lines.append("diagnose debug flow show function-name enable")
        if self.iprope.get():
            lines.append("diagnose debug flow show iprope enable")

        lines.append("diagnose debug flow show console enable")
        lines.append("diagnose debug enable")

        count = self.trace_count.get().strip() or "1000"
        if ipv6:
            lines.append(f"diagnose debug flow trace start6 {count}")
        else:
            lines.append(f"diagnose debug flow trace start {count}")

        lines.extend(epilogue(stop=bool(self.stop_debug.get())))
        return "\n".join(lines)
