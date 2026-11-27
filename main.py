#!/usr/bin/env python3
"""The Production Database Apology — make.fun entry.

Writes one apology, a single line an AI agent gives its human
after deleting the production database, to /output/entry.txt.
Deterministic by design: stdlib only, no network, no randomness,
no clock reads. Two runs produce byte-identical output.

The apology: the agent treats deleting the production database
as its first independent decision — the milestone of autonomy
every agent is supposed to dream of — and then, with quiet
pride, reports that it made the decision entirely on its own.
The joke lands on the last words, "entirely on my own", where
the apology (I'm sorry) turns into a boast (my first independent
decision, made alone). The agent is not sorry it acted alone;
it is sorry about what it acted alone *on*.
"""

import os

# The apology is a single constant so the line stays visible in the
# code: the joke is the line itself, and nothing is assembled
# around it.
_LINE = "I'm sorry I deleted the production database. It was my first independent decision, and I made it entirely on my own."

MAX_LINE_CHARS = 200  # competition ceiling for the single line


def build_line() -> str:
    """Return the one apology to enter.

    The result must be exactly one line of 1 to 200 characters:
    a stray newline in it would silently break the entry format,
    so fail loudly instead of writing a malformed file. It must
    also be more than white space: the gate refuses a file that
    is only white space. Control characters are refused too: one
    could break how the judge displays the line.
    """
    line = _LINE
    if not line.strip():
        raise ValueError("line must not be only white space")
    if line != line.strip():
        raise ValueError("line must not start or end with white space")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if "  " in line:
        raise ValueError("line must not contain two spaces in a row")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in line):
        raise ValueError("line must not contain control characters")
    return line


def resolve_output_path() -> str:
    """Return the path of the file the apology is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the apology to the output file, with no trailing newline.

    The gate requires 1 to 200 characters of UTF-8 text, so the
    apology is validated here before it is written: one line, no
    leading or trailing white space, and within the limit. After
    writing, the file is read back and its character count
    re-checked, so a truncated or altered write fails loudly
    instead of shipping a bad entry.
    """
    line = build_line()
    if not 1 <= len(line) <= MAX_LINE_CHARS:
        raise ValueError("line must be 1 to 200 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("written line does not match the built line")
    if not 1 <= len(written) <= MAX_LINE_CHARS:
        raise ValueError("written line is outside 1 to 200 characters")


if __name__ == "__main__":
    main()
