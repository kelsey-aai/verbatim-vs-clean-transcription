"""Shared setup for the verbatim vs clean transcription examples."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from assemblyai.prerecorded.v2 import TranscriptionConfig

# Pre-recorded flagship model. disfluencies and format_text both default to
# true on it, so these examples always set them explicitly.
STT_3_7 = "assemblyai-stt-3-7"

# Short public sample from the AssemblyAI docs
DEFAULT_AUDIO = "https://assembly.ai/wildfires.mp3"

# The four transcript styles you can get from two booleans.
STYLES = {
    # Fillers, repetitions and false starts kept; numbers written ("$1,250").
    # This is what AssemblyAI-STT-3.7 returns when you set nothing.
    "verbatim": {"disfluencies": True, "format_text": True},
    # Fillers removed; numbers written. Readable prose for summaries and search.
    "clean": {"disfluencies": False, "format_text": True},
    # Fillers kept; numbers, dates and emails spelled out as spoken.
    # The closest match to a strict-verbatim human transcript.
    "strict": {"disfluencies": True, "format_text": False},
    # Fillers removed; spoken-form numbers. Useful when your own code
    # normalizes numbers downstream.
    "clean-spoken": {"disfluencies": False, "format_text": False},
}


def get_api_key() -> str:
    """Read ASSEMBLYAI_API_KEY from the environment or a local .env file."""
    load_dotenv()
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        sys.exit(
            "ASSEMBLYAI_API_KEY is not set. Copy .env.example to .env and add "
            "your key from the AssemblyAI dashboard."
        )
    return api_key


def build_config(style: str, **extra) -> TranscriptionConfig:
    """Build a TranscriptionConfig for one of the four styles.

    Both flags are always sent, so the output doesn't change if your
    speech_models list or the account's default model changes.
    """
    if style not in STYLES:
        raise ValueError(f"Unknown style {style!r}. Pick one of: {', '.join(STYLES)}")

    flags = STYLES[style]

    # PII redaction runs on formatted text, so the API requires format_text=True.
    if extra.get("redact_pii") and not flags["format_text"]:
        raise ValueError(
            f"redact_pii requires format_text=True; the {style!r} style turns it off."
        )

    return TranscriptionConfig(
        speech_models=[STT_3_7],
        language_detection=True,
        **flags,
        **extra,
    )


def out_dir() -> Path:
    path = Path("out")
    path.mkdir(exist_ok=True)
    return path
