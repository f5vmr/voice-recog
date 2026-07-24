"""Basic live Vosk recognition test."""

from __future__ import annotations

import argparse
import json
import queue
import sys

import sounddevice as sd
from vosk import KaldiRecognizer, Model


SAMPLE_RATE = 48000
AUDIO_QUEUE: queue.Queue[bytes] = queue.Queue()


def audio_callback(indata, frames, time_info, status) -> None:
    if status:
        print(status, file=sys.stderr)

    AUDIO_QUEUE.put(bytes(indata))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="models/vosk-model-small-en-gb-0.15",
    )
    parser.add_argument(
        "--device",
        type=int,
        default=None,
        help="Input-device number shown by sounddevice",
    )
    args = parser.parse_args()

    model = Model(args.model)
    recogniser = KaldiRecognizer(model, SAMPLE_RATE)

    print("Listening. Press Ctrl-C to stop.")

    try:
        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=4000,
            device=args.device,
            dtype="int16",
            channels=1,
            callback=audio_callback,
        ):
            while True:
                audio = AUDIO_QUEUE.get()

                if recogniser.AcceptWaveform(audio):
                    result = json.loads(recogniser.Result())
                    text = result.get("text", "").strip()

                    if text:
                        print(f"FINAL:   {text}")
                else:
                    partial = json.loads(recogniser.PartialResult())
                    text = partial.get("partial", "").strip()

                    if text:
                        print(f"PARTIAL: {text}", end="\r", flush=True)

    except KeyboardInterrupt:
        print("\nStopped.")
        return 0
    except Exception as error:
        print(f"Recognition error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())