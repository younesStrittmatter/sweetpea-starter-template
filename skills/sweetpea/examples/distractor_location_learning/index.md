# A distractor that is usually in one place

Source: Gong & Theeuwes (2021), *Attention, Perception, & Psychophysics*,
Experiment 3. doi:10.3758/s13414-020-02142-8

**Takeaway.** Often there is no design without a cost, only a choice between
costs, and which cost is acceptable depends on the analysis. Ask which
comparisons are planned before proposing a design. When two things cannot
share a level (a place, an item, a key), the level that one of them occupies
most cannot also be an ordinary level for the other. Lay out the options with
what each keeps and gives up, say which fits the planned comparisons and why,
and write the chosen design down so that design and analysis agree.

## Research question

**What, and why.** Attentional control: people learn where a salient
distractor tends to appear and suppress that location. Is the suppression of a
location fixed, or does it adjust to how salient the distractor on the current
trial is?

**How.** Visual search for a diamond among eight shapes. On most trials another
shape stands out too (the distractor), weakly or strongly, most often at one
location. Suppression is read from how much a distractor slows the search at
its frequent location, compared with other locations and with no distractor.

**Part used.** A distractor at the frequent location against no distractor.

## Analysis

Response time with the distractor at its usual place against response time
without a distractor, within participants.

## Design as published

| Decision | Chosen | Reason given | What follows |
|---|---|---|---|
| Distractor | Absent on 1 trial in 6; otherwise at one place on 65% of the trials, at each of the 7 others on 5% | The manipulation: people are to learn the place | Unequal on purpose |
| Target without a distractor | Equally often at each of the 8 places | Stated | At the distractor's usual place on 1 trial in 8 |
| Target with a distractor | At random among the 7 places the distractor does not occupy | Stated | With the distractor at its usual place, never at that place |

## What to balance

**Assumption.** Trials with the distractor at its usual place and trials
without a distractor differ only in the distractor.

**Where it fails.** They differ in where the target can be. The target is at
the distractor's usual place on 1 trial in 8 without a distractor, on 1 in 7
with the distractor elsewhere, and never with the distractor at that place.

Those trials are in the design on purpose: the paper compares targets at that
place with targets elsewhere, to show that the place is suppressed, and finds
them slower. The problem is not that they exist. It is that the comparison
with "no distractor" counts them as ordinary baseline trials. This is a
mismatch between design and analysis, not an accident of the design.

This is a regular factor (the place of the target), not a derived one. It is
the simplest case of a combination that cannot exist.

## Options

Three wishes cannot all hold: the distractor is usually at one place (the
manipulation); target and distractor are never at the same place; and where
the target is tells nothing and is told by nothing. The options differ in how
often the target is at the distractor's usual place (`design(choice)` in
`design.py`). Each keeps one wish and gives up two.

| Choice | Target at the usual place | Keeps | Gives up |
|---|---|---|---|
| `"as often"` as at any other free place (the published design) | 1 trial in 8 without a distractor, 1 in 7 with the distractor elsewhere; 9% of all trials | A distractor elsewhere says nothing about the target | The usual place holds the target less often than the other places; 1 baseline trial in 8 has its target where the compared condition never has it |
| `"never"` | never | Every trial has the target elsewhere, so the baseline can use all its trials | A place that never holds the target can be learned as such; no trial is left to compare targets there with targets elsewhere |
| `"more often"`, only on trials with the distractor at another place | 1 in 8 without a distractor, as in the original; more with the distractor elsewhere (twice as often in the code; 10 to 7 gives exactly 1 in 8 over all trials) | Every place holds the target equally often; the baseline is as in the original | With a distractor elsewhere, the target is likelier at the usual place than anywhere else |

The third option leaves the trials without a distractor alone, because they
are the baseline of the main comparison. In SweetPea it is a second copy of
some trials: a factor `copy` in the crossing, and an `Exclude` of every second
copy except those with the target at the usual place and the distractor
elsewhere.

## Which design for which analysis

No option is best in general. Which fits depends on the comparisons that are
planned (`best_for(comparisons)` in `design.py`). This is reasoning from the
counts, not a result of the paper.

| Planned comparison | What it needs | Fits | Why |
|---|---|---|---|
| Distractor at its usual place against no distractor | The same target places in both | `"never"`, or any option with the baseline formed from the trials with the target elsewhere | With the distractor at its usual place the target is always elsewhere |
| Distractor at its usual place against distractor at another place | The same | `"never"`, or the others restricted to the target elsewhere; `"more often"` leaves fewest usable trials | Trials with the distractor elsewhere can have the target at the usual place |
| Target at the usual place against target elsewhere, without a distractor | Trials with the target at the usual place | `"as often"`; `"more often"` if targets being rare at that place is itself a worry | `"never"` has no such trials |

So: if only the first two are planned, `"never"` uses every trial, at the
price of a place that never holds the target. If the third is planned, as in
the paper, `"never"` is out, and the baseline of the other comparisons has to
leave out the trials with the target at the usual place.

In every option the trials with the distractor at its usual place have the
target at the seven other places. A baseline that is fair to them is made of
trials that have the target at those seven places: `target_place ==
"elsewhere"`.

## What to present

Ask first which comparisons are planned. Then show all three options with the
tables above, say which fits those comparisons and why, and name what it gives
up. Do not present one as correct in general. Write the chosen design down
with `target_place` as a factor, so that the choice is explicit and the
analysis can follow it.

Counts of one generated block of each (simplified frequencies), as target
elsewhere / target at the usual place:

| distractor | as often | never | more often |
|---|---|---|---|
| none | 7 / 1 | 7 / 0 | 7 / 1 |
| at its usual place | 28 / 0 | 28 / 0 | 28 / 0 |
| at another place | 42 / 7 | 42 / 0 | 42 / 14 |
