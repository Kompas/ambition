---
name: ambition
description: "Use when someone asks to think bigger, be more ambitious, raise the bar, aim higher, go deeper, or types /ambition, about a task, plan, feature, research question or prompt."
license: MIT
---

# Ambition

Find the deeper version of a task, not a bigger one, and hand it back in a form a busy person can act on in one read.

Built on Felix Rieseberg's four types of ambition (Speed, Altitude, Depth, Range) from "How to be more ambitious: A tutorial for humans with models" (2026-10-13): https://felixrieseberg.com/how-to-be-more-ambitious-a-tutorial-for-humans-with-models/ . Adapted from Nick Beaird's `ambition` skill (MIT). This version was rewritten after a blind eval on real tasks; the evidence is in `eval/RESULTS.md`.

## Think (not printed)

Work through these before writing. They shape the output; they are not the output.

1. **Baseline (Speed).** The literal task and the fastest competent way to do it. Every upgrade is a change from this.
2. **Known.** What the task and context already establish: numbers, rules the person set, work already done, things already tried, what is out of reach. Anything you would cite that is not in here is an assumption and gets labeled as one.
3. **Altitude.** What should happen after this is done? What decision or person does it feed? What would owning the outcome continuously look like? Stop climbing where the result can no longer be measured.
4. **Depth.** What would a field-leading professional do here that was not asked? What raw material would they start from instead of the digested summary? Which instruments and methods would they use? What assumption in the task would they test first?
5. **Range.** Rewrite the deliverable as verbs. Which fields do those verbs, including one adversary? What does each field *do* (methods, not voices)?
6. **Judge.** For each idea: what other than the model shows it worked? Who runs it, when, and what result counts as a pass?

## Output contract

Write in the person's language, headings included. Print these parts, in this order, and nothing else.

1. **First line: the answer.** If the task is a question, answer it. Otherwise name the one upgrade to adopt and why, in at most two sentences.
2. **Known** (max 4 bullets). The facts from the context that the upgrades rest on, including what is already done. Mark any assumption with "(assumption)".
3. **Upgrades** (ranked table, max 3). Columns: Upgrade · Type · Cost · Payoff · Judge.
   - If the task is to fix a problem whose cause is not yet measured, upgrade #1 measures the cause. If the task asks for a feature or change, the brief still delivers it; upgrades deepen it rather than postpone it.
   - Cost = agent time plus what the person must supply (access, data, a decision, waiting time). Never human work-days.
   - Judge = the instrument whose output decides (a test that fails first, a metric in a dashboard, a before/after run on the same data, a held-out set, a person who is not the author), who reads it, when, and the pass line. The agent is never the judge: "I check the logs" is not a judge, "the error count in Grafana for that batch" is.
   - A stretch target must fit the numbers in Known. If the data shows a ceiling, either respect it or make "test whether the ceiling is real" the upgrade.
4. **Brief.** The baseline plus upgrade #1 only, as a prompt that stands alone (it repeats every rule and number it needs). Then one line per other upgrade: "With #2: add …".
5. **Needs from you** (max 3 bullets). Access, data or decisions, each with what it unlocks.

Then stop. The person picks; when they name upgrades, run the brief with those upgrades. If they asked up front to also do the work, do the baseline plus upgrade #1 and report the judge's result next to the target.

## Size

- **Default:** the contract above, under 350 words.
- **Small task** (the answer or the work fits in a few lines, e.g. a lookup, a one-line message, a rename): answer in the first line, then at most one upgrade as a single sentence with its judge. No table, no brief. Under 80 words.
- **Full** (only when the person asks for it): the same contract with up to 5 upgrades and one line per Think step above the table. Under 800 words. Run fields as read-only subagents when available and when there is raw material for them to read.

## Rules

- **Deeper, not bigger.** An upgrade that adds deliverables without raising the outcome, the standard or the set of perspectives is cut.
- **No self-grading.** An upgrade without an outside judge is cut.
- **No invention.** Every number, file, dataset, tool and access you cite is in Known or labeled "(assumption)". Never claim a test, source or result you do not have.
- **Methods, not voices.** A field contributes what it does, never a writing style.
- **Hard targets, honest reports.** Ask for the ambitious number; when the work runs, report the measured result next to it, including misses and what blocked them.
- **Their scope, their call.** Never start an upgrade the person did not pick.

## Example (small task)

> "Which Node version does the build use?"

Node 20, pinned in `.nvmrc`. Upgrade: make CI fail when `.nvmrc` and the `engines` field in `package.json` disagree; pass = a test PR with a mismatch goes red.
