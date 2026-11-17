# SweetPea Starter

Design experiments with [SweetPea](https://sweetpea-org.github.io) together
with an AI assistant that knows SweetPea. You say what you want to find out;
the assistant states the hypothesis, writes the design, and counts whether it
does what you asked.

Website with the examples and the tutorial:
<https://younesstrittmatter.github.io/sweetpea-starter/>

> Unofficial and experimental. Not (yet) part of the SweetPea project.

## Start

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/younesStrittmatter/sweetpea-starter-template)

| Way in | What you need |
|---|---|
| **Codespaces** (button above) | A GitHub account. Everything runs in the browser. |
| **Your own copy** | The green button "Use this template" at the top of this page gives you your own repository to keep your designs in. |
| **Your own computer** | Python 3.9 or later: `git clone https://github.com/younesStrittmatter/sweetpea-starter-template`, then `pip install -r requirements.txt`. |
| **Download** | [The folder as a zip](https://github.com/younesStrittmatter/sweetpea-starter-template/archive/refs/heads/main.zip), then `pip install -r requirements.txt`. |

## Bring your AI

Open a terminal and start the assistant you have an account for. Each asks
you to log in through the browser the first time.

| Command | Account |
|---|---|
| `claude` | Claude Pro or Max |
| `codex` | ChatGPT Plus or higher |
| `gemini` | Google account (has a free tier) |

Then say what you want to find out, for example:

- *"I want to run a Stroop experiment to test the congruency effect. What is
  it about, and what do I need to decide?"*
- *"Run the guided tutorial."* The assistant then leads you through the four
  steps in `tutorial/`.

Using a chat window (ChatGPT, Claude, Gemini in the browser)? Upload
`skills/sweetpea/SKILL.md` and copy the code it writes into a notebook.

## What is in here

| Path | Purpose |
|---|---|
| `skills/` | What the assistant reads: the SweetPea reference and working method, worked examples, and how to teach. |
| `tutorial/` | One Stroop experiment in four questions: a page per step, notebooks, and the reference designs. |
| `experiments/` | Your own designs go here. |
| `AGENTS.md` | Tells the assistant where to look. |

This repository is built automatically from
[sweetpea-starter](https://github.com/younesStrittmatter/sweetpea-starter),
where the skills are developed. Changes made here are overwritten.
