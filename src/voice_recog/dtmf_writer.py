"""Write validated commands to an SvxLink DTMF control path."""

from __future__ import annotations

import re
from pathlib import Path


VALID_DTMF = re.compile(r"^[0-9A-D*#]+$", re.IGNORECASE)


def send_dtmf(command: str, control_path: str) -> None:
    """Send one command to an SvxLink DTMF control file or FIFO."""
    if not VALID_DTMF.fullmatch(command):
        raise ValueError(f"Invalid DTMF command: {command!r}")

    path = Path(control_path)

    if not path.exists():
        raise FileNotFoundError(f"DTMF control path does not exist: {path}")

    with path.open("w", encoding="ascii") as control:
        control.write(command)
        control.write("\n")
        control.flush()