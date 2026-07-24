import pytest

from voice_recog.grammar import parse_command


@pytest.mark.parametrize(
    "phrase",
    [
        "Callie, connect to talkgroup 23561",
        "Callie connect to talk group 23561",
        "connect to talkgroup two three five six one",
        "select talkgroup 23561",
    ],
)
def test_connect_talkgroup(phrase: str) -> None:
    result = parse_command(phrase)

    assert result.name == "connect_talkgroup"
    assert result.talkgroup == "23561"
    assert result.dtmf == "9123561"


def test_unknown_command() -> None:
    with pytest.raises(ValueError, match="Command not understood"):
        parse_command("Callie make the tea")