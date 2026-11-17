# Simon task: the trial before

Source: Dunaway & Weissman (2026), *Psychological Research*, Experiment 4.
doi:10.1007/s00426-025-02216-y

**Takeaway.** Making things even within a short stretch of trials (sets,
mini-blocks) changes what follows what: a trial then follows its own type, its
side and its response less often than half of the time, and this does not even
out over a block. When a user asks for such sets, say so, and offer to make
what repeats from the trial before part of the design. The sets can stay.

## Research question

**What, and why.** Cognitive control: when two irrelevant signals are present
at once, do their effects on a response add up or interact? The answer speaks
to whether one control process handles all distraction or several handle
different kinds.

**How.** A prime word (Red, Green or Cross) is followed by a red or green
square on the left or right. Participants press the key of the colour. The
word can match the colour or not; the side can match the side of the key or
not (the Simon effect). The two effects are compared across their
combinations.

**Part used.** The Simon effect and its interaction with prime compatibility.

## Analysis

Response time and errors by prime compatibility (compatible, neutral,
incompatible) and Simon congruency (congruent, incongruent), within
participants.

## Design as published

| Decision | Chosen | Reason given | What follows |
|---|---|---|---|
| Combinations | 3 words x 2 sides x 2 colours = 12 | Fully crossed design | Each of the 6 conditions twice per set |
| Sets | A block is 9 sets of the 12 combinations, each set in its own random order | "By presenting each of the 12 possible combinations equally often, we avoided contingency learning confounds." | Inside a set a trial follows its own type less often than another type |
| Trial before | Not controlled | None | A congruent trial follows a congruent one in 46% of cases (11/24), not 50% |

The design is counterbalanced for the combinations, by choice and for a stated
reason. The trial before is a side effect of that choice.

## What to balance

**Assumption.** The compared conditions have the same kinds of trial before
them. Congruency effects depend on the trial before (the congruency sequence
effect), and so do repetitions of the side and of the response.

**Where it fails.** Inside a set, whatever was just shown is scarcer among the
trials that are left. Between two sets nothing is biased. The borders are
fair, and fair cannot make up for the bias inside the sets, so it does not
even out over a block. It concerns every property that is even within a set,
derived or not.

What repeats from one trial to the next, over many blocks of shuffled sets:

| Set size | Trial type | Side | Response | The same square |
|---|---|---|---|---|
| 2 (one congruent, one incongruent square) | 25% | 50% | 50% | 12.5% |
| 4 (each square once) | 37.5% | 37.5% | 37.5% | 6.25% |
| 12 (the original) | 45.8% | 45.8% | 45.8% | 18.75% |
| without sets | 50% | 50% | 50% | 25% |

## Options

In the design (functions in `design.py`):

| Option | Sets kept | What repeats | Cost |
|---|---|---|---|
| `proposed`: sets of 12, merged with a block that crosses "the side repeats" with "the colour repeats" over the whole block | yes | trial type 50%, side 50%, response 50%, same square 25% | One extra trial per block (109). Inside a set the transitions stay free. About four minutes to generate at 109 trials, seconds at 49. |
| `within_every_four`: the same, and also even within every four trials | yes | the same | Stricter than needed: a regularity in the order. Seconds with `CMSGen`. |
| `conditions_crossed`: each of the 6 conditions follows each 3 times | yes | trial type 50% | About two minutes; side and response are not addressed. |
| `trial_type_only`: Simon congruency crossed with that of the trial before | yes | trial type 50%, side and response further from 50% than before | Evens out one property by adding trials on which side and colour both change. Do not propose. |
| No sets: cross the square with the square before | no | all even | Gives up the sets and what they were for. |

In the analysis, with the published design:

| Option | Cost |
|---|---|
| Add the trial before as a factor of the analysis | More cells with fewer trials each; the first trial of a block drops out. |
| Reweight the conditions to the same share of each kind of trial before | Changes what the condition mean estimates; needs a choice of weights. |

**What smaller sets cost.** Sets and an even trial before are two demands on
the same order. With sets of 12 no further restriction was found. With sets of
4 (each square once) every set has to start with the square that ended the
last one, because a square can repeat only across a border. With sets of 2 the
order of trial types is fixed (c i i c c i i c). Say this when a user wants
small sets.

None of the options is the correct one; which to take depends on the claim.

## What to tell the user

When someone asks for sets, mini-blocks or "each condition once every n
trials", say these four things before writing the design:

1. Sets make every combination equally frequent and evenly spread. They also
   make a trial follow its own type less often than half of the time, and that
   does not even out over a block. Give the number for their set size.
2. It concerns everything that is even within a set: the trial type, the side,
   the response, the stimulus itself.
3. It matters when the measure depends on the trial before, which is usual in
   conflict, switching and priming tasks. Ask whether it does.
4. It can be made part of the design with the sets kept. Evening out one
   property alone makes the others worse, so balance all of them, and say what
   small sets cost.

## Design to propose

`proposed()`. Raise what repeats from the trial before with the user, show
this design, and name the alternatives with their costs.

Two blocks, merged with `Merge`. The first holds the twelve combinations in
repeat mode: once in every set. The second crosses "the side repeats" with
"the colour repeats" in weight mode: each of the four cases equally often,
anywhere in the block. Nothing is counted by hand; the two blocks say what
is even where. Inside a set the combinations are even and the transitions
are free; over the block the transitions are even. The balance is over all
trials, not within each of the six compared conditions; `conditions_crossed`
does that.

| | `as_published` | `proposed` |
|---|---|---|
| trials per block | 108 | 109 |
| sets of 12 with every combination once | 9 | 9 |
| the same trial type follows | 45.8% in the long run | 50% in every block |
| the side repeats, the response repeats | 45.8% | 50% |
| the same square repeats | 18.75% | 25% |

`as_published()` gives a valid block of shuffled sets, but SweetPea's sampler
does not draw orders the way a shuffle does. The rates above are exact under
shuffling, not counts from that block.
