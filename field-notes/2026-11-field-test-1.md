# Field test 1 — a 15-task build with subagent-driven development

**Date:** November 2026. **Project:** a web dashboard plus a Python data collector sharing a
Postgres database (13 planned tasks, 2 deployment tasks), built task by task by subagents, each
task reviewed before the next. The coordinating session ran on `opus`. Every agent's model was
chosen with this skill and logged.

## What was launched

| Model | Agents | Roles |
|---|---|---|
| `sonnet` | 45 | all 15 implementers; most task reviews; most fix rounds |
| `opus` | 9 | 6 comparison reviews, 2 re-reviews of rewritten algorithms, 1 final whole-branch review |
| `haiku` | 8 | re-reviews of small fixes, small exact fixes as fresh agents |

Tokens per agent were similar across models for the same job (most reviews 40–75k, mostly fixed
context overhead), so the price per token is the main cost lever. `opus` reviews took 2–4×
the wall time of `sonnet` reviews of the same diff.

No implementer ever needed escalating to a stronger model. Every fix round traced back to the
brief or to a decision the coordinator had made, not to model capability.

## Sonnet vs opus on the same review

Six task reviews were run twice, `sonnet` and `opus`, from an identical brief; neither saw the
other's result.

| Task kind | Brief | Serious issues: sonnet / opus | Notes |
|---|---|---|---|
| database schema | plain | 1 / 3 | sonnet saw one of opus's issues but rated it Minor |
| storage + retry logic | + failure modes marked Important | 1 / 1 (same) | sharper brief closed the gap |
| detection logic | + failure modes | 0 / 1 | sonnet saw the flaw, filed it Minor because "it follows the controller decision" |
| detection logic | + challenge the coordinator's decisions | 2 / 3 | sonnet found one opus missed; opus two sonnet missed |
| integration with a live API | + challenge | 3 / 3, different | opus checked the live database and found detection silently never fired |
| concurrent scheduled job | + challenge | 3 / same 3 | opus proved it with a probe and proposed a better single fix |

Takeaways:

1. A plain-briefed `sonnet` reviewer **sees** most problems but **under-rates** them, and
   **defers to the coordinator's decisions**. Both are fixed by the brief, not the model.
2. With a sharp brief, `sonnet` matched `opus` on spec-checking work at about half the time.
3. `opus` kept an edge on deep logic and, unprompted, on checking real behaviour (probe scripts,
   the live database). Once the brief asked for a live run, `sonnet` did that too.

## The final whole-branch review

One `opus` review of the whole branch (about 200k tokens, 7 minutes) found four Important issues
that no per-task review could see, because each needed two components at once: a health signal
that reported "healthy" while partial upstream failures made detection blind, and a retention
job that deleted rows but never freed disk. It also triaged ~70 deferred minor findings into
"fix now" and "later". This is the clearest case for paying for `opus`.

## Haiku

8 of 8 `haiku` jobs passed: 5 re-reviews of small fixes (each cited line evidence, two spotted
real residual issues) and 3 small fixes from a fresh, exact brief. Same token count as `sonnet`
for the same job, at a fraction of the price.

## Where the serious defects came from

Of the serious defects found by reviews, the largest group came from decisions the coordinating
agent wrote into the briefs before any code existed (a dedup rule, a detection-window rule, a
refresh trigger, a merge rule). Implementers followed them faithfully. Reviews only caught them
when told the decisions were open to challenge.

## Costly patterns observed

- Resuming a long-running implementer for a one-line fix: ~150k tokens vs ~45k for a fresh
  `haiku` with an exact brief.
- Shadow reviews for comparison double review cost; they are worth it only as an experiment.
