#!/bin/zsh
# Daily Peak Interval blog publisher. Uses OpenClaw's configured OpenAI OAuth
# instead of the separate Claude CLI, whose weekly quota can block publishing.
set -euo pipefail

PEAK_DIR="${0:A:h:h}"
PROMPT_FILE="$PEAK_DIR/Scripts/marketing/openclaw_daily_publish_prompt.txt"

if [[ ! -f "$PROMPT_FILE" ]]; then
  echo "Missing prompt file: $PROMPT_FILE" >&2
  exit 1
fi

cd "$PEAK_DIR"
/opt/homebrew/bin/openclaw agent \
  --to +17573193487 \
  --message "$(<"$PROMPT_FILE")" \
  --model openai/gpt-5.6-terra \
  --timeout 1800 \
  --thinking high
