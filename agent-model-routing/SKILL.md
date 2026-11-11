---
name: agent-model-routing
description: Choose the right model for every subagent before launching it, so expensive models are not spent on work a cheaper one does well, and brief cheaper models so they catch what expensive ones would. Use this EVERY time you are about to call the Agent tool, write a Workflow script, dispatch parallel agents, or run subagent-driven development or an implementation plan with subagents - even for a single agent, and even when the task seems obviously to need the session's own model. Also use it when the user asks which model a job needs, mentions agent cost or token spend, or says agents should not all share one model.
---

# Agent model routing

The main session usually runs on the most capable and most expensive model. An agent launched
without a `model` inherits it. Most delegated jobs (implementing a well-specified task,
reviewing one diff, re-checking a small fix) do not need that model, so inheriting by default
wastes the user's money without buying accuracy.

So: **decide the model for each agent separately, and pass `model` explicitly on every Agent
call.** Leaving it out is a decision to pay for the top model; make that decision on purpose or
not at all.

## The tiers

The Agent tool accepts `haiku`, `sonnet`, `opus`, `fable` (cheapest to most expensive). These
are aliases for the current version of each tier; a specific older version cannot be selected.

| Model | Use it for |
|---|---|
| `haiku` | One right answer, no design choices: a search, a test run, a fact lookup, a rename. Also: **re-checking a small fix against an exact findings list**, and **a small exact fix given as a fresh agent** (one guard clause, one constant, one test). |
| `sonnet` | **The default for building and for reviewing one task.** Implementing a task whose brief holds the decisions; writing tests; a known-cause bug fix; a CRUD screen; a container file; reviewing one task's diff (with the briefing rules below); a live verification run with stated pass criteria. |
| `opus` | Judgement the brief cannot supply, or misses that would go unnoticed: reviewing logic where a wrong rule silently loses or duplicates data; re-reviewing a rewritten algorithm; the final whole-branch review; diagnosis with an unknown cause; design decisions later work depends on. |
| `fable` | Rare: the final review before something handling sensitive data or money ships, or a problem `opus` could not solve. |

## How to decide

Ask in order; stop at the first that settles it.

1. **Did the user name a model?** Use it.
2. **Exactly one correct result, reachable by following steps?** → `haiku`.
3. **Does the brief already contain the decisions** (paths, signatures, behaviour, a test to
   pass)? → `sonnet`. A good plan exists so that this is true.
4. **Must the agent make or judge decisions itself** (diagnose, design, decide whether a rule is
   right)? → `opus`.
5. **Expensive, likely-unnoticed mistake with sensitive data or money?** → `fable`.

Then adjust once for **verifiability**: if a test or command will immediately show a mistake,
stay or go one lower; if nothing downstream will catch it (a review, a design, a summary you
will act on), go one higher.

Do not route by project importance or task length. Long, fully specified work is still `sonnet`.

## Reviews: brief the reviewer before you upgrade it

Field data (below) showed a `sonnet` reviewer missing or under-rating serious problems for three
fixable reasons. Fix the brief first; it costs nothing.

1. **Give the failure modes and their severity.** List the conditions the spec says must never
   break the program (bad input, outages, duplicates, retries) and say "a violation of any of
   these is Important, not Minor". Without this, `sonnet` found real problems but filed them as
   Minor. With it, `sonnet` matched `opus` on database code.
2. **Tell it to challenge the coordinator's decisions.** If the code implements decisions you
   (the coordinating agent) made before the code existed, say so, and instruct the reviewer to
   test those decisions against real use and report a wrong one as Important, with a concrete
   case. Without this, `sonnet` approved code that faithfully implemented a wrong rule
   ("it follows the controller decision"). With it, `sonnet` rejected wrong rules, with a proof
   script. **Your own pre-dispatch decisions are the biggest single source of serious defects** —
   treat them as unreviewed.
3. **Give it the usage context.** Say how the code is called (how often, on what data, what
   writes concurrently). The most valuable `sonnet` finding of the field test — a design flaw in
   the plan itself — came from one paragraph of usage context.
4. **For code that talks to external systems, require a live run** with numbers to report and
   a pass criterion. Unit tests passed while the real system silently failed (a rate limit and
   a cycle time no test simulated). `opus` discovered that on its own initiative; `sonnet` found
   it in five minutes once the brief asked for a live run.

Then choose the reviewer model:

- One task, settled requirements, briefed as above → `sonnet`.
- Logic where a wrong rule silently loses or duplicates data (detection rules, merge/dedup
  logic, scheduling under concurrency) → `opus`, still briefed as above. Even in challenge mode
  `opus` found more of these, and backed findings with probe scripts.
- A re-check of a small fix against an exact findings list → `haiku`.
- A re-check of a rewritten algorithm → `opus` (it is a new review, not a re-check).
- The final whole-branch review → `opus` (`fable` for sensitive data or money).

## Fix rounds: fresh and cheap beats resumed and expensive

Resuming the original implementer keeps its context, but it also re-reads all of it: a
one-constant fix sent to a long-running implementer cost about 150k tokens; the same size of fix
given to a fresh `haiku` with an exact brief cost about 45k. Resume the implementer when the fix
needs its understanding of the task; otherwise brief a fresh `haiku` (tiny, exact) or `sonnet`.

## Escalate instead of over-buying

Start at the tier the rules give. If a result fails its check, or the agent says it is stuck,
relaunch **one tier up** with what was learned. Do not retry at the same tier more than once,
and do not jump straight to `fable`. Before escalating, ask whether the brief was the problem
(missing decision, missing usage context, missing live check) — in the field test it nearly
always was.

## Cheaper models need better briefs

Give exact file paths, names and signatures to use, what is out of scope, what "done" looks like
(the command and the output that means success), the failure modes that count as serious, and
how the code is used. If you cannot write that brief, finish the thinking yourself or give the
job to `opus`.

## Mechanics to remember

- **Forks ignore `model`** (`subagent_type: "fork"` runs on the parent's model). Prefer a fresh
  agent with a proper brief.
- **Named agent types** carry their own model; an explicit `model` overrides it.
- **Workflow scripts:** choose per agent inside the script; never let a fan-out inherit.
- **Other skills that launch agents** (subagent-driven development, parallel dispatch, code
  review) do not choose models for you. Apply this skill to every agent they launch.
- **Hand reviewers their instructions as a file** when several reviewers share them (e.g. a
  comparison); it keeps the briefs identical and the coordinator's context small.
- **The main session's own model is the user's choice.** This skill never changes it.

## Tell the user what you chose

The user cannot see the `model` parameter. When you launch agents, say in one line which model
each got and why. If you escalate, say so and what failed.

## Worked examples

- **Plan task with signature, rules and named tests** → `sonnet` implementer.
- **Review of that task's diff, rules fixed by the plan** → `sonnet`, with the failure-mode list.
- **Review of a detector whose thresholds and windowing you decided** → `opus`, told to
  challenge your decisions; or `sonnet` in challenge mode if a miss would be noticed quickly.
- **"Add one index and its test" after a review** → fresh `haiku` with the exact change.
- **Re-check that three listed findings were fixed in a 9 KB diff** → `haiku`.
- **A collector/integration that calls a rate-limited API** → `sonnet` reviewer whose brief
  requires a 4-minute live run reporting request outcomes and data gaps.
- **Final review before going public** → `opus`.

## Field evidence

See `field-notes/` in the skill's repository for the measurements behind these rules.
