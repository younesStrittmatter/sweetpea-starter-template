#!/usr/bin/env python3
"""Count what a trial sequence actually contains.

    python check_design.py trials.csv --balance color congruency --runs congruency
    python check_design.py trials.csv --compare congruency
    python check_design.py block_*.csv --compare congruency

Reads CSV files with one row per trial and one column per factor, and prints

  * how often each level of each column occurs,
  * how often each combination of the --balance columns occurs, and whether
    those combinations are equally frequent,
  * the longest run of each level of the --runs columns,
  * for --compare: everything else that differs between the compared
    conditions. For every other column it tabulates, per condition, its level
    on this trial, its level on the trial before, and whether it repeats; for
    two columns that share levels, whether they are equal; and it lists what
    is unequal. This finds differences nobody asked about. --back N also
    looks N trials back (does a level return?), for tasks with sequences.

Several files are read as several blocks: the trial before is never taken from
another file. Empty cells (the first trial of a transition factor has none)
are ignored. Exits with status 1 if the --balance combinations are not equally
frequent. Needs only the Python standard library.
"""
import argparse
import csv
import sys
from collections import Counter
from itertools import groupby, product
from statistics import NormalDist


def read_columns(paths):
    """The columns of one or several files, with a column `(block)` that tells the files apart."""
    if isinstance(paths, str):
        paths = [paths]
    rows = []
    for number, path in enumerate(paths, start=1):
        with open(path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                row["(block)"] = str(number)
                rows.append(row)
    if not rows:
        sys.exit(f"{', '.join(paths)}: no trials found")
    return {name: [row.get(name, "") for row in rows] for name in rows[0]}


def level_counts(values):
    return Counter(value for value in values if value != "")


def combination_counts(columns, names):
    """Counts of every possible combination of the named columns (zeros included)."""
    levels = [sorted(level_counts(columns[name])) for name in names]
    seen = Counter(
        combination
        for combination in zip(*(columns[name] for name in names))
        if "" not in combination
    )
    return {combination: seen[combination] for combination in product(*levels)}


def longest_runs(values):
    runs = Counter()
    for value, group in groupby(values):
        if value != "":
            runs[value] = max(runs[value], len(list(group)))
    return runs


def differences(columns, compare, smallest=0.05, back=1):
    """Everything that differs between the conditions formed by the `compare` columns.

    For every other column: its level on this trial, its level on the trial before, and
    whether it repeats; for the compared columns: their level on the trial before; and for
    two columns that share levels: whether they are equal, on this trial and across trials.
    A share is reported when it differs between two conditions by more than `smallest`
    and by more than chance allows, or when a level never occurs in a condition although
    it is frequent enough elsewhere to be expected there. The more shares are looked at,
    the stricter the test for each, so that a long list of properties does not produce
    lines by chance alone.
    Returns (findings, number of properties looked at).
    """
    blocks = columns["(block)"]
    n = len(blocks)
    condition = [" / ".join(columns[name][i] for name in compare)
                 if all(columns[name][i] != "" for name in compare) else None for i in range(n)]
    conditions = sorted({c for c in condition if c is not None})
    has_before = [i > 0 and blocks[i] == blocks[i - 1] for i in range(n)]

    properties = []          # (what, column, values per trial or None)
    for name, values in columns.items():
        if name == "(block)" or len(level_counts(values)) > 12:
            continue
        before = [values[i - 1] if has_before[i] and values[i - 1] != "" else None for i in range(n)]
        if name not in compare:
            properties.append(("on this trial", name, [v if v != "" else None for v in values]))
            properties.append(("repeats from the trial before", name,
                               [None if before[i] is None or values[i] == "" else
                                ("repeats" if values[i] == before[i] else "changes") for i in range(n)]))
        properties.append(("on the trial before", name, before))
        for lag in range(2, back + 1):          # further back, when asked for: does the level of `lag` trials ago return?
            same_block = [i >= lag and blocks[i] == blocks[i - lag] for i in range(n)]
            properties.append((f"equals its level {lag} trials before", name,
                               [None if not same_block[i] or values[i] == "" or values[i - lag] == "" else
                                ("same" if values[i] == values[i - lag] else "different") for i in range(n)]))

    # Relations between two columns that share levels (a prime and a target, a colour and a word):
    # do they have the same value on this trial, and does one equal the other of the trial before?
    names = [name for name, values in columns.items() if name != "(block)" and len(level_counts(values)) <= 12]
    for first in names:
        for second in names:
            if first == second or len(set(level_counts(columns[first])) & set(level_counts(columns[second]))) < 2:
                continue
            a, b = columns[first], columns[second]
            if first < second:
                properties.append((f"equals {second} on this trial", first,
                                   [None if a[i] == "" or b[i] == "" else ("same" if a[i] == b[i] else "different") for i in range(n)]))
            properties.append((f"equals {second} of the trial before", first,
                               [None if not has_before[i] or a[i] == "" or b[i - 1] == "" else
                                ("same" if a[i] == b[i - 1] else "different") for i in range(n)]))

    candidates = []
    for what, name, values in properties:
        tables = {c: Counter(v for v, cond in zip(values, condition) if cond == c and v is not None) for c in conditions}
        totals = {c: sum(tables[c].values()) for c in conditions}
        if min(totals.values(), default=0) == 0:
            continue
        # a compared column that has one level per condition on the trial before is a blocked
        # condition seen from the next trial: nothing to report. (Another column that is tied to
        # the condition in this way is reported: that is a complete confound.)
        if name in compare and all(len(table) == 1 for table in tables.values()) and \
                len({next(iter(table)) for table in tables.values()}) == len(conditions):
            continue
        # for a yes-or-no property, report the "yes" side: repeats, same
        for level in sorted({level for table in tables.values() for level in table},
                            key=lambda level: (level not in ("repeats", "same"), level)):
            shares = {c: tables[c][level] / totals[c] for c in conditions}
            low, high = min(conditions, key=shares.get), max(conditions, key=shares.get)
            p = sum(tables[c][level] for c in conditions) / sum(totals.values())
            error = (p * (1 - p) * (1 / totals[low] + 1 / totals[high])) ** 0.5
            gap = shares[high] - shares[low]
            never = shares[low] == 0 and tables[high][level] >= 3 and shares[high] * totals[low] >= 3
            candidates.append((gap, what, name, level, shares, never, error))
            if what == "repeats from the trial before" or what.startswith("equals "):
                break            # the second of two levels is the mirror image of the first
    # One error in twenty over the whole list, not per line. Each line compares the highest with the
    # lowest of the conditions, so with more than two conditions every pair of them counts as a test.
    pairs = max(1, len(conditions) * (len(conditions) - 1) // 2)
    noise = NormalDist().inv_cdf(1 - 0.025 / max(1, len(candidates) * pairs))
    findings = [c[:6] for c in candidates if c[5] or (c[0] > smallest and c[0] > noise * c[6])]
    findings.sort(key=lambda f: -f[0])
    return findings, len(properties), conditions


def report_differences(columns, compare, back=1):
    findings, looked_at, conditions = differences(columns, compare, back=back)
    print(f"\nWhat differs between the levels of {' x '.join(compare)} ({looked_at} properties looked at)")
    if len(conditions) < 2:
        print("  fewer than two conditions: nothing to compare")
        return
    if not findings:
        print("  nothing differs by more than chance in these trials")
    for gap, what, name, level, shares, never in findings:
        cells = ", ".join(f"{c}: {shares[c]:.0%}" for c in conditions)
        print(f"  {name} {what} = {level}   {cells}" + ("   <- never in one condition" if never else ""))
    if findings:
        print("  For each line: is it left out of the crossing (then it can be fixed), or forced by another\n"
              "  choice (then it is a trade-off to put to the user)? Does it plausibly affect the measure?")
    trials = len(columns["(block)"])
    print(f"  Based on {trials} trials. A line is listed when the shares differ by more than 5 points and by more\n"
          "  than chance allows over the whole list. With few trials small differences cannot show: generate\n"
          "  more sequences, pass all the files, and see whether a line stays.")


def report(columns, balance=(), runs=()):
    """Print the report; return True if the --balance combinations are equally frequent."""
    for name in list(balance) + list(runs):
        if name not in columns:
            sys.exit(f"no column named '{name}'; columns are: {', '.join(columns)}")

    total = len(next(iter(columns.values())))
    print(f"{total} trials, columns: {', '.join(columns)}")

    print("\nLevel counts")
    for name, values in columns.items():
        counts = level_counts(values)
        if len(counts) > 12:
            print(f"  {name}: {len(counts)} distinct values (not tabulated)")
            continue
        print(f"  {name}: " + ", ".join(f"{level}={count}" for level, count in sorted(counts.items())))

    balanced = True
    if balance:
        counts = combination_counts(columns, balance)
        balanced = len(set(counts.values())) == 1
        print(f"\nCombinations of {' x '.join(balance)}")
        for combination, count in counts.items():
            print(f"  {' / '.join(combination)}: {count}")
        print("  -> BALANCED: every combination occurs equally often" if balanced
              else "  -> NOT BALANCED: combinations differ in frequency")

    for name in runs:
        print(f"\nLongest run in {name}")
        for level, length in sorted(longest_runs(columns[name]).items()):
            print(f"  {level}: {length}")

    return balanced


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("csv_files", nargs="+", metavar="csv_file")
    parser.add_argument("--balance", nargs="+", default=[], metavar="COLUMN",
                        help="columns whose combinations should be equally frequent")
    parser.add_argument("--runs", nargs="+", default=[], metavar="COLUMN",
                        help="columns for which to report the longest run of each level")
    parser.add_argument("--compare", nargs="+", default=[], metavar="COLUMN",
                        help="the columns of the planned comparison: list everything else that differs between their levels")
    parser.add_argument("--back", type=int, default=1, metavar="N",
                        help="with --compare: also look N trials back (default 1, the trial before)")
    arguments = parser.parse_args()
    columns = read_columns(arguments.csv_files)
    for name in arguments.compare:
        if name not in columns:
            sys.exit(f"no column named '{name}'; columns are: {', '.join(c for c in columns if c != '(block)')}")
    visible = {name: values for name, values in columns.items() if name != "(block)"}
    balanced = report(visible, arguments.balance, arguments.runs)
    if arguments.compare:
        report_differences(columns, arguments.compare, arguments.back)
    sys.exit(0 if balanced else 1)


if __name__ == "__main__":
    main()
