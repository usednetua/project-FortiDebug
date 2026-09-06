"""Headless smoke tests for Recipe R6 + session/flow VDOM helpers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.fortios_version import FortiOSVersion
from ui.tabs.recipe_impl import RecipeImplMixin
from ui.tabs.recipe_extra import RecipeExtraMixin
from ui.tabs.recipe_r6 import RecipeR6Mixin


class _Harness(RecipeR6Mixin, RecipeExtraMixin, RecipeImplMixin):
    """No GUI — only mixin methods."""


def test_session_block_with_vd():
    h = _Harness()
    lines = h._session_block("10.0.0.1", "8.8.8.8", "443", vd="0")
    assert "diagnose sys session filter vd 0" in lines
    assert "diagnose sys session filter src 10.0.0.1" in lines


def test_flow_block_with_vd():
    h = _Harness()
    lines = h._flow_block("1.1.1.1", "2.2.2.2", "80", vd="1")
    assert any("flow filter vd 1" in x for x in lines)


def test_advpn_contains_ike_and_sdwan():
    h = _Harness()
    out = h._advpn(FortiOSVersion.V7_4, "HUB1", "wan1", "10.1.1.1", "10.2.2.2")
    assert "diagnose vpn ike gateway list" in out
    assert "diagnose sys sdwan" in out
    assert "advpn" in out
    assert "diagnose debug application ike -1" in out


def test_sip_default_port():
    h = _Harness()
    out = h._sip_voip("10.0.0.5", "10.0.0.6", "", "any")
    assert "5060" in out
    assert "diagnose debug application sip -1" in out


def test_app_control_7():
    h = _Harness()
    out = h._app_control(FortiOSVersion.V7_4, "10.0.0.1", "")
    assert "internet-service-app-ctrl-list" in out


def test_email_file_transparent_modem():
    h = _Harness()
    assert "emailfilter" in h._email_filter("1.1.1.1", "")
    assert "dlp" in h._file_dlp("", "")
    assert "brctl" in h._transparent_bridge("port1")
    assert "modem" in h._modem_lte("wwan").lower()


def test_first_steps_vd_banner():
    h = _Harness()
    out = h._first_steps("10.0.0.1", "8.8.8.8", "", vd="0")
    assert "VDOM context: 0" in out
    assert "session filter vd 0" in out
