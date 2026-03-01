"""
system_ops/log_translator.py
============================
Ubuntu systemd journal logs → internal JSON schema

Ubuntu's systemd journal already supports structured JSON output via:
    journalctl -o json --follow

The question is whether to use Ubuntu's schema directly or translate it.
Answer: translate. Ubuntu's schema is rich but noisy — 30+ fields per
entry, most irrelevant to the Executive Module. This service reads the
raw journal stream and produces the minimal, typed events the Executive
Module actually needs.

Two modes:
  - passthrough: Ubuntu JSON → internal schema (fast, lightweight)
  - enriched:    passthrough + metric extraction from message text
                 (e.g., parse "CPU temp 87°C" from kernel messages)

The internal schema is defined by foundation.json. Status codes map
Ubuntu's syslog PRIORITY (0-7) to our NORMAL/ALERT/WARNING/ERROR/FATAL.

This runs as a subprocess of System Ops, not the Executive Module.
The Executive Module reads the output stream; it does not call this directly.
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from typing import Iterator


# ─────────────────────────────────────────────────────────────────────────────
# Priority mapping: syslog levels → internal status codes
# Ubuntu PRIORITY is a string "0" through "7"
# ─────────────────────────────────────────────────────────────────────────────
PRIORITY_TO_STATUS = {
    "0": "FATAL",    # emerg
    "1": "FATAL",    # alert
    "2": "FATAL",    # crit
    "3": "ERROR",    # err
    "4": "WARNING",  # warning
    "5": "ALERT",    # notice  — not NORMAL; notice means "pay attention"
    "6": "NORMAL",   # info
    "7": "NORMAL",   # debug
}

# Source taxonomy — from foundation.json log_source_taxonomy
UNIT_TO_SOURCE = {
    "kernel":                   "kernel",
    "systemd-journald.service": "systemd",
    "systemd.service":          "systemd",
    "NetworkManager.service":   "network",
    "postgresql.service":       "database",
    "mongod.service":           "database",
}


# ─────────────────────────────────────────────────────────────────────────────
# Metric extractors
# These try to pull structured values from unstructured log messages.
# If Ubuntu eventually emits these as structured fields, remove the extractor.
# ─────────────────────────────────────────────────────────────────────────────
METRIC_EXTRACTORS = [
    # Kernel thermal: "CPU: Package temperature above threshold"
    # or: "thermal thermal_zone0: 87 C"
    {
        "pattern": re.compile(r"temp(?:erature)?\s*(?:above threshold|:\s*(\d+)\s*[°C])", re.I),
        "stream_id": "cpu_temperature",
        "extract": lambda m: int(m.group(1)) if m.group(1) else None,
    },
    # OOM killer: indicates memory_usage is effectively 100%
    {
        "pattern": re.compile(r"Out of memory|oom.kill", re.I),
        "stream_id": "memory_usage",
        "extract": lambda m: 100.0,
    },
    # systemd service crash → error_rate signal
    {
        "pattern": re.compile(r"(failed|crashed|core.dump)", re.I),
        "stream_id": "error_rate",
        "extract": lambda m: None,  # signal only, no numeric value
    },
    # Disk space: "No space left on device"
    {
        "pattern": re.compile(r"no space left on device", re.I),
        "stream_id": "disk_free",
        "extract": lambda m: 0.0,
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Translation
# ─────────────────────────────────────────────────────────────────────────────
def translate_entry(raw: dict) -> dict:
    """
    Convert one journalctl JSON entry to the internal log schema.

    Internal schema:
    {
      "schema_version": "1.0",
      "timestamp":      ISO-8601 UTC,
      "source":         foundation.json log_source_taxonomy id,
      "status":         foundation.json system_status_codes id,
      "message":        str,
      "unit":           str | null,
      "pid":            int | null,
      "metrics":        [ { "stream_id": str, "value": float | null } ],
      "_raw_priority":  int
    }

    The Executive Module reads `status` to classify urgency and `metrics`
    to update its interoceptive model. Everything else is for human review.
    """
    # Timestamp: journald gives microseconds since epoch as a string
    ts_us = raw.get("__REALTIME_TIMESTAMP", "0")
    ts_dt = datetime.fromtimestamp(int(ts_us) / 1_000_000, tz=timezone.utc)

    priority_str = raw.get("PRIORITY", "6")
    status = PRIORITY_TO_STATUS.get(priority_str, "NORMAL")

    unit = raw.get("_SYSTEMD_UNIT") or raw.get("SYSLOG_IDENTIFIER") or "unknown"
    source = "systemd"
    for key, val in UNIT_TO_SOURCE.items():
        if key in unit.lower():
            source = val
            break

    message = raw.get("MESSAGE", "")
    # MESSAGE can sometimes be a list of integers (binary blob) — skip those
    if not isinstance(message, str):
        message = "<binary>"

    # Extract metrics from message text
    metrics = []
    for extractor in METRIC_EXTRACTORS:
        match = extractor["pattern"].search(message)
        if match:
            value = extractor["extract"](match)
            metrics.append({
                "stream_id": extractor["stream_id"],
                "value": value,
            })

    # If any metric extract implies a more severe status, upgrade
    if any(m["stream_id"] == "memory_usage" and m["value"] == 100.0 for m in metrics):
        status = max_severity(status, "FATAL")
    if any(m["stream_id"] == "cpu_temperature" and (m["value"] or 0) > 85 for m in metrics):
        status = max_severity(status, "WARNING")

    return {
        "schema_version": "1.0",
        "timestamp":      ts_dt.isoformat(),
        "source":         source,
        "status":         status,
        "message":        message,
        "unit":           unit,
        "pid":            int(raw["_PID"]) if "_PID" in raw else None,
        "metrics":        metrics,
        "_raw_priority":  int(priority_str),
    }


STATUS_ORDER = ["NORMAL", "ALERT", "WARNING", "ERROR", "FATAL"]

def max_severity(a: str, b: str) -> str:
    """Return whichever status code is more severe."""
    rank = {s: i for i, s in enumerate(STATUS_ORDER)}
    return a if rank.get(a, 0) >= rank.get(b, 0) else b


# ─────────────────────────────────────────────────────────────────────────────
# Stream reader
# ─────────────────────────────────────────────────────────────────────────────
def journal_stream(since: str = "now") -> Iterator[dict]:
    """
    Tail the systemd journal in JSON format. Yields raw journal dicts.

    We use --since=now to start from the current moment (not replay history).
    For historical analysis, pass a timestamp like "2026-01-15 00:00:00".

    Requires: systemd (Ubuntu 20.04+)
    """
    cmd = ["journalctl", "-o", "json", "--follow", f"--since={since}", "--no-pager"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    for line in proc.stdout:
        line = line.strip()
        if not line:
            continue
        try:
            yield json.loads(line)
        except json.JSONDecodeError:
            # Malformed line from journald — skip
            continue


def translate_stream(since: str = "now", min_status: str = "ALERT") -> Iterator[dict]:
    """
    Yield translated log events, filtered to min_status severity or above.

    The Executive Module subscribes to this stream. In normal operation it
    uses min_status="ALERT" to avoid flooding on routine INFO messages.
    During boot or troubleshooting, min_status="NORMAL" gives everything.
    """
    min_rank = STATUS_ORDER.index(min_status) if min_status in STATUS_ORDER else 0
    for raw in journal_stream(since=since):
        translated = translate_entry(raw)
        event_rank = STATUS_ORDER.index(translated["status"]) if translated["status"] in STATUS_ORDER else 0
        if event_rank >= min_rank:
            yield translated


# ─────────────────────────────────────────────────────────────────────────────
# CLI: run as standalone pipe (System Ops uses this)
#   journalctl -o json --follow | python log_translator.py
# or let this script call journalctl directly:
#   python log_translator.py --since=now --min-status=ALERT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ubuntu systemd log → internal JSON")
    parser.add_argument("--since",      default="now",  help="journalctl --since value")
    parser.add_argument("--min-status", default="ALERT", choices=STATUS_ORDER,
                        help="Minimum severity to emit")
    parser.add_argument("--stdin",      action="store_true",
                        help="Read journalctl JSON from stdin instead of spawning journalctl")
    args = parser.parse_args()

    if args.stdin:
        # Useful for testing with recorded journal output
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                raw = json.loads(line)
                translated = translate_entry(raw)
                rank = STATUS_ORDER.index(translated["status"]) if translated["status"] in STATUS_ORDER else 0
                min_rank = STATUS_ORDER.index(args.min_status) if args.min_status in STATUS_ORDER else 0
                if rank >= min_rank:
                    print(json.dumps(translated), flush=True)
            except (json.JSONDecodeError, Exception):
                pass
    else:
        for event in translate_stream(since=args.since, min_status=args.min_status):
            print(json.dumps(event), flush=True)
