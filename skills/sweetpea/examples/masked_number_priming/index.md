# Masked number priming

Source: Zerweck et al. (2021), *Attention, Perception, & Psychophysics*,
Experiment 3. doi:10.3758/s13414-021-02312-2

**Takeaway.** A complete crossing of two stimuli from the same set contains
the pairs with the same item twice, and those can only be congruent. When you
remove them, check what the first stimulus then says about the second: the
second must be equally expected in every compared condition.

## Research question

**What, and why.** Unconscious processing: is the magnitude of a number
processed when the number is masked and cannot be reported? The paper tests
the standard evidence for this by comparing a direct and an indirect measure
of the masked number.

**How.** Masked priming: a masked number (the prime) precedes a visible one
(the target), which is classified as smaller or larger than five. If the
prime's magnitude was processed, responses are faster when both fall on the
same side of five (the priming effect).

**Part used.** The priming effect in the indirect task.

## Analysis

Response time on congruent against incongruent trials, within participants.

## Design as published

| Decision | Chosen | Reason given | What follows |
|---|---|---|---|
| Numbers | 1, 4, 6, 9, as digit or word | Replicates Dehaene et al. (1998) | Two numbers on each side of five |
| Primes and targets | Same four numbers | Same | A prime can equal its target |
| Pairs | All 16 number pairs x 4 notation combinations, once per block (64 trials) | None | Half congruent; a quarter show the same number twice |
| Order | Random per block | None | The previous trial is not controlled |

The design is counterbalanced, not only randomised: prime and target are
completely crossed. The same-number trials are cells of that crossing, so they
are a consequence of the counterbalancing and not an accident of sampling.

## What to balance

**Assumption.** Congruent and incongruent trials differ only in whether prime
and target share the category.

**Where it fails.** Half of the congruent trials repeat the number; no
incongruent trial can.

| | different number | same number |
|---|---|---|
| congruent | 16 | 16 |
| incongruent | 32 | 0 |

A congruent response may be faster because the number repeats, not because the
category matches. Reordering trials cannot change this: an incongruent pair
with the same number does not exist.

## Options

In the design (functions in `design.py`):

| Option | Same-number pairs | Congruent share | Trials per congruent : incongruent pair | Cost |
|---|---|---|---|---|
| `proposed`: each prime has one congruent and one fixed incongruent target | none | 1/2 | 8 : 8 | Half of the incongruent pairs are not shown to a participant; use two mappings across participants. Two targets per prime, each expected at 50%. |
| `drop_identical_double_congruent` | none | 1/2 | 8 : 4 | After a prime, its congruent target is twice as likely as each incongruent target (50% against 25%), so congruent targets are the expected numbers. Congruency itself and the response stay at one half. |
| `drop_identical_only` | none | 1/3 | 4 : 4 | Incongruent trials are twice as frequent as congruent ones; 48 trials. |
| `separate_number_sets`: primes 1, 4, 6, 9, targets 2, 3, 7, 8 | none | 1/2 | 4 : 4 | Primes never occur as targets, which is a different question (priming by numbers never responded to). |

In the analysis, with the published design:

| Option | Cost |
|---|---|
| Leave the same-number trials out of the congruent mean | Congruent mean from 16 trials per block, incongruent from 32. Participants still saw the repetitions. |
| Three trial types: same number, congruent with different numbers, incongruent | Same trial counts. Identity cannot be crossed with congruency, because one of the four cells does not exist. |

**Unequal in every option.** Numerical distance: congruent pairs of different
numbers are 3 apart, incongruent pairs 2, 5 or 8 (5 in `proposed`).

None of the options is the correct one; which to take depends on the claim.

## Design to propose

`proposed()`. Raise number identity with the user, show this design, and name
the alternatives with their costs.

Prime and target stay separate factors, crossed as prime x congruency. Two
constraints remove what must not occur: `Exclude` the trials with the same
number, and `Exclude` the incongruent pairs outside the mapping.

When checking any option, state what the prime predicts separately for the
trial type, the response and the target number. In
`drop_identical_double_congruent` the first two stay at one half and only the
third is unequal.

| | `as_published` | `proposed` |
|---|---|---|
| trials | 64 | 64 |
| congruent / incongruent | 32 / 32 | 32 / 32 |
| congruent trials with the same number | 16 | 0 |
| trials per pair, congruent : incongruent | 4 : 4 | 8 : 8 |
| targets that can follow a prime | 4 | 2 |
| how expected the target is after its prime, congruent : incongruent | 25% : 25% | 50% : 50% |
