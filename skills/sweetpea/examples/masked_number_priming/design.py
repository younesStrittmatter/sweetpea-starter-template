"""Masked number priming: the published design and four alternatives.

Run:  python design.py        prints the counts of one block of every design

`proposed()` is the design to propose. `as_published()` is shown to explain
what it leaves unequal; do not propose it without raising that.
"""
import pandas as pd
from sweetpea import (Factor, Level, DerivedLevel, WithinTrial, Exclude, MinimumTrials,
                      CrossBlock, synthesize_trials, CMSGen)

NUMBERS = ["1", "4", "6", "9"]
NOTATIONS = ["digit", "word"]

# One fixed incongruent partner per prime. Half of the participants get each
# mapping, so every incongruent pair occurs across the sample.
MAPPINGS = {
    "A": {"1": "6", "4": "9", "6": "1", "9": "4"},
    "B": {"1": "9", "4": "6", "6": "4", "9": "1"},
}


def same_side_of_five(prime, target):
    return (int(prime) < 5) == (int(target) < 5)


def _block_of_pairs(pairs, weights=None, targets=NUMBERS, trials=None):
    """A block that crosses a list of (prime, target) pairs with both notations (used for the alternatives).

    The pairs are one factor, so that exactly the listed pairs occur, each as
    often as its weight says. Prime, target, congruency and number identity
    are derived from the pair.
    """
    weights = weights or {}
    pair = Factor("pair", [Level(f"{p}-{t}", weights.get((p, t), 1)) for p, t in pairs])
    prime_notation = Factor("prime_notation", NOTATIONS)
    target_notation = Factor("target_notation", NOTATIONS)

    def part(name, index, levels):
        return Factor(name, [
            DerivedLevel(n, WithinTrial(lambda x, n=n: x.split("-")[index] == n, [pair])) for n in levels])

    def is_congruent(x):
        return same_side_of_five(*x.split("-"))

    def is_identical(x):
        return x.split("-")[0] == x.split("-")[1]

    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(is_congruent, [pair])),
        DerivedLevel("incongruent", WithinTrial(lambda x: not is_congruent(x), [pair])),
    ])
    number_identity = Factor("number_identity", [
        DerivedLevel("identical", WithinTrial(is_identical, [pair])),
        DerivedLevel("different", WithinTrial(lambda x: not is_identical(x), [pair])),
    ])
    design = [pair, prime_notation, target_notation, part("prime_number", 0, NUMBERS),
              part("target_number", 1, targets), congruency, number_identity]
    constraints = [MinimumTrials(trials)] if trials else []
    return CrossBlock(design, [pair, prime_notation, target_notation], constraints)


def proposed(mapping="A"):
    """Every prime is followed by two targets, one congruent and one incongruent.

    Prime and target are factors; two constraints say what must not occur. No
    pair shows the same number twice, congruency is one half, and every pair
    occurs equally often: 8 pairs x 4 notation combinations x 2 = 64.
    """
    partner = MAPPINGS[mapping]
    prime_number = Factor("prime_number", NUMBERS)
    prime_notation = Factor("prime_notation", NOTATIONS)
    target_number = Factor("target_number", NUMBERS)
    target_notation = Factor("target_notation", NOTATIONS)
    numbers = [prime_number, target_number]

    def left_out(prime, target):
        return not same_side_of_five(prime, target) and partner[prime] != target

    congruency = Factor("congruency", [
        DerivedLevel("congruent", WithinTrial(lambda p, t: same_side_of_five(p, t), numbers)),
        DerivedLevel("incongruent", WithinTrial(lambda p, t: not same_side_of_five(p, t), numbers)),
    ])
    number_identity = Factor("number_identity", [
        DerivedLevel("identical", WithinTrial(lambda p, t: p == t, numbers)),
        DerivedLevel("different", WithinTrial(lambda p, t: p != t, numbers)),
    ])
    pairing = Factor("pairing", [
        DerivedLevel("left_out", WithinTrial(left_out, numbers)),
        DerivedLevel("kept", WithinTrial(lambda p, t: not left_out(p, t), numbers)),
    ])
    design = [prime_number, prime_notation, target_number, target_notation, congruency, number_identity, pairing]
    # every prime, in each notation combination, equally often congruent and incongruent
    crossing = [prime_number, prime_notation, target_notation, congruency]
    constraints = [Exclude((number_identity, "identical")),   # no trial shows the same number twice
                   Exclude((pairing, "left_out")),            # one incongruent target per prime
                   MinimumTrials(64)]
    return CrossBlock(design, crossing, constraints)


def as_published():
    """Every prime-target pair once per block: 16 pairs x 4 notation combinations = 64."""
    return _block_of_pairs([(p, t) for p in NUMBERS for t in NUMBERS])


def drop_identical_double_congruent():
    """Alternative: no identical pairs, the 4 other congruent pairs twice. 64 trials."""
    pairs = [(p, t) for p in NUMBERS for t in NUMBERS if p != t]
    return _block_of_pairs(pairs, weights={pt: 2 for pt in pairs if same_side_of_five(*pt)})


def drop_identical_only():
    """Alternative: no identical pairs, every other pair once. 48 trials, one third congruent."""
    return _block_of_pairs([(p, t) for p in NUMBERS for t in NUMBERS if p != t])


def separate_number_sets():
    """Alternative: primes 1, 4, 6, 9 and targets 2, 3, 7, 8. All 16 pairs once. 64 trials."""
    targets = ["2", "3", "7", "8"]
    return _block_of_pairs([(p, t) for p in NUMBERS for t in targets], targets=targets)


DESIGNS = {
    "proposed": proposed,
    "as_published": as_published,
    "drop_identical_double_congruent": drop_identical_double_congruent,
    "drop_identical_only": drop_identical_only,
    "separate_number_sets": separate_number_sets,
}


def one_block(name):
    """One generated block of the named design, as a table with one row per trial."""
    trials = pd.DataFrame(synthesize_trials(DESIGNS[name](), 1, CMSGen)[0])
    if "pair" not in trials:
        trials["pair"] = trials["prime_number"] + "-" + trials["target_number"]
    return trials


def summary(trials):
    """The counts that the example reports for a block."""
    cell = trials.groupby(["congruency", "number_identity"]).size()
    per_pair = trials.groupby(["congruency", "pair"]).size().groupby("congruency").unique()
    return {
        "trials": len(trials),
        "counts": {f"{c}/{i}": int(n) for (c, i), n in cell.items()},
        "trials_per_pair": {c: sorted(int(v) for v in values) for c, values in per_pair.items()},
        "targets_after_a_prime": int(trials.groupby("prime_number")["target_number"].nunique().max()),
    }


if __name__ == "__main__":
    for name in DESIGNS:
        print(name, summary(one_block(name)))
