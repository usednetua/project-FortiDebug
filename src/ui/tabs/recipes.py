"""Recipes / Workflows — incident playbooks for FortiGate debug."""

import customtkinter as ctk
from ui.tabs.base_tab import BaseTab
from core.fortios_version import (
    DEFAULT_VERSION,
    ike_log_filter_clear,
    ike_filter_remote_peer,
    ike_filter_name,
    sdwan_cmd,
    sdwan_service_cmd,
    version_banner,
)
from core.safety import preamble, epilogue
from ui.widgets.tooltip import tip


class RecipesTab(BaseTab):
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
    ]
