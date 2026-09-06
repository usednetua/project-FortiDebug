"""Ensure restored recipes no longer emit stub placeholders."""

import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.fortios_version import DEFAULT_VERSION
from ui.tabs.recipe_impl import RecipeImplMixin
from ui.tabs.recipe_extra import RecipeExtraMixin
from ui.tabs.recipe_r6 import RecipeR6Mixin


class _H(RecipeR6Mixin, RecipeExtraMixin, RecipeImplMixin):
    pass


def test_no_pending_restore_in_core_methods():
    h = _H()
    version = DEFAULT_VERSION
    samples = [
        h._dialup_ipsec(version, "1.2.3.4", "10.0.0.1"),
        h._ssl_login_fail("10.0.0.2"),
        h._policy_nat("10.0.0.1", "8.8.8.8", "443"),
        h._vip("10.0.0.1", "1.2.3.4", "443", "wan1"),
        h._local_in("10.0.0.1", "wan1"),
        h._ospf(),
        h._bgp("192.0.2.1"),
        h._routing("8.8.8.8"),
        h._dhcp("lan"),
        h._auth_fsso(),
        h._dns("10.0.0.1", "8.8.8.8"),
        h._webfilter("10.0.0.1"),
        h._ips_utm("10.0.0.1", "8.8.8.8"),
        h._explicit_proxy("10.0.0.1"),
        h._wireless(),
        h._lacp("agg1"),
        h._interface("wan1"),
        h._npu(),
        h._certificate(),
        h._fortiguard(),
        h._log_disk(),
        h._ntp(),
        h._ipv6("2001:db8::1", "2001:db8::2"),
        h._multicast("lan"),
    ]
    for body in samples:
        assert "pending restore" not in body, body[:120]
        assert body.strip(), "empty recipe body"
        assert body.lstrip().startswith("#"), body[:80]
