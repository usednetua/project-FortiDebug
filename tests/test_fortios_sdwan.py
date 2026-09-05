"""SD-WAN / IKE version syntax checks."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.fortios_version import (
    FortiOSVersion,
    ike_log_filter_base,
    ike_filter_remote_peer,
    ike_filter_local_peer,
    sdwan_diag_prefix,
    sdwan_service_cmd,
    sdwan_cmd,
)


def test_ike_pre_74():
    v = FortiOSVersion.V7_2
    assert ike_log_filter_base(v) == "diagnose vpn ike log-filter"
    assert "dst-addr4" in ike_filter_remote_peer(v, "1.2.3.4")
    assert "src-addr4" in ike_filter_local_peer(v, "10.0.0.1")


def test_ike_74_plus():
    v = FortiOSVersion.V7_4
    assert ike_log_filter_base(v) == "diagnose vpn ike log filter"
    assert "rem-addr4" in ike_filter_remote_peer(v, "1.2.3.4")
    assert "loc-addr4" in ike_filter_local_peer(v, "10.0.0.1")


def test_ike_80():
    v = FortiOSVersion.V8_0
    assert ike_log_filter_base(v) == "diagnose vpn ike log filter"


def test_sdwan_6x():
    for v in (FortiOSVersion.V6_0, FortiOSVersion.V6_2, FortiOSVersion.V6_4):
        assert sdwan_diag_prefix(v) == "diagnose sys virtual-wan-link"
        assert sdwan_cmd(v, "member") == "diagnose sys virtual-wan-link member"


def test_sdwan_70():
    v = FortiOSVersion.V7_0
    assert sdwan_diag_prefix(v) == "diagnose sys sdwan"
    assert sdwan_service_cmd(v) == "diagnose sys sdwan service"


def test_sdwan_74_service4():
    for v in (FortiOSVersion.V7_4, FortiOSVersion.V7_6, FortiOSVersion.V8_0):
        assert sdwan_service_cmd(v) == "diagnose sys sdwan service4"
