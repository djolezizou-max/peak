#!/bin/zsh
# Weekly content-RESEARCH runner with per-attempt timeout + retry.
# Invoked by launchd (com.peakinterval.content-research). Mirrors
# run_content_pipeline.sh so a single transient Claude CLI error
# ("An unknown error occurred (Unexpected)") no longer fails the whole run.
#
# Behavior:
#   - Up to $MAX_ATTEMPTS tries of `claude ... /content-pipeline research`
#   - Each attempt capped at $ATTEMPT_TIMEOUT seconds (no `timeout` binary on macOS)
#   - Transient errors are retried
#   - OAuth expiry is NOT retried: sends a distinct "re-auth needed" alert and stops
#   - Only sends the generic FAILED alert after all attempts are exhausted

# Repo root, derived from this script's own location, so the checkout the
# launchd job runs from (outside ~/Documents, which TCC hides from launchd)
# and a manual run from anywhere both resolve correctly.
PEAK_DIR="${0:A:h:h}"
CLAUDE_BIN="/Users/djordjejankovicmacmini/.local/bin/claude"
LOG="$PEAK_DIR/logs/content-research.log"
NOTIFY_CMD="/Users/djordjejankovicmacmini/QuestSpark/logs/qsnotify.cmd"
NOTIFY_APP="/Users/djordjejankovicmacmini/Applications/QSNotify.app"

MAX_ATTEMPTS=3
ATTEMPT_TIMEOUT=1200   # 20 min per attempt
BACKOFF=30             # seconds between attempts

notify() {
  # $1 = message
  printf "send|%s" "$1" > "$NOTIFY_CMD"
  /usr/bin/open -W -a "$NOTIFY_APP"
}

# Run "$@" with a hard timeout of $1 seconds. Returns the command's exit code,
# or 124 if it was killed for exceeding the timeout.
run_with_timeout() {
  local secs=$1; shift
  local flag; flag="$(mktemp -t cr-timeout.XXXXXX)"; rm -f "$flag"
  "$@" &
  local cmd_pid=$!
  ( sleep "$secs"; : > "$flag"; kill -TERM "$cmd_pid" 2>/dev/null; sleep 5; kill -KILL "$cmd_pid" 2>/dev/null ) &
  local watcher=$!
  wait "$cmd_pid" 2>/dev/null
  local rc=$?
  kill "$watcher" 2>/dev/null
  wait "$watcher" 2>/dev/null
  if [ -f "$flag" ]; then rc=124; fi
  rm -f "$flag"
  return $rc
}

cd "$PEAK_DIR" || { echo "=== run $(date) ===" >> "$LOG"; echo "FATAL cannot cd to $PEAK_DIR" >> "$LOG"; notify "Peak Interval weekly research job FAILED: cannot cd to peak dir"; exit 1; }

echo "=== run $(date) ===" >> "$LOG"

attempt=1
rc=1
while [ $attempt -le $MAX_ATTEMPTS ]; do
  tmp_out="$(mktemp -t content-research.XXXXXX)"
  [ $attempt -gt 1 ] && echo "--- retry attempt $attempt of $MAX_ATTEMPTS $(date) ---" >> "$LOG"

  run_with_timeout "$ATTEMPT_TIMEOUT" "$CLAUDE_BIN" --dangerously-skip-permissions -p "/content-pipeline research" > "$tmp_out" 2>&1
  rc=$?

  cat "$tmp_out" >> "$LOG"

  # OAuth expiry: retrying won't help — alert and stop.
  if grep -qi "OAuth session expired" "$tmp_out"; then
    echo "OAUTH-EXPIRED — stopping, re-auth required $(date)" >> "$LOG"
    rm -f "$tmp_out"
    notify "Peak Interval weekly research job needs RE-AUTH: Claude OAuth session expired. Run claude login, then re-run /content-pipeline research."
    exit 1
  fi

  rm -f "$tmp_out"

  if [ $rc -eq 0 ]; then
    break
  fi

  if [ $rc -eq 124 ]; then
    echo "TIMEOUT attempt $attempt after ${ATTEMPT_TIMEOUT}s $(date)" >> "$LOG"
  else
    echo "attempt $attempt failed exit=$rc $(date)" >> "$LOG"
  fi

  attempt=$((attempt + 1))
  [ $attempt -le $MAX_ATTEMPTS ] && sleep $BACKOFF
done

if [ $rc -ne 0 ]; then
  echo "FAILED exit=$rc after $MAX_ATTEMPTS attempts $(date)" >> "$LOG"
  notify "Peak Interval weekly research job FAILED (exit $rc) after $MAX_ATTEMPTS attempts - check Documents/peak/logs/content-research.log"
  exit 1
fi

exit 0
