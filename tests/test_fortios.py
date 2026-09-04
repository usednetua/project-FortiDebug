"""Tests for core.fortios_version."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.fortios_version import (
    FortiOSVersion,
    parse_version,
    uses_new_ike_filter_syntax,
    ike_log_filter_base,
    ike_filter_remote_peer,
    ike_filter_name,
    ike_filter_interface,
)


def test_parse():
    assert parse_version("7.4.x") == FortiOSVersion.V7_4
    assert parse_version("6.2") == FortiOSVersion.V6_2


def test_syntax_split():
    assert uses_new_ike_filter_syntax(FortiOSVersion.V7_4)
    assert not uses_new_ike_filter_syntax(FortiOSVersion.V7_2)


def test_filter_commands():
    old = FortiOSVersion.V7_2
    new = FortiOSVersion.V7_4
    assert "log-filter" in ike_log_filter_base(old)
    assert "log filter" in ike_log_filter_base(new)
    assert "dst-addr4" in ike_filter_remote_peer(old, "1.1.1.1")
    assert "rem-addr4" in ike_filter_remote_peer(new, "1.1.1.1")
    assert "name vpn1" in ike_filter_name(new, "vpn1")
    assert "ifindex" in ike_filter_interface(new, "0")
