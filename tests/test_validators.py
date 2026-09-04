"""Tests for core.validators."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.validators import is_valid_ip, is_valid_port, is_valid_policy_id


def test_ipv4_ok():
    assert is_valid_ip("10.1.1.10")
    assert is_valid_ip("192.168.0.1")
    assert is_valid_ip("")


def test_ipv4_bad():
    assert not is_valid_ip("10.1.1.256")
    assert not is_valid_ip("abc")


def test_ipv6_ok():
    assert is_valid_ip("2001:db8::1")
    assert is_valid_ip("::1")


def test_port():
    assert is_valid_port("80")
    assert is_valid_port("65535")
    assert is_valid_port("")
    assert not is_valid_port("0")
    assert not is_valid_port("70000")


def test_policy_id():
    assert is_valid_policy_id("12")
    assert is_valid_policy_id("")
    assert not is_valid_policy_id("x")
