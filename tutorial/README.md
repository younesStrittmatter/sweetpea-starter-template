# Tutorial: four questions about one task

Stuck, or want to be led? Say to your assistant: **"Run the guided tutorial."**
It then teaches the four steps itself, one at a time.

One experiment, grown in four steps. Each step is a research question. You say
what you want to find out; your assistant says what the question is about,
proposes a design and what it costs, writes it, and counts it with you.

| Step | The question | New in the design |
|---|---|---|
| [1. Congruency](1_congruency.md) | Does an irrelevant word interfere? | Factors, a derived factor, what is crossed |
| [2. The trial before](2_sequence.md) | Does a conflict change how the next trial is handled? | A transition factor |
| [3. Adaptation](3_adaptation.md) | Do people adjust to how frequent conflict is? | Weights; blocks |
| [4. Transfer](4_transfer.md) | Does adapting to conflict make switching to another task harder? | A second task; mini-blocks with a transition factor inside |

## Backup: notebooks

The same four steps without an assistant, in `notebooks/`. They run on Google
Colab (each step page has an "Open in Colab" button) or in any Jupyter.

## How to work

You do not write code. Your assistant does.

1. Start your assistant in this folder (`claude`, `codex` or `gemini`).
2. Open the page of a step and give the assistant the prompt, in your own words
   if you like.
3. It says what the question is about, asks you about the analysis and
   explains each decision. You decide.
4. It writes the design in `experiments/`, runs it, and walks you through the
   file and the counts.
5. Compare with "What to check" on the page.

`reference/` holds one worked design per step, to compare with afterwards.

The three examples on the website show why the analysis comes first: a design
is a set of choices, and which are acceptable depends on what is compared.
