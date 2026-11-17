#!/usr/bin/env python3
"""Run a Python script with a time limit, so that a design that is too large to generate shows at once.

    python limit.py 60 experiments/my_design.py [arguments of the script]

Stops the script after the given number of seconds and says so. Exit status 124 means it was stopped.
Needs only the Python standard library.
"""
import subprocess
import sys


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    seconds, script = float(sys.argv[1]), sys.argv[2:]
    try:
        sys.exit(subprocess.run([sys.executable, *script], timeout=seconds).returncode)
    except subprocess.TimeoutExpired:
        print(f"\nStopped after {seconds:g} seconds: the design takes too long to generate as written.\n"
              "Shorten the block and build the session from several blocks, cross fewer factors, or drop a\n"
              "constraint, and tell the user what you changed and what it costs.", file=sys.stderr)
        sys.exit(124)


if __name__ == "__main__":
    main()
