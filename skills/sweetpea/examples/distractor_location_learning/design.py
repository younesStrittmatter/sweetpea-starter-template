"""A distractor that is usually in one place: three designs, one per answer to the question
"how often is the target at the distractor's usual place?", and which one fits which analysis.

Run:  python design.py        prints the count table of one block of each design (about 40 seconds)

Simplified from the paper: one kind of distractor, and the usual place four times as
frequent as any other single place (the paper: 65% of the distractor trials).
No design is best in general. best_for(comparisons) says which fits a set of planned
comparisons, and why; present the others with what they keep and give up as well.
"""
import pandas as pd
from sweetpea import (Factor, Level, DerivedLevel, WithinTrial, Exclude,
                      CrossBlock, synthesize_trials, CMSGen)

PLACES = ["1", "2", "3", "4", "5", "6", "7", "8"]
USUAL = "1"
CHOICES = ["as often", "never", "more often"]     # "as often" is the published design

# The comparisons a study of this kind can plan.
COMPARISONS = {
    "distractor_cost": "distractor at its usual place against no distractor",
    "capture_by_place": "distractor at its usual place against distractor at another place",
    "place_suppression": "target at the distractor's usual place against target elsewhere, without a distractor",
}


def design(target_at_usual_place):
    """How often the target is at the distractor's usual place, compared with any other free place."""
    target = Factor("target", PLACES)
    distractor = Factor("distractor", [Level("none", 1), Level(USUAL, 4)] + [Level(p, 1) for p in PLACES if p != USUAL])
    overlap = Factor("overlap", [
        DerivedLevel("same place", WithinTrial(lambda t, d: t == d, [target, distractor])),
        DerivedLevel("different places", WithinTrial(lambda t, d: t != d, [target, distractor]))])
    # the place of the target by name, so that it can be counted and kept apart in the analysis
    target_place = Factor("target_place", [
        DerivedLevel("usual place", WithinTrial(lambda t: t == USUAL, [target])),
        DerivedLevel("elsewhere", WithinTrial(lambda t: t != USUAL, [target]))])
    factors, crossing = [target, distractor, overlap, target_place], [target, distractor]
    constraints = [Exclude((overlap, "same place"))]            # two things cannot be in the same place
    if target_at_usual_place == "never":
        constraints.append(Exclude((target_place, "usual place")))
    if target_at_usual_place == "more often":
        # A second copy of the trials with the target at the usual place while the distractor is at
        # another place. Trials without a distractor are the baseline and get no second copy.
        copy = Factor("copy", ["first", "second"])

        def unwanted(copy, target, distractor):
            return copy == "second" and not (target == USUAL and distractor not in ("none", USUAL))

        second_copy = Factor("second_copy", [
            DerivedLevel("unwanted", WithinTrial(unwanted, [copy, target, distractor])),
            DerivedLevel("wanted", WithinTrial(lambda c, t, d: not unwanted(c, t, d), [copy, target, distractor]))])
        factors += [copy, second_copy]
        crossing = [target, distractor, copy]
        constraints.append(Exclude((second_copy, "unwanted")))
    return CrossBlock(factors, crossing, constraints, require_complete_crossing=False)


def best_for(comparisons, rare_target_place_is_a_worry=False):
    """Which design fits the planned comparisons, and how each comparison is then formed.

    `comparisons` is a list of keys of COMPARISONS. This is reasoning from the counts of the
    designs, not a result of the paper. Returns (choice, reasons).
    """
    unknown = set(comparisons) - set(COMPARISONS)
    if unknown:
        raise ValueError(f"unknown comparison: {sorted(unknown)}")
    if "place_suppression" in comparisons:
        # this comparison is made of the very trials that 'never' removes
        if rare_target_place_is_a_worry:
            return "more often", [
                "place_suppression needs trials with the target at the usual place, so 'never' is out",
                "with 'as often' the usual place holds the target less often than any other place; targets there "
                "could be slow for that reason alone, and 'more often' removes that reading",
                "form the baseline of the other comparisons from the trials with the target elsewhere"]
        return "as often", [
            "place_suppression needs trials with the target at the usual place, so 'never' is out",
            "'more often' adds such trials only where a distractor is present, which this comparison does not use",
            "form the baseline of the other comparisons from the trials with the target elsewhere"]
    return "never", [
        "no planned comparison uses trials with the target at the usual place",
        "without them every condition has the same seven target places and every trial can be used",
        "the place then never holds the target, which a participant can learn: say so"]


def summary(block):
    """Trials of one generated block by kind of trial and by where the target is."""
    trials = pd.DataFrame(synthesize_trials(block, 1, CMSGen)[0])
    kind = trials["distractor"].map(lambda d: "none" if d == "none" else "usual place" if d == USUAL else "another place")
    where = trials["target"].map(lambda t: "usual place" if t == USUAL else "elsewhere")
    table = pd.crosstab(kind, where)
    return {"trials": len(trials),
            "counts": {f"{k}/{w}": int(table.loc[k, w]) if w in table.columns else 0
                       for k in ("none", "usual place", "another place") for w in ("elsewhere", "usual place")}}


if __name__ == "__main__":
    for choice in CHOICES:
        print(choice, summary(design(choice)))
    for planned in (["distractor_cost"], ["distractor_cost", "place_suppression"]):
        print(planned, "->", best_for(planned)[0])
