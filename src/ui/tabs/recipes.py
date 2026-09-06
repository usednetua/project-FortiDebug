"""Recipes / Workflows — incident playbooks for FortiGate debug."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from ui.tabs.recipe_impl import RecipeImplMixin
from ui.tabs.recipe_extra import RecipeExtraMixin
from ui.tabs.recipe_r6 import RecipeR6Mixin
from ui.tabs.recipe_r8 import RecipeR8Mixin
from ui.tabs.recipe_r9 import RecipeR9Mixin
from ui.tabs.recipe_r10 import RecipeR10Mixin
from ui.tabs.recipe_r11 import RecipeR11Mixin
from core.fortios_version import DEFAULT_VERSION
from core.vdom import resolve_vd_index
from ui.widgets.tooltip import tip


class RecipesTab(
    RecipeR11Mixin,
    RecipeR10Mixin,
    RecipeR9Mixin,
    RecipeR8Mixin,
    RecipeR6Mixin,
    RecipeExtraMixin,
    RecipeImplMixin,
    BaseTab,
):
    RECIPES = [
        "First steps connectivity",
        "Traffic not passing",
        "VPN down / rekey",
        "Dial-up IPsec",
        "SSL VPN login fail",
        "SD-WAN member dead",
        "High CPU",
        "High memory / conserv mode",
        "Session table full",
        "Policy / NAT check",
        "VIP / port forward",
        "Local-in / admin access",
        "HA out-of-sync",
        "OSPF neighbor down",
        "BGP neighbor down",
        "Static route / RIB",
        "DHCP no lease",
        "Auth / FSSO",
        "DNS issues",
        "Webfilter / URL block",
        "IPS / UTM hit",
        "Explicit proxy",
        "Wireless AP / client",
        "LACP / aggregate",
        "Interface / link down",
        "NPU / offload check",
        "Certificate / SSL inspect",
        "FortiGuard / license",
        "Log disk / crashlog",
        "NTP / time sync",
        "IPv6 connectivity",
        "Multicast",
        "ZTNA / Access Proxy",
        "FortiAnalyzer / remote logging",
        "WAD / Proxy engine",
        "DoS / Flood protection",
        "User auth LDAP/RADIUS/TACACS",
        "General TAC collect / healthcheck",
        "ARP / Neighbor",
        "Link-monitor / health-check",
        "Antivirus / AV engine",
        "Traffic shaping / QoS",
        "ADVPN / Shortcut tunnels",
        "SIP / VoIP / ALG",
        "Application Control / ISDB",
        "Email filter / Antispam",
        "File filter / DLP",
        "Transparent mode / Bridging",
        "Modem / LTE / PPP",
        "RIP neighbor / routes",
        "SSL VPN web-mode",
        "IS-IS neighbor / LSP",
        "Automation Stitch",
        "IoC / Threat feed",
        "Cloud SDN connector",
        # Release 11
        "BFD neighbor",
        "SAML SSO / admin login",
    ]

    def __init__(
        self,
        master,
        on_change=None,
        get_version=None,
        get_vdom_mode=None,
        get_vdom_name=None,
        get_vdom_map=None,
        **kwargs,
    ):
        super().__init__(master, on_change=on_change, **kwargs)
        self.get_version = get_version or (lambda: DEFAULT_VERSION)
        self.get_vdom_mode = get_vdom_mode or (lambda: False)
        self.get_vdom_name = get_vdom_name or (lambda: "root")
        self.get_vdom_map = get_vdom_map or (lambda: {})
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Recipes / Workflows", font=ctk.CTkFont(size=18, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", padx=10, pady=(5, 8))
        ctk.CTkLabel(
            self,
            text=f"{len(self.RECIPES)} playbooks — заповни поля де потрібно → Copy / Export",
            text_color="gray",
        ).grid(row=1, column=0, columnspan=2, sticky="w", padx=10, pady=(0, 8))
        ctk.CTkLabel(self, text="Scenario").grid(row=2, column=0, sticky="w", padx=10, pady=4)
        self.recipe = ctk.CTkOptionMenu(
            self, values=self.RECIPES, command=lambda _: self.notify_change(), width=280
        )
        self.recipe.set(self.RECIPES[0])
        self.recipe.grid(row=2, column=1, sticky="ew", padx=10, pady=4)
        tip(self.recipe, "Типові інциденти FortiGate")
        ctk.CTkLabel(self, text="Source / Client IP").grid(row=3, column=0, sticky="w", padx=10, pady=4)
        self.src = ctk.CTkEntry(self, placeholder_text="optional")
        self.src.grid(row=3, column=1, sticky="ew", padx=10, pady=4)
        self.src.bind("<KeyRelease>", self.notify_change)
        ctk.CTkLabel(self, text="Destination / VIP").grid(row=4, column=0, sticky="w", padx=10, pady=4)
        self.dst = ctk.CTkEntry(self, placeholder_text="optional")
        self.dst.grid(row=4, column=1, sticky="ew", padx=10, pady=4)
        self.dst.bind("<KeyRelease>", self.notify_change)
        ctk.CTkLabel(self, text="Port").grid(row=5, column=0, sticky="w", padx=10, pady=4)
        self.port = ctk.CTkEntry(self, placeholder_text="optional")
        self.port.grid(row=5, column=1, sticky="ew", padx=10, pady=4)
        self.port.bind("<KeyRelease>", self.notify_change)
        ctk.CTkLabel(self, text="Peer / Phase1 / Neighbor").grid(row=6, column=0, sticky="w", padx=10, pady=4)
        self.peer = ctk.CTkEntry(self, placeholder_text="IP or name")
        self.peer.grid(row=6, column=1, sticky="ew", padx=10, pady=4)
        self.peer.bind("<KeyRelease>", self.notify_change)
        ctk.CTkLabel(self, text="Interface").grid(row=7, column=0, sticky="w", padx=10, pady=4)
        self.wan = ctk.CTkEntry(self, placeholder_text="wan1 / any / port1")
        self.wan.grid(row=7, column=1, sticky="ew", padx=10, pady=4)
        self.wan.bind("<KeyRelease>", self.notify_change)
        ctk.CTkLabel(self, text="VDOM index override").grid(row=8, column=0, sticky="w", padx=10, pady=4)
        self.vdom = ctk.CTkEntry(self, placeholder_text="optional; map/sidebar is primary")
        self.vdom.grid(row=8, column=1, sticky="ew", padx=10, pady=4)
        self.vdom.bind("<KeyRelease>", self.notify_change)
        tip(
            self.vdom,
            "Override filter vd. Інакше — Settings map + sidebar VDOM name.",
        )
        self.grid_columnconfigure(1, weight=1)

    def current_recipe_name(self) -> str:
        try:
            return self.recipe.get() or ""
        except Exception:
            return ""

    def _resolved_vd(self) -> str:
        return resolve_vd_index(
            self.get_vdom_mode(),
            self.get_vdom_name(),
            self.vdom.get().strip(),
            self.get_vdom_map(),
        )

    def generate_commands(self) -> str:
        name = self.recipe.get()
        src = self.src.get().strip()
        dst = self.dst.get().strip()
        port = self.port.get().strip()
        peer = self.peer.get().strip()
        iface = self.wan.get().strip() or "any"
        vd = self._resolved_vd()
        version = self.get_version()
        dispatch = {
            "First steps connectivity": lambda: self._first_steps(src, dst, port, vd),
            "Traffic not passing": lambda: self._traffic_not_passing(src, dst, port, vd),
            "VPN down / rekey": lambda: self._vpn_down(version, peer),
            "Dial-up IPsec": lambda: self._dialup_ipsec(version, peer, src),
            "SSL VPN login fail": lambda: self._ssl_login_fail(src),
            "SD-WAN member dead": lambda: self._sdwan_dead(version),
            "High CPU": self._high_cpu,
            "High memory / conserv mode": self._high_memory,
            "Session table full": self._session_full,
            "Policy / NAT check": lambda: self._policy_nat(src, dst, port),
            "VIP / port forward": lambda: self._vip(src, dst, port, iface),
            "Local-in / admin access": lambda: self._local_in(src, iface),
            "HA out-of-sync": self._ha_sync,
            "OSPF neighbor down": self._ospf,
            "BGP neighbor down": lambda: self._bgp(peer),
            "Static route / RIB": lambda: self._routing(dst),
            "DHCP no lease": lambda: self._dhcp(iface),
            "Auth / FSSO": self._auth_fsso,
            "DNS issues": lambda: self._dns(src, dst),
            "Webfilter / URL block": lambda: self._webfilter(src),
            "IPS / UTM hit": lambda: self._ips_utm(src, dst),
            "Explicit proxy": lambda: self._explicit_proxy(src),
            "Wireless AP / client": self._wireless,
            "LACP / aggregate": lambda: self._lacp(iface),
            "Interface / link down": lambda: self._interface(iface),
            "NPU / offload check": self._npu,
            "Certificate / SSL inspect": self._certificate,
            "FortiGuard / license": self._fortiguard,
            "Log disk / crashlog": self._log_disk,
            "NTP / time sync": self._ntp,
            "IPv6 connectivity": lambda: self._ipv6(src, dst),
            "Multicast": lambda: self._multicast(iface),
            "ZTNA / Access Proxy": lambda: self._ztna(version, src, dst),
            "FortiAnalyzer / remote logging": self._faz_logging,
            "WAD / Proxy engine": lambda: self._wad(src, dst),
            "DoS / Flood protection": self._dos,
            "User auth LDAP/RADIUS/TACACS": lambda: self._user_auth(src),
            "General TAC collect / healthcheck": self._tac_healthcheck,
            "ARP / Neighbor": lambda: self._arp(iface),
            "Link-monitor / health-check": self._link_monitor,
            "Antivirus / AV engine": lambda: self._antivirus(src, dst),
            "Traffic shaping / QoS": self._shaper,
            "ADVPN / Shortcut tunnels": lambda: self._advpn(version, peer, iface, src, dst),
            "SIP / VoIP / ALG": lambda: self._sip_voip(src, dst, port, iface),
            "Application Control / ISDB": lambda: self._app_control(version, src, dst),
            "Email filter / Antispam": lambda: self._email_filter(src, dst),
            "File filter / DLP": lambda: self._file_dlp(src, dst),
            "Transparent mode / Bridging": lambda: self._transparent_bridge(iface),
            "Modem / LTE / PPP": lambda: self._modem_lte(iface),
            "RIP neighbor / routes": self._rip,
            "SSL VPN web-mode": lambda: self._ssl_web_mode(src),
            "IS-IS neighbor / LSP": self._isis,
            "Automation Stitch": self._automation_stitch,
            "IoC / Threat feed": lambda: self._ioc_threat_feed(src),
            "Cloud SDN connector": self._cloud_sdn,
            "BFD neighbor": lambda: self._bfd(peer),
            "SAML SSO / admin login": lambda: self._saml_sso(src),
        }
        fn = dispatch.get(name)
        return fn() if fn else "# select a recipe"
