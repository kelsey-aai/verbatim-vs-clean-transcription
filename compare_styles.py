"""Run one recording through all four styles and print them side by side.

Usage:
    python compare_styles.py                   # docs sample
    python compare_styles.py interview.m4a     # local file or URL

A local file is uploaded once and the four jobs run in parallel.
Each job is billed as a separate transcription.
"""

import sys
from pathlib import Path

from assemblyai.prerecorded.v2 import Transcriber

from _common import DEFAULT_AUDIO, STYLES, build_config, get_api_key, out_dir


def main() -> None:
    audio = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_AUDIO
    transcriber = Transcriber(api_key=get_api_key())

    # Upload a local file once, then reuse the URL for every job
    if Path(audio).exists():
        audio = transcriber.upload_file(audio)

    # submit() returns right away, so the four jobs run at the same time
    jobs = {style: transcriber.submit(audio, build_config(style)) for style in STYLES}

    for style, job in jobs.items():
        transcript = job.wait_for_completion()
        print(f"=== {style}  {STYLES[style]}")
        if transcript.status == "error":
            print(f"failed: {transcript.error}\n")
            continue

        words = len(transcript.words or [])
        print(f"({words} words, model: {transcript.speech_model_used})")
        print(transcript.text, "\n")
        (out_dir() / f"{style}.txt").write_text(transcript.text or "")

    print(f"Saved each style to {out_dir()}/")


if __name__ == "__main__":
    main()
