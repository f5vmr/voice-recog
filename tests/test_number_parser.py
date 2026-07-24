import pytest

from voice_recog.number_parser import parse_talkgroup


@pytest.mark.parametrize(
    ("spoken", "expected"),
    [
        ("23561", "23561"),
        ("2 3 5 6 1", "23561"),
        ("two three five six one", "23561"),
        ("two 3 five 6 one", "23561"),
        ("oh nine five", "095"),
    ],
)
def test_parse_talkgroup(spoken: str, expected: str) -> None:
    assert parse_talkgroup(spoken) == expected


def test_reject_unknown_number_word() -> None:
    with pytest.raises(ValueError):
        parse_talkgroup("two potato five")