"""Ensure recipe bodies are non-empty and not stub placeholders."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.fortios_version import DEFAULT_VERSION
from ui.tabs.recipe_impl import RecipeImplMixin
from ui.tabs.recipe_extra import RecipeExtraMixin
from ui.tabs.recipe_r6 import RecipeR6Mixin
from ui.tabs.recipe_r8 import RecipeR8Mixin
from ui.tabs.recipe_r9 import RecipeR9Mixin
from ui.tabs.recipe_r10 import RecipeR10Mixin
from ui.tabs.recipe_r11 import RecipeR11Mixin


class _H(
    RecipeR11Mixin,
    RecipeR10Mixin,
    RecipeR9Mixin,
    RecipeR8Mixin,
    RecipeR6Mixin,
    RecipeExtraMixin,
    RecipeImplMixin,
):
    pass


def _assert_body(body: str):
    assert "pending restore" not in body, body[:120]
    assert body.strip(), "empty recipe body"
    assert body.lstrip().startswith("#"), body[:80]


def test_no_pending_restore_in_core_methods():
    h = _H()
    version = DEFAULT_VERSION
    samples = [
        h._dialup_ipsec(version, "1.2.3.4", "10.0.0.1"),
        h._ssl_login_fail("10.0.0.2"),
        h._policy_nat("10.0.0.1", "8.8.8.8", "443"),
        h._ospf(),
        h._bgp("192.0.2.1"),
        h._npu(),
        h._advpn(version, "1.2.3.4", "wan1", "10.0.0.1", "10.0.0.2"),
        h._rip(),
        h._ssl_web_mode("10.0.0.5"),
        h._isis(),
        h._automation_stitch(),
        h._ioc_threat_feed("10.0.0.9"),
        h._cloud_sdn(),
        h._bfd("192.0.2.8"),
        h._saml_sso("10.1.1.10"),
    ]
    for body in samples:
        _assert_body(body)
