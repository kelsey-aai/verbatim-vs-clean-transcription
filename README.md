# Verbatim vs clean transcription with AssemblyAI-STT-3.7

Companion code for [Verbatim vs clean transcription: controlling fillers, false starts and number formatting](https://www.assemblyai.com/blog/verbatim-transcription-api).

Pre-recorded transcription with AssemblyAI-STT-3.7 (`assemblyai-stt-3-7`) gives you two independent switches:

- `disfluencies`: `true` keeps fillers ("um", "uh"), repetitions, stutters, false starts and informal contractions ("gonna"). `false` removes them.
- `format_text`: `true` writes numbers, currency, dates, emails and URLs in written form ("$12.50", "415-555-0132"). `false` returns them as spoken ("twelve fifty").

On AssemblyAI-STT-3.7 both default to `true`. Universal-3.5 Pro, Universal-3 Pro and Universal-2 remove disfluencies by default, so these scripts always set both flags explicitly.

| Style | `disfluencies` | `format_text` | Typical use |
| --- | --- | --- | --- |
| `verbatim` | `true` | `true` | Legal records, research interviews, edit-by-transcript tools |
| `clean` | `false` | `true` | Summaries, search, meeting notes, most captions |
| `strict` | `true` | `false` | Matching a strict-verbatim human reference, WER evaluation |
| `clean-spoken` | `false` | `false` | Pipelines that parse spoken numbers themselves |

| Script | What it shows |
| --- | --- |
| `transcribe.py` | One file in the style you pick, with optional `.srt` captions |
| `compare_styles.py` | The same file in all four styles, run in parallel |
| `filler_report.py` | Filler and repetition counts with timestamps from a verbatim transcript |
| `curl_example.sh` | A clean transcript with curl and jq |

## Requirements

- Python 3.9+
- An AssemblyAI API key ([sign up free](https://www.assemblyai.com/dashboard/signup))
- For the curl example: `curl` and `jq`

## Setup

```bash
git clone https://github.com/kelsey-aai/verbatim-vs-clean-transcription.git
cd verbatim-vs-clean-transcription
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then paste your API key into .env
```

## Run

```bash
python transcribe.py                                  # verbatim, docs sample file
python transcribe.py path/to/meeting.mp3 --style clean
python transcribe.py path/to/video.mp4 --style clean --srt
python compare_styles.py path/to/interview.m4a
python filler_report.py path/to/interview.m4a
ASSEMBLYAI_API_KEY=your_key ./curl_example.sh
```

Output files go to `out/`. Each script exits with a clear message if `ASSEMBLYAI_API_KEY` is not set.

## Notes

- `redact_pii` requires `format_text: true`. `build_config()` raises an error if you combine PII redaction with the `strict` or `clean-spoken` styles.
- If `speech_models` includes `assemblyai-stt-3-7` anywhere in the list, `disfluencies` defaults to `true` for the whole request, even when Universal-2 transcribes the audio. On Universal-2, `disfluencies: true` keeps filler words only.
- Verbatim and spoken-form output are supported in all 32 AssemblyAI-STT-3.7 languages.
- These switches are pre-recorded only. Realtime models return formatted finals, and their verbatim behavior isn't configurable.
- `compare_styles.py` runs four transcriptions, so it's billed as four.

## Pricing

AssemblyAI-STT-3.7 is $0.21/hr. `disfluencies` and `format_text` are request parameters, not add-ons. New accounts get $50 in free credits for the speech APIs. See [pricing](https://www.assemblyai.com/pricing).

## Docs

- [Verbatim (disfluencies)](https://www.assemblyai.com/docs/pre-recorded-audio/include-filler-words)
- [Formatting (format_text)](https://www.assemblyai.com/docs/pre-recorded-audio/formatting)
- [AssemblyAI-STT-3.7 migration guide](https://www.assemblyai.com/docs/pre-recorded-audio/assemblyai-stt-3-7-migration-guide)
- [Export SRT and VTT captions](https://www.assemblyai.com/docs/pre-recorded-audio/export-transcripts-as-srt-vtt-or-text)
