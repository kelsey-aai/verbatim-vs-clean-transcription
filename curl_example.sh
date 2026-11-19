#!/usr/bin/env bash
# Clean transcript (fillers removed, numbers written) with curl and jq.
# Flip DISFLUENCIES / FORMAT_TEXT to get the other styles.
#
# Usage: ASSEMBLYAI_API_KEY=your_key ./curl_example.sh [audio_url]
set -euo pipefail

: "${ASSEMBLYAI_API_KEY:?Set ASSEMBLYAI_API_KEY first}"
AUDIO_URL="${1:-https://assembly.ai/wildfires.mp3}"
DISFLUENCIES=false
FORMAT_TEXT=true

BODY=$(jq -n \
  --arg url "$AUDIO_URL" \
  --argjson disfluencies "$DISFLUENCIES" \
  --argjson format_text "$FORMAT_TEXT" \
  '{audio_url: $url, speech_models: ["assemblyai-stt-3-7"], language_detection: true,
    disfluencies: $disfluencies, format_text: $format_text}')

ID=$(curl -s https://api.assemblyai.com/v2/transcript \
  -H "authorization: $ASSEMBLYAI_API_KEY" \
  -H "content-type: application/json" \
  -d "$BODY" | jq -r '.id')
echo "Submitted $ID"

while true; do
  RESULT=$(curl -s "https://api.assemblyai.com/v2/transcript/$ID" \
    -H "authorization: $ASSEMBLYAI_API_KEY")
  STATUS=$(echo "$RESULT" | jq -r '.status')
  case "$STATUS" in
    completed) echo "$RESULT" | jq -r '.text'; break ;;
    error) echo "$RESULT" | jq -r '.error' >&2; exit 1 ;;
    *) sleep 3 ;;
  esac
done
