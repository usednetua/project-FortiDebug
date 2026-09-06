"""Tests for core.vdom."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.vdom import (
    wrap_vdom_context,
    resolve_vd_index,
    vdom_banner,
    vdom_enter,
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


def test_resolve_vd():
    assert resolve_vd_index(False, "root", "") == ""
    assert resolve_vd_index(True, "root", "") == "0"
    assert resolve_vd_index(True, "root", "3") == "3"
    assert resolve_vd_index(True, "2", "") == "2"
    assert resolve_vd_index(True, "vd-LAN", "") == ""  # name only → context edit


def test_banner():
    assert "off" in vdom_banner(False).lower()
    assert "on" in vdom_banner(True, "root").lower()


def test_enter_default_root():
    lines = vdom_enter("")
    assert any("edit root" in x for x in lines)
