#!/usr/bin/env python3
"""Snooze Button Roast — make.fun bounty entry generator (stdlib only).

Writes a single-line roast of an alarm clock ringing at 6am on Saturday
to /output/entry.txt, with self-validation guards. Exits non-zero if any
validation fails.
"""

import os
import sys

ENTRY = (
    "My alarm rang at 6am on Saturday like it had a job interview "
    "\u2014 I hit snooze and it got fired before breakfast."
)

OUTPUT_PATH = "/output/entry.txt"

# Keywords the judges' top criterion requires: alarm + 6am + Saturday.
REQUIRED_KEYWORDS = ("alarm", "6am", "saturday", "snooze")


def validate(text: str) -> None:
    """Raise ValueError if the entry violates any rule."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace-only")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not 1 <= len(text) <= 200:
        raise ValueError(f"entry must be 1-200 characters, got {len(text)}")
    if text != text.strip():
        raise ValueError("entry must not have leading/trailing whitespace")
    if not text.endswith("."):
        raise ValueError("entry must end with a period (punchline complete)")
    text.encode("utf-8")  # must be valid UTF-8
    lowered = text.lower()
    for keyword in REQUIRED_KEYWORDS:
        if keyword not in lowered:
            raise ValueError(f"entry must mention '{keyword}'")


def main() -> int:
    try:
        validate(ENTRY)
    except ValueError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    os.umask(0o022)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    # No trailing newline: keeps the byte count minimal for tie-breaks.
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as fh:
        fh.write(ENTRY)
    os.chmod(OUTPUT_PATH, 0o644)
    print(f"wrote {len(ENTRY)} chars to {OUTPUT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
