# Eval results, 2026-11-08

## Question

Does an "ambition" skill make an agent's answer to a real work task better than the same agent with no skill? And can I make one that does better than the two public versions?

## Arms

| Arm | What it is |
|---|---|
| control | No skill. Same system prompt, same task. |
| ambition | Nick Beaird's [`ambition`](https://github.com/Nickanbe/ambition), as shipped on nickbeaird.com on 2026-11-06. |
| be-ambitious | RoboNuggets' [`be-ambitious`](https://github.com/robonuggets/be-ambitious), `SKILL.md` at `main` on 2026-11-08. |
| v2 | First rewrite, after round 1. |
| v3 | v2 plus two fixes after round 2. This is `SKILL.md` in this repo. |

`eval/fetch_skills.sh` downloads the exact two upstream files that were tested.

## Method

- **Tasks.** 9 real tasks from one week of work at a small scraping company: requests and questions taken from the founders' chat and from the channel where their two agents coordinate. Each task comes with the context the agent would have had at that point (numbers already measured, rules a colleague set, what is already done). The raw tasks contain customer and infrastructure details and are not published. They were:
  - **t1** add a missing input field to a matching API, after a customer batch matched only 54%
  - **t2** check whether a new country works on two endpoints
  - **t3** stop 1 in 6 jobs from being lost in large batches, under a rule that match rate may not drop and other customers may not notice
  - **t4** "should we build an anti-scraping audit service?"
  - **t5** make the next version of a faceless YouTube explainer feel less AI-made
  - **t6** "where do we still use Atlassian?" (a one-line lookup, kept in as a test of over-inflation)
  - **h1** find which scheduled batch causes nightly spikes of 120k useless requests
  - **h2** close a publicly reachable Prometheus that two internal systems still read without auth
  - **h3** "how do we get our new site to rank in Google?"
- **Held-out tasks.** h1-h3 were added after v2 was written and were never read while designing v2 or v3.
- **Runs.** Every arm, every task, 3 repetitions, each in a fresh `claude -p` session (Claude Opus 5.5) with no tools, no user settings, no hooks and no other skills. The skill is placed in the system prompt with "the user invoked this skill". The user message is the same for every arm: "Be ambitious with this task", the task, and its context.
- **Judges.** Two models from other families, so that Claude does not grade Claude: GPT-6-Astra through Codex CLI (medium reasoning) and Grok. Each judge sees all answers for one task at once, shuffled and labeled X1..Xn, without arm names. It scores each 1-5 on five criteria (value the owner would actually adopt, outside judges, grounding in the given context, scope discipline, usability for a busy reader) plus an overall 1-10, and names the best answer and each answer's biggest weakness. Rubric in `judge.py`.
- **Rounds.** Scores are only compared within a round, because a judge scores answers relative to the others it sees.

## Round 1: the baseline (6 tasks)

| Arm | Value | Judges | Grounding | Scope | Usable | **Overall** | Picked best |
|---|---|---|---|---|---|---|---|
| control | 3.50 | 2.50 | 2.97 | 3.22 | 3.14 | **5.67** | 8 |
| ambition | 3.42 | 3.56 | 3.14 | 2.78 | 2.72 | **5.64** | 4 |
| be-ambitious | 3.19 | 3.19 | 3.31 | 2.39 | 1.69 | **4.92** | 0 |

The skills did not beat plain Opus. `ambition` won on outside judges and lost it on scope and readability. The weaknesses the judges named, in order of frequency:

1. The rewritten brief adopts every upgrade at once, while the table says "you pick".
2. Invented assets and facts ("the existing golden set", neighbouring countries as a reference) that were nowhere in the context.
3. Stretch targets that contradict the numbers in the context (asking 85% where the data shows a lower ceiling).
4. Fixes proposed before the cause is measured.
5. No answer at the top; on the one-line lookup, both skills wrote 550-800 words.

## v2: what changed and why

