#!/bin/bash
set -e

# Configure NETEM if environment variables are set
if [ -n "$NETEM_DELAY_MS" ] || [ -n "$NETEM_LOSS_PCT" ] || [ -n "$NETEM_JITTER_MS" ]; then
  DELAY="${NETEM_DELAY_MS:-0}ms"
  JITTER="${NETEM_JITTER_MS:-0}ms"
  LOSS="${NETEM_LOSS_PCT:-0}%"
  echo "[netem] Applying: delay $DELAY $JITTER loss $LOSS"
  # remove existing qdisc if any
  tc qdisc del dev eth0 root 2>/dev/null || true
  tc qdisc add dev eth0 root netem delay $DELAY $JITTER loss $LOSS
fi

exec python /app/sensor.py
