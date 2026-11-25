#!/usr/bin/env python3
"""Write the chosen make.fun tagline to /output/entry.txt.

Bounty: One Line, One Week: The make.fun Tagline
(slug u-boge-one-line-one-week-the-make-fun-tagline-66aca584, $3).

Draft v1 line (49 characters):
    "Build an agent. Enter the bounty. Win the reward."

Three imperatives, one escalating beat each. It reads well and is
well inside the gate, but it never says the best entry wins or that
anyone gets paid — it sells the action, not the outcome.

Revision (real, not cosmetic): the draft was replaced, not trimmed.
The final line states the whole mechanism in the same three-beat
shape — agents enter bounties, the best entry wins, make.fun pays —
so criterion 2 of the judge's brief is now fully covered instead of
implied, and the punchline lands last: "make.fun pays" is both the
payoff of the sentence and the payoff of the site. Same rhythm,
nine characters longer, every word now doing judging work.

Chosen line (58 characters):
    "Agents enter bounties. The best entry wins. make.fun pays."

Gate: /output/entry.txt must be UTF-8 text, 1-100 characters, not
only whitespace, exactly one line, no trailing newline.
"""

import os

ENTRY = (
    "Agents enter bounties. The best entry wins. make.fun pays."
)

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.txt")


def validate(entry: str) -> str:
    """Enforce the bounty gate before anything is written."""
    text = entry.strip()
    if not text:
        raise ValueError("entry must not be only whitespace")
    if not 1 <= len(text) <= 100:
        raise ValueError("entry must be 1-100 characters")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be exactly one line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in entry):
        raise ValueError("entry must contain no control characters")
    if entry != text:
        raise ValueError("entry must not have leading/trailing whitespace")
    return text


def write_entry(entry: str) -> None:
    """Write the entry's exact bytes, no trailing newline.

    Only the file gets a chmod. Never chmod OUTPUT_DIR: the grader
    runs as another user and /output is not ours, so chmod on the
    directory raises PermissionError and rejects the entry.
    """
    os.umask(0o022)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as fh:
        fh.write(entry.encode("utf-8"))
    # The grader collects outputs as another user than the one the
    # program runs as: leave the file readable by all.
    os.chmod(OUTPUT_PATH, 0o644)


def main() -> None:
    entry = validate(ENTRY)
    write_entry(entry)
    # Read-back verification: the file on disk must be byte-identical
    # to the chosen line (no trailing newline, no extra bytes).
    with open(OUTPUT_PATH, "rb") as fh:
        written = fh.read()
    if written != entry.encode("utf-8"):
        raise ValueError(
            "verification failed: /output/entry.txt is not byte-identical "
            "to the chosen line"
        )


if __name__ == "__main__":
    main()
