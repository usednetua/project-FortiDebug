"""Tests for core.cmd_builders."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.cmd_builders import build_network_commands, build_policy_lookup
from core.fortios_version import FortiOSVersion


def test_network_arp():
    text = build_network_commands(arp_get=True, arp_diag=True)
    assert "get system arp" in text
    assert "diagnose ip arp list" in text


def test_network_nic_and_lacp():
    text = build_network_commands(
        nic_iface="wan1",
        agg_list=True,
        agg_name="lacp1",
        nd6=True,
    )
    assert "get hardware nic wan1" in text
    assert "diagnose netlink aggregate list" in text
    assert "diagnose netlink aggregate name lacp1" in text
    assert "neighbor-cache" in text


def test_network_empty():
    assert build_network_commands() == "# select options"


def test_policy_lookup_base():
    cmd = build_policy_lookup("10.1.1.10", "12345", "8.8.8.8", "443", "6", "port1")
    assert cmd == (
        "diagnose firewall iprope lookup 10.1.1.10 12345 8.8.8.8 443 6 port1"
    )


def test_policy_lookup_74_extended():
    cmd = build_policy_lookup(
        "10.1.1.10",
        "12345",
        "8.8.8.8",
        "443",
        "6",
        "port1",
        version=FortiOSVersion.V7_4,
        pol_type="policy",
        auth_type="local",
        user_or_group="alice",
    )
    assert cmd.endswith("policy local alice")


def test_policy_lookup_72_ignores_extra():
    cmd = build_policy_lookup(
        "10.1.1.10",
        "12345",
        "8.8.8.8",
        "443",
        "6",
        "port1",
        version=FortiOSVersion.V7_2,
        pol_type="policy",
        auth_type="local",
        user_or_group="alice",
    )
    assert cmd == (
        "diagnose firewall iprope lookup 10.1.1.10 12345 8.8.8.8 443 6 port1"
    )
