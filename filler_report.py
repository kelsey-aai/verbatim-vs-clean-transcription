"""Count fillers and repeated words in a verbatim transcript.

Useful for research coding, interview QA and speaking-coach features, where
the hesitations are the data. Requests a verbatim transcript (disfluencies on)
and counts from the word list, so each hit has a timestamp.

Usage:
    python filler_report.py interview.mp3
"""

import string
import sys
from collections import Counter

from assemblyai.prerecorded.v2 import Transcriber

from _common import DEFAULT_AUDIO, build_config, get_api_key

# Lexical fillers. Extend for your domain and languages.
FILLERS = {"um", "umm", "uh", "uhh", "er", "erm", "ah", "hmm", "mm"}


def normalize(word: str) -> str:
    return word.lower().strip(string.punctuation + "—–")


def main() -> None:
    audio = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_AUDIO

    transcriber = Transcriber(api_key=get_api_key())
    transcript = transcriber.transcribe(audio, build_config("verbatim"))

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    words = transcript.words or []
    tokens = [normalize(w.text) for w in words]

    fillers = Counter(t for t in tokens if t in FILLERS)
    repeats = [
        (words[i].start, tokens[i])
        for i in range(1, len(tokens))
        if tokens[i] and tokens[i] == tokens[i - 1] and tokens[i] not in FILLERS
    ]

    total = len(tokens) or 1
    print(f"Words: {len(tokens)}")
    print(f"Fillers: {sum(fillers.values())} ({100 * sum(fillers.values()) / total:.1f} per 100 words)")
    for filler, count in fillers.most_common():
        print(f"  {filler}: {count}")

    print(f"Immediate repetitions: {len(repeats)}")
    for start_ms, token in repeats[:10]:
        # word timestamps are in milliseconds
        print(f"  {start_ms / 1000:7.2f}s  {token} {token}")


if __name__ == "__main__":
    main()
