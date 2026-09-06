"""Tests for core.vdom."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.vdom import (
    wrap_vdom_context,
    resolve_vd_index,
    vdom_banner,
    vdom_enter,
    should_wrap_vdom,
    normalize_vdom_map,
    vdom_map_to_text,
)


def test_wrap_off_noop():
    body = "get system status"
    assert wrap_vdom_context(body, False, "root") == body


def test_wrap_on():
    body = "get system status"
    out = wrap_vdom_context(body, True, "vd-LAN")
    assert "config vdom" in out
    assert "edit vd-LAN" in out


def test_wrap_skipped_for_ha_tab():
    body = "get system ha status"
    out = wrap_vdom_context(body, True, "root", tab_key="ha")
    assert out == body


def test_should_wrap_matrix():
    assert should_wrap_vdom(True, tab_key="ha") is False
    assert should_wrap_vdom(True, recipe_name="High CPU") is False
    assert should_wrap_vdom(True, recipe_name="Traffic not passing") is True


def test_normalize_map_text():
    m = normalize_vdom_map("root=0\nvd-LAN=1\n# comment\nvd-DMZ:2\n")
    assert m["root"] == "0"
    assert m["vd-lan"] == "1"
    assert m["vd-dmz"] == "2"


def test_resolve_with_map():
    m = {"vd-lan": "3", "root": "0"}
    assert resolve_vd_index(True, "vd-LAN", "", m) == "3"
    assert resolve_vd_index(True, "root", "", m) == "0"
    assert resolve_vd_index(True, "unknown", "", m) == ""
    assert resolve_vd_index(True, "root", "9", m) == "9"  # explicit wins


def test_map_to_text_roundtrip():
    m = normalize_vdom_map("root=0\nvd-lan=1\n")
    text = vdom_map_to_text(m)
    assert "root=0" in text
    assert normalize_vdom_map(text)["vd-lan"] == "1"


def test_banner_global():
    assert "GLOBAL" in vdom_banner(True, "root", wrapped=False)
