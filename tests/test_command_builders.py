"""Smoke tests for command generation helpers used by tabs."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.safety import preamble, epilogue
from core.fortios_version import FortiOSVersion, ike_log_filter_clear, ike_filter_remote_peer


def test_flow_like_block():
    lines = preamble(reset=True, clear_flow_filter=True, timestamps=True)
    lines.append("diagnose debug flow filter saddr 10.1.1.10")
    lines.append("diagnose debug flow show function-name enable")
    lines.append("diagnose debug flow show iprope enable")
    lines.append("diagnose debug enable")
    lines.append("diagnose debug flow trace start 100")
    lines.extend(epilogue(stop=True))
    text = "\n".join(lines)
    assert "diagnose debug reset" in text
    assert "filter clear" in text
    assert "iprope enable" in text
    assert "trace start 100" in text
    assert "debug disable" in text


def test_vpn_ike_block():
    v = FortiOSVersion.V7_4
    lines = preamble(reset=True, timestamps=True)
    lines.append(ike_log_filter_clear(v))
    lines.append(ike_filter_remote_peer(v, "203.0.113.1"))
    lines.append("diagnose debug application ike -1")
    lines.append("diagnose debug enable")
    lines.extend(epilogue(stop=True))
    text = "\n".join(lines)
    assert "log filter clear" in text
    assert "rem-addr4 203.0.113.1" in text
