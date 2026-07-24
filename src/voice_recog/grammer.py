"""Parse restricted Callie voice commands."""

from __future__ import annotations

import re
from dataclasses import dataclass

from .number_parser import parse_talkgroup


@dataclass(frozen=True)
class ParsedCommand:
    name: str
    dtmf: str
    talkgroup: str | None = None


CONNECT_PATTERNS = (
    re.compile(
        r"^(?:callie[\s,]*)?connect(?:\s+to)?\s+talk\s*group\s+(.+)$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^(?:callie[\s,]*)?select\s+talk\s*group\s+(.+)$",
        re.IGNORECASE,
    ),
)


def normalise_phrase(phrase: str) -> str:
    phrase = phrase.strip()
    phrase = re.sub(r"\s+", " ", phrase)
    return phrase


def parse_command(phrase: str) -> ParsedCommand:
    """
    Translate a restricted spoken instruction into SvxLink DTMF.

    Example:
        Callie, connect to talkgroup 23561
        becomes:
        9123561
    """
    normalised = normalise_phrase(phrase)

    if not normalised:
        raise ValueError("No command was supplied")

    for pattern in CONNECT_PATTERNS:
        match = pattern.fullmatch(normalised)

        if match:
            talkgroup = parse_talkgroup(match.group(1))

            return ParsedCommand(
                name="connect_talkgroup",
                talkgroup=talkgroup,
                dtmf=f"91{talkgroup}",
            )

    raise ValueError("Command not understood")