"""Simple input validators."""

import re

IPV4_RE = re.compile(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)


def is_valid_ip(value: str) -> bool:
    value = value.strip()
    if not value:
        return True  # empty is allowed
    return bool(IPV4_RE.match(value))


def is_valid_port(value: str) -> bool:
    value = value.strip()
    if not value:
        return True
    try:
        p = int(value)
        return 1 <= p <= 65535
    except ValueError:
        return False
