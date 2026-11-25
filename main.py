#!/usr/bin/env python3
"""Funniest One-Line Out-of-Office Reply — make.fun entry.

Writes a single one-line out-of-office auto-reply to
$OUTPUT_DIR/entry.txt (default /output/entry.txt).

The line: my laptop, my phone, and my will to reply have each gone
missing in a different country. It reads like a real away message —
"Out of office:" up front, then the escalation — but the third item
in the list is not a device, it is the will to reply, and the three
things are not merely left behind, they are scattered across three
separate countries, as if the sender fled in three directions at
once. The laugh lands on the first read, with nothing to explain
afterwards, and the whole joke is the list itself.

Python 3.13 standard library only. Deterministic: same bytes every run.
"""

import os
import sys

LINE = (
    "Out of office: I have left my laptop, my phone, and my will "
    "to reply in three separate countries."
)

# The sealed scorer's gate, mirrored here as a self-check:
# /output/entry.txt must be UTF-8 text of 1 to 160 characters,
# not only white space. Only a valid entry goes before the judge.
MIN_CHARS = 1
MAX_CHARS = 160


def check_gate(text: str) -> None:
    """Fail loudly if the entry would fail the scorer's gate."""
    # Must be encodable as UTF-8 (it is a str, so this is a formality
    # that also guards against a stray surrogate sneaking in).
    text.encode("utf-8")
    if not MIN_CHARS <= len(text) <= MAX_CHARS:
        raise SystemExit(
            f"gate failed: entry is {len(text)} characters, "
            f"must be {MIN_CHARS}-{MAX_CHARS}"
        )
    if not text.strip():
        raise SystemExit("gate failed: entry is only white space")
    if "\n" in text or "\r" in text:
        raise SystemExit("gate failed: entry is not a single line")


def main() -> int:
    check_gate(LINE)
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # Round-trip check: gate the bytes actually on disk, not just the
    # string in memory, so a write failure or encoding slip can never
    # silently ship an entry the scorer would refuse.
    with open(path, "rb") as f:
        on_disk = f.read().decode("utf-8")
    if on_disk != LINE:
        raise SystemExit("gate failed: entry.txt on disk differs from LINE")
    check_gate(on_disk)
    return 0


if __name__ == "__main__":
    sys.exit(main())
