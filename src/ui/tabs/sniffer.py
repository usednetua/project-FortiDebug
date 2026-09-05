"""Sniffer tab — BPF presets JSON, IPv6 host."""

import customtkinter as ctk
from tkinter import simpledialog, messagebox
from ui.tabs.base_tab import BaseTab
from core.config import load_bpf_presets, save_bpf_preset, delete_bpf_preset
from ui.widgets.tooltip import tip


class SnifferTab(BaseTab):
    VERBOSE_HELP = {
        "1": "headers only",
        "2": "headers + IP data",
        "3": "headers + Ethernet data",
        "4": "headers + interface names (default)",
        "5": "IP data + interface names",
        "6": "Ethernet data + interface names (full)",
    }

    BUILTIN_PRESETS = {
        "TCP SYN": "tcp[tcpflags] & (tcp-syn) != 0",
        "TCP RST": "tcp[tcpflags] & (tcp-rst) != 0",
        "New TCP (SYN no ACK)": "tcp[tcpflags] & (tcp-syn|tcp-ack) == tcp-syn",
        "SYN only": "tcp[tcpflags] == 2",
        "ICMP": "icmp",
        "ARP": "arp",
        "VLAN": "vlan",
        "IPv6": "ip6",
        "DNS": "port 53",
        "IKE/ESP": "udp port 500 or udp port 4500 or esp",
        "Broadcast": "ether broadcast",
        "Multicast": "ether multicast",
        "HTTP/HTTPS": "tcp port 80 or tcp port 443",
    }

    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(master, on_change=on_change, **kwargs)
        self._build_ui()

    def _all_presets(self):
        merged = dict(self.BUILTIN_PRESETS)
        merged.update(load_bpf_presets())
        return merged

    def _preset_names(self):
        return [""] + list(self._all_presets().keys())

    def _build_ui(self):
        title = ctk.CTkLabel(self, text="Sniffer", font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, columnspan=3, sticky="w", padx=10, pady=(5, 12))

        ctk.CTkLabel(self, text="Interface").grid(row=1, column=0, sticky="w", padx=10, pady=4)
        self.interface = ctk.CTkComboBox(
            self,
            values=["any", "port1", "port2", "wan1", "wan2", "internal", "vlan100"],
            command=lambda _: self.notify_change(),
        )
        self.interface.set("any")
        self.interface.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10, pady=4)
        tip(self.interface, "any = усі інтерфейси; для WAN краще конкретний if")

        ctk.CTkLabel(self, text="Verbose").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.verbose = ctk.CTkOptionMenu(
            self, values=["1", "2", "3", "4", "5", "6"], command=self._on_verbose_change
        )
        self.verbose.set("4")
        self.verbose.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        self.verbose_hint = ctk.CTkLabel(self, text=self.VERBOSE_HELP["4"], text_color="gray")
        self.verbose_hint.grid(row=2, column=2, sticky="w", padx=5)
        tip(self.verbose, "4 — зазвичай достатньо; 6 — повний Ethernet dump")

        ctk.CTkLabel(self, text="Count (0=unlimited)").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.count = ctk.CTkEntry(self, placeholder_text="0")
        self.count.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.count.bind("<KeyRelease>", self.notify_change)
        tip(self.count, "0 = без ліміту; Ctrl+C щоб зупинити на FGT")

        ctk.CTkLabel(self, text="Timestamp").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.ts = ctk.CTkOptionMenu(
            self,
            values=["none", "a (absolute)", "l (relative)"],
            command=lambda _: self.notify_change(),
        )
        self.ts.set("l (relative)")
        self.ts.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        tip(self.ts, "l = відносний час; a = абсолютний")

        self.use_bpf = ctk.CTkSwitch(
            self, text="Use custom BPF filter", command=self._toggle_mode
        )
        self.use_bpf.grid(row=5, column=0, columnspan=3, sticky="w", padx=10, pady=10)
        tip(self.use_bpf, "Розширений BPF або простий host/port")

        self.simple_frame = ctk.CTkFrame(self)
        self.simple_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.simple_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.simple_frame, text="Host (v4/v6)").grid(
            row=0, column=0, sticky="w", padx=8, pady=3
        )
        self.s_host = ctk.CTkEntry(self.simple_frame, placeholder_text="10.0.0.1 or 2001:db8::1")
        self.s_host.grid(row=0, column=1, sticky="ew", padx=8, pady=3)
        self.s_host.bind("<KeyRelease>", self.notify_change)
        tip(self.s_host, "IPv6 підтримується через host/src host/dst host")
        self.s_host_dir = ctk.CTkOptionMenu(
            self.simple_frame, values=["either", "src", "dst"], command=lambda _: self.notify_change()
        )
        self.s_host_dir.set("either")
        self.s_host_dir.grid(row=0, column=2, padx=5)

        ctk.CTkLabel(self.simple_frame, text="Port").grid(row=1, column=0, sticky="w", padx=8, pady=3)
        self.s_port = ctk.CTkEntry(self.simple_frame, placeholder_text="80")
        self.s_port.grid(row=1, column=1, sticky="ew", padx=8, pady=3)
        self.s_port.bind("<KeyRelease>", self.notify_change)
        self.s_port_dir = ctk.CTkOptionMenu(
            self.simple_frame, values=["either", "src", "dst"], command=lambda _: self.notify_change()
        )
        self.s_port_dir.set("either")
        self.s_port_dir.grid(row=1, column=2, padx=5)

        ctk.CTkLabel(self.simple_frame, text="Protocol").grid(row=2, column=0, sticky="w", padx=8, pady=3)
        self.s_proto = ctk.CTkOptionMenu(
            self.simple_frame,
            values=["any", "tcp", "udp", "icmp", "arp", "ip6"],
            command=lambda _: self.notify_change(),
        )
        self.s_proto.set("any")
        self.s_proto.grid(row=2, column=1, sticky="ew", padx=8, pady=3)

        self.bpf_frame = ctk.CTkFrame(self)
        ctk.CTkLabel(self.bpf_frame, text="Presets").grid(row=0, column=0, sticky="w", padx=8, pady=4)
        self.preset = ctk.CTkOptionMenu(
            self.bpf_frame, values=self._preset_names(), command=self._apply_preset
        )
        self.preset.set("")
        self.preset.grid(row=0, column=1, sticky="ew", padx=8, pady=4)

        btn_row = ctk.CTkFrame(self.bpf_frame, fg_color="transparent")
        btn_row.grid(row=0, column=2, padx=4)
        ctk.CTkButton(btn_row, text="Save BPF", width=80, command=self._save_bpf).pack(
            side="left", padx=2
        )
        ctk.CTkButton(btn_row, text="Del", width=50, command=self._del_bpf).pack(side="left", padx=2)

        ctk.CTkLabel(self.bpf_frame, text="BPF expression").grid(
            row=1, column=0, sticky="nw", padx=8, pady=4
        )
        self.bpf_text = ctk.CTkTextbox(self.bpf_frame, height=80)
        self.bpf_text.grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=4)
        self.bpf_text.bind("<KeyRelease>", self.notify_change)
        self.bpf_frame.grid_columnconfigure(1, weight=1)
        self.bpf_frame.grid_remove()

    def _on_verbose_change(self, value):
        self.verbose_hint.configure(text=self.VERBOSE_HELP.get(value, ""))
        self.notify_change()

    def _toggle_mode(self):
        if self.use_bpf.get():
            self.simple_frame.grid_remove()
            self.bpf_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
            self.preset.configure(values=self._preset_names())
        else:
            self.bpf_frame.grid_remove()
            self.simple_frame.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.notify_change()

    def _apply_preset(self, name):
        presets = self._all_presets()
        if name and name in presets:
            self.bpf_text.delete("1.0", "end")
            self.bpf_text.insert("1.0", presets[name])
            self.notify_change()

    def _save_bpf(self):
        expr = self.bpf_text.get("1.0", "end-1c").strip()
        if not expr:
            messagebox.showwarning("Empty", "BPF expression is empty")
            return
        name = simpledialog.askstring("Save BPF", "Preset name:")
        if not name:
            return
        save_bpf_preset(name.strip(), expr)
        self.preset.configure(values=self._preset_names())
        self.preset.set(name.strip())
        messagebox.showinfo("Saved", f"Saved «{name.strip()}»")

    def _del_bpf(self):
        name = self.preset.get()
        custom = load_bpf_presets()
        if name not in custom:
            messagebox.showinfo("Info", "Only custom presets can be deleted")
            return
        if messagebox.askyesno("Delete", f"Delete «{name}»?"):
            delete_bpf_preset(name)
            self.preset.configure(values=self._preset_names())
            self.preset.set("")

    def _build_simple_filter(self) -> str:
        parts = []
        host = self.s_host.get().strip()
        if host:
            d = self.s_host_dir.get()
            if d == "src":
                parts.append(f"src host {host}")
            elif d == "dst":
                parts.append(f"dst host {host}")
            else:
                parts.append(f"host {host}")
        port = self.s_port.get().strip()
        if port:
            d = self.s_port_dir.get()
            if d == "src":
                parts.append(f"src port {port}")
            elif d == "dst":
                parts.append(f"dst port {port}")
            else:
                parts.append(f"port {port}")
        proto = self.s_proto.get()
        if proto and proto != "any":
            parts.append(proto)
        return " and ".join(parts) if parts else ""

    def generate_commands(self) -> str:
        iface = self.interface.get().strip() or "any"
        verbose = self.verbose.get()
        count = self.count.get().strip() or "0"
        ts = self.ts.get()
        ts_flag = ""
        if ts.startswith("a"):
            ts_flag = "a"
        elif ts.startswith("l"):
            ts_flag = "l"

        if self.use_bpf.get():
            filt = self.bpf_text.get("1.0", "end-1c").strip()
        else:
            filt = self._build_simple_filter()

        cmd = f"diagnose sniffer packet {iface} '{filt}' {verbose} {count}"
        if ts_flag:
            cmd += f" {ts_flag}"
        return cmd
