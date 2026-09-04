"""Tests for core.safety."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.safety import preamble, epilogue


def test_preamble_default():
    lines = preamble(reset=True, clear_flow_filter=True, timestamps=True)
    assert "diagnose debug reset" in lines
    assert "diagnose debug flow filter clear" in lines
    assert "diagnose debug console timestamp enable" in lines


def test_preamble_minimal():
    lines = preamble(reset=False, clear_flow_filter=False, timestamps=False)
    assert lines == []


def test_epilogue():
    lines = epilogue(stop=True)
    assert "diagnose debug disable" in lines
    assert "diagnose debug reset" in lines
    assert epilogue(stop=False) == []
