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
)


def test_wrap_off_noop():
    body = "get system status"
    assert wrap_vdom_context(body, False, "root") == body


def test_wrap_on():
    body = "get system status"
    out = wrap_vdom_context(body, True, "vd-LAN")
    assert "config vdom" in out
    assert "edit vd-LAN" in out
    assert "get system status" in out
    assert out.strip().endswith("end")


def test_wrap_skipped_for_ha_tab():
    body = "get system ha status"
    out = wrap_vdom_context(body, True, "root", tab_key="ha")
    assert out == body
    assert "config vdom" not in out


def test_wrap_skipped_for_global_recipe():
    body = "diagnose sys ha checksum cluster"
    out = wrap_vdom_context(body, True, "root", recipe_name="HA out-of-sync")
    assert out == body


def test_should_wrap_matrix():
    assert should_wrap_vdom(False) is False
    assert should_wrap_vdom(True, tab_key="sessions") is True
    assert should_wrap_vdom(True, tab_key="ha") is False
    assert should_wrap_vdom(True, tab_key="hardware") is False
    assert should_wrap_vdom(True, recipe_name="High CPU") is False
    assert should_wrap_vdom(True, recipe_name="Traffic not passing") is True


def test_resolve_vd():
    assert resolve_vd_index(False, "root", "") == ""
    assert resolve_vd_index(True, "root", "") == "0"
    assert resolve_vd_index(True, "root", "3") == "3"
    assert resolve_vd_index(True, "2", "") == "2"
    assert resolve_vd_index(True, "vd-LAN", "") == ""


def test_banner_global():
    b = vdom_banner(True, "root", wrapped=False)
    assert "GLOBAL" in b


def test_enter_default_root():
    lines = vdom_enter("")
    assert any("edit root" in x for x in lines)