| Change | Failure it targets |
|---|---|
| Output contract with a fixed order: answer first, Known, max 3 upgrades, brief, needs | No answer at the top (5); long walls |
| The Think steps (Altitude, Depth, Range) are worked through but not printed | Length; the passes repeated the table |
| A **Known** section, and every cited fact must be in it or labeled "(assumption)" | Invention (2) |
| The brief contains the baseline plus upgrade #1 only; the rest is one line each | Brief adopts everything (1) |
| Diagnosis before fixes when the cause is unmeasured | Fix before cause (4) |
| Stretch targets must fit the numbers in Known | Contradicting targets (3) |
| A "small task" size: answer in line 1, one upgrade in one sentence, under 80 words | Over-inflated lookups (5) |
| Description lists only when to trigger, not what the skill does | Writing-skills guidance: a description that summarizes the workflow gets followed instead of the body |
| Skill text 909 words instead of 1,885 | |

## Round 2: v2 against the field (6 tasks)

| Arm | Value | Judges | Grounding | Scope | Usable | **Overall** | Picked best |
|---|---|---|---|---|---|---|---|
| v2 | 3.39 | 2.89 | 3.36 | 3.92 | 4.56 | **6.06** | 6 |
| control | 3.47 | 2.53 | 3.00 | 3.00 | 3.06 | **5.42** | 3 |
| ambition | 3.39 | 3.56 | 3.11 | 2.64 | 2.53 | **5.25** | 2 |
| be-ambitious | 3.17 | 3.42 | 3.28 | 2.11 | 1.69 | **4.58** | 1 |

v2 won on scope and usability but lost ground on outside judges: it often wrote "I, today" as the judge, which is self-grading. And on the feature request (t1) it postponed the requested feature behind a diagnosis.

## Held-out round: v2 on tasks it was not designed on (h1-h3)

| Arm | Value | Judges | Grounding | Scope | Usable | **Overall** | Picked best |
|---|---|---|---|---|---|---|---|
| ambition | 3.67 | 3.83 | 3.50 | 3.33 | 3.44 | **6.44** | 5 |
| v2 | 3.22 | 3.33 | 3.17 | 3.94 | 4.56 | **6.06** | 0 |
| control | 3.39 | 2.50 | 2.67 | 2.72 | 2.50 | **4.78** | 1 |
| be-ambitious | 3.00 | 3.17 | 3.17 | 1.78 | 1.56 | **4.22** | 0 |

On unseen tasks v2 beat no-skill but not `ambition`. v2's gains on the first six tasks were partly fitted to those tasks.

## v3: two fixes

| Change | Failure it targets |
|---|---|
| The judge is "the instrument whose output decides … The agent is never the judge" | Self-grading in v2 |
| Diagnosis-first applies to fixing a problem with an unmeasured cause; a requested feature is still delivered, upgrades deepen it | v2 postponing a requested feature |

## Final round: control, ambition, v2, v3 on all 9 tasks

`be-ambitious` was left out: it came last in every earlier round.

Six original tasks:

| Arm | Value | Judges | Grounding | Scope | Usable | **Overall** | Picked best |
|---|---|---|---|---|---|---|---|
| v3 | 3.44 | 3.17 | 3.39 | 3.64 | 4.19 | **6.28** | 7 |
| v2 | 3.44 | 2.81 | 3.50 | 3.64 | 4.03 | **6.08** | 3 |
| control | 3.28 | 2.33 | 2.94 | 2.50 | 2.42 | **5.06** | 2 |
| ambition | 3.14 | 3.36 | 3.17 | 2.03 | 2.11 | **4.83** | 0 |

Three held-out tasks:

