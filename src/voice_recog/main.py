"""Initial command-line test program for voice_recog."""

from __future__ import annotations

import argparse
import sys

from .dtmf_writer import send_dtmf
from .grammar import parse_command


DEFAULT_CONTROL_PATH = "/dev/shm/repeater_dtmf_ctrl"


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Translate a Callie instruction into an SvxLink DTMF command"
    )

    parser.add_argument(
        "phrase",
        help='Command such as "Callie, connect to talkgroup 23561"',
    )

    parser.add_argument(
        "--control-path",
        default=DEFAULT_CONTROL_PATH,
        help=f"SvxLink DTMF control path; default: {DEFAULT_CONTROL_PATH}",
    )

    parser.add_argument(
        "--send",
        action="store_true",
        help="Write the generated command to SvxLink",
    )

    return parser


def main() -> int:
    args = build_argument_parser().parse_args()

    try:
        command = parse_command(args.phrase)
    except ValueError as error:
        print(f"NOT UNDERSTOOD: {error}", file=sys.stderr)
        return 2

    print(f"Command:   {command.name}")
    print(f"Talkgroup: {command.talkgroup}")
    print(f"DTMF:      {command.dtmf}")

    if not args.send:
        print("Dry run only; nothing sent to SvxLink")
        return 0

    try:
        send_dtmf(command.dtmf, args.control_path)
    except (OSError, ValueError) as error:
        print(f"OPERATION FAILED: {error}", file=sys.stderr)
        return 1

    print(f"Sent to:   {args.control_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())