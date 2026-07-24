"""Convert spoken talkgroup digits into a numeric string."""

from __future__ import annotations

import re


DIGIT_WORDS = {
    "zero": "0",
    "oh": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def parse_talkgroup(value: str) -> str:
    """
    Convert a recognised talkgroup value into digits.

    Accepted examples:
        "23561"
        "2 3 5 6 1"
        "two three five six one"
        "two 3 five 6 one"
    """
    cleaned = value.lower().strip()
    cleaned = re.sub(r"[^a-z0-9\s]", " ", cleaned)
    tokens = cleaned.split()

    if not tokens:
        raise ValueError("No talkgroup number was supplied")

    digits: list[str] = []

    for token in tokens:
        if token.isdigit():
            digits.append(token)
        elif token in DIGIT_WORDS:
            digits.append(DIGIT_WORDS[token])
        else:
            raise ValueError(f"Unrecognised number word: {token}")

    talkgroup = "".join(digits)

    if not talkgroup.isdigit():
        raise ValueError("Talkgroup must contain digits only")

    if not 1 <= len(talkgroup) <= 9:
        raise ValueError("Talkgroup length must be between 1 and 9 digits")

    return talkgroup