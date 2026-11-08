# ambition

An agent skill that finds the deeper version of a task and hands it back in a form you can act on in one read: the answer first, what is already known, at most three upgrades that each name an outside judge, and a brief you can run.

It is a rewrite of Nick Beaird's [`ambition`](https://www.nickbeaird.com/ambition), which packages Felix Rieseberg's essay [How to be more ambitious: A tutorial for humans with models](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/). The four types of ambition (Speed, Altitude, Depth, Range) and the techniques are Felix's. Read his essay first.

## Why a rewrite

We tested both public versions, Nick's `ambition` and RoboNuggets' [`be-ambitious`](https://github.com/robonuggets/be-ambitious), on nine real tasks from our own week of work, against the same agent with no skill. Two models from other families judged the answers blind. On the six tasks we started with, the original skills did no better than no skill at all (`ambition` 5.64, no skill 5.67, `be-ambitious` 4.92). They found good ideas, but buried them, inflated small tasks and adopted every upgrade at once. On three tasks added later, `ambition` did beat no skill clearly, and `be-ambitious` came last in every round.

This version keeps Felix's method and changes what the agent prints:

| | Nick's `ambition` | This version |
|---|---|---|
| First line | Header and baseline | The answer, or the one upgrade to adopt |
| Altitude / Depth / Range | Printed as passes | Worked through, not printed |
| Facts | | A **Known** section; anything else is labeled "(assumption)" |
| Brief | Adopts the top upgrades | Baseline plus upgrade #1; the rest one line each |
| Judge | Something other than the model | The instrument whose output decides, who reads it, when, the pass line. Never "I check" |
| Fix vs diagnose | | Measure an unknown cause first; a requested feature is still delivered |
| Small tasks | Run the full pass when invoked by name | Answer in line 1, one upgrade in one sentence, under 80 words |
| Skill length | 1,885 words | 909 words |

## Results

Final blind round, 9 tasks, 3 runs each, overall score 1-10 (details and limits in [`eval/RESULTS.md`](eval/RESULTS.md)):

| Arm | 6 tasks used while writing it | 3 held-out tasks | Median length |
|---|---|---|---|
| **this version** | **6.28** | **6.44** | 487 words |
| Nick's `ambition` | 4.83 | 6.00 | 573 words |
| no skill | 5.06 | 4.67 | 858 words |

This version scored higher than `ambition` on all 9 tasks (mean +1.1, 95% interval +0.7 to +1.6). On the held-out tasks, `ambition` still came up with the most valuable ideas and was picked as the single best answer most often. This version wins on average because it is usable and does not inflate the task, not because it thinks bigger. The judges are models and the agents had no tools, so this measures plans, not outcomes.

## Install

Claude Code:

```bash
mkdir -p ~/.claude/skills/ambition
curl -fsSL https://raw.githubusercontent.com/Kompas/ambition/main/SKILL.md -o ~/.claude/skills/ambition/SKILL.md
```

Codex, Cursor, Gemini CLI and other agents that read `SKILL.md`: put it in `.agents/skills/ambition/` in your repo. No skill support: paste `SKILL.md` above your task.

Then ask for it the way you would ask anyway:

```
/ambition stop 1 in 6 jobs from getting lost in large batches
```

## Run the eval on your own tasks

The harness in [`eval/`](eval/) runs any set of skills against a no-skill control in fresh `claude -p` sessions and has the answers judged blind by Codex and Grok. Your own tasks are the point: a skill that wins on someone else's week may not win on yours. See the end of [`eval/RESULTS.md`](eval/RESULTS.md).

## Credits and license

- Method: Felix Rieseberg, [How to be more ambitious](https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/) (2026-10-13).
- Original skill: Nick Beaird, [`ambition`](https://github.com/Nickanbe/ambition) (MIT). His own eval, which executes briefs against fixtures, is in that repo.
- Compared: RoboNuggets, [`be-ambitious`](https://github.com/robonuggets/be-ambitious) (MIT).
- This version: Tim Hagebols. MIT, see [LICENSE](LICENSE).

Not made or endorsed by Felix, Nick, RoboNuggets or Anthropic.