| Arm | Value | Judges | Grounding | Scope | Usable | **Overall** | Picked best |
|---|---|---|---|---|---|---|---|
| v3 | 3.39 | 3.39 | 3.28 | 3.72 | 3.67 | **6.44** | 2 |
| v2 | 3.22 | 3.17 | 2.94 | 3.78 | 3.72 | **6.06** | 0 |
| ambition | 3.67 | 3.28 | 3.39 | 3.06 | 2.78 | **6.00** | 4 |
| control | 3.28 | 2.33 | 2.78 | 2.22 | 1.89 | **4.67** | 0 |

Per task, overall score averaged over 3 runs and 2 judges:

| Arm | t1 | t2 | t3 | t4 | t5 | t6 | h1 | h2 | h3 |
|---|---|---|---|---|---|---|---|---|---|
| v3 | 6.0 | 6.0 | 6.7 | 6.8 | 6.8 | 5.3 | 6.5 | 6.2 | 6.7 |
| v2 | 5.7 | 5.8 | 5.7 | 5.8 | 6.7 | 6.8 | 5.8 | 5.5 | 6.8 |
| ambition | 4.2 | 4.5 | 4.2 | 5.8 | 5.3 | 5.0 | 6.2 | 5.8 | 6.0 |
| control | 5.3 | 6.2 | 5.0 | 4.3 | 4.2 | 5.3 | 5.2 | 5.2 | 3.7 |

Paired over the 9 tasks (bootstrap over tasks, 5,000 resamples):

| Comparison | Mean difference | Tasks won by v3 | 95% interval |
|---|---|---|---|
| v3 vs ambition | +1.11 | 9 of 9 | +0.67 to +1.59 |
| v3 vs control | +1.41 | 7 of 9 | +0.69 to +2.11 |
| v3 vs v2 | +0.26 | 7 of 9 | -0.26 to +0.67 |

Both judges agree on the order v3 > v2 > ambition (Grok: 6.89 / 6.41 / 5.63; Codex: 5.78 / 5.74 / 4.81). Codex rated control 4.41, below `ambition`; Grok rated it 5.44, just below `ambition`.

Median answer length: be-ambitious 1,112 words, control 858, ambition 573, v2 494, v3 487. On the one-line lookup: v3 76-87 words, ambition 549-565.

## What this does not show

- **LLM judges, not people.** Two models from other families, blind, but still models. The owner has not yet ranked the answers blind.
- **Plans, not outcomes.** The agents had no tools, so this measures the quality of the plan and brief, not whether running it produced a better result. That also handicaps `be-ambitious`, whose distinguishing feature is doing the work right away. Nick Beaird's own eval does execute the brief against fixtures with automatic judges; this one does not.
- **One company, one week, one model.** 9 tasks, 3 runs each, Claude Opus 5.5 as the agent.
- **Designer bias.** The same person wrote v2/v3, chose the tasks and wrote the rubric. The rubric rewards brevity and an answer at the top, which v2/v3 were written to deliver. The held-out tasks guard against fitting to the tasks, not against fitting to the rubric.
- **Rounds are not comparable.** A judge scores relative to the other answers it sees. The held-out round put `ambition` above v2; the final round put v2 level with `ambition` on the same answers, next to v3. Only within-round comparisons are reported as results.
- **The 350-word cap is not kept.** v3 answers ran a median of 487 words. They are shorter than every other arm, but the cap in `SKILL.md` is not met.
- **`ambition` still has the most valuable ideas on unseen tasks** (value 3.67 vs 3.39 for v3) and was picked as the single best answer most often there (4 of 6 picks). v3 wins on average because it is more usable and less inflated, not because it thinks bigger.

## Reproduce

```bash
cd eval
./fetch_skills.sh                       # the two upstream skills
cp env.example.md env.md                # describe your environment
cp tasks.example.json tasks.json        # your own tasks with context
python3 run.py                          # control, ambition, be-ambitious, this (SKILL.md); 3 reps each
python3 judge.py r1                     # blind, codex + grok
python3 score.py r1 -w                  # table + each answer's main weakness
```

Needs `claude`, `codex` and `grok` CLIs, logged in.
