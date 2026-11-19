"""Transcribe one file in the style you pick.

Usage:
    python transcribe.py                                   # verbatim, docs sample
    python transcribe.py meeting.mp3 --style clean
    python transcribe.py deposition.wav --style strict
    python transcribe.py video.mp4 --style clean --srt     # also write captions
"""

import argparse

from assemblyai.prerecorded.v2 import Transcriber

from _common import DEFAULT_AUDIO, STYLES, build_config, get_api_key, out_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("audio", nargs="?", default=DEFAULT_AUDIO, help="URL or local file")
    parser.add_argument("--style", choices=STYLES, default="verbatim")
    parser.add_argument("--srt", action="store_true", help="also export an .srt caption file")
    args = parser.parse_args()

    transcriber = Transcriber(api_key=get_api_key())
    transcript = transcriber.transcribe(args.audio, build_config(args.style))

    if transcript.status == "error":
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    print(f"Model used: {transcript.speech_model_used}")
    print(f"Style: {args.style} {STYLES[args.style]}\n")
    print(transcript.text)

    txt_path = out_dir() / f"{transcript.id}-{args.style}.txt"
    txt_path.write_text(transcript.text or "")
    print(f"\nSaved {txt_path}")

    if args.srt:
        srt_path = out_dir() / f"{transcript.id}-{args.style}.srt"
        srt_path.write_text(transcript.export_subtitles_srt(chars_per_caption=32))
        print(f"Saved {srt_path}")


if __name__ == "__main__":
    main()
