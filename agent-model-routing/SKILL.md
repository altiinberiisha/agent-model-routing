---
name: agent-model-routing
description: Choose the right model for every subagent before launching it, so expensive models are not spent on work a cheaper one does well. Use this EVERY time you are about to call the Agent tool, write a Workflow script, dispatch parallel agents, or run subagent-driven development or an implementation plan with subagents - even for a single agent, and even when the task seems obviously to need the session's own model. Also use it when the user asks which model a job needs, mentions agent cost or token spend, or says agents should not all share one model.
---

# Agent model routing

The main session usually runs on the most capable and most expensive model. An agent launched
without a `model` inherits it. Most delegated jobs (searching, running a command, implementing a
task that already has a signature and a test) do not need that model, so inheriting by default
wastes the user's money without buying accuracy.

So: **decide the model for each agent separately, and pass `model` explicitly on every Agent
call.** Leaving it out is a decision to pay for the top model; make that decision on purpose or
not at all.

## The tiers

The Agent tool accepts `haiku`, `sonnet`, `opus`, `fable` (cheapest to most expensive). These
are aliases for the current version of each tier; a specific older version cannot be selected
through this parameter.

| Model | Use it for | Examples |
|---|---|---|
| `haiku` | Mechanical work with one right answer and no design choices | Find where a function is used; list files matching a pattern; run the tests and report failures; fetch a page and extract a fact; rename a symbol; apply the same small edit across files |
| `sonnet` | Well-specified building. **The default for implementation.** | Implement a plan task that gives the signature and the tests; write tests for existing code; a bug fix where the cause is known; a migration, a CRUD screen, a config file; documentation; reviewing one task's diff; exploring a codebase to answer a concrete question |
| `opus` | Work that needs judgement, where the brief cannot spell out the answer | Debugging with an unknown cause; designing an algorithm or a detector's rules; a refactor that changes interfaces across several files; concurrency, security or money-handling code; turning a vague requirement into a design; reviewing a whole branch |
| `fable` | The rare job where a mistake is costly and hard to spot, or `opus` has already failed | An architecture decision much later work depends on; the final review before something ships or is deployed; a problem an `opus` agent could not solve |

## How to decide

Ask these in order and stop at the first that settles it.

1. **Did the user name a model for this work?** Use it. Their instruction beats this skill.
2. **Is there exactly one correct result, reachable by following steps?** → `haiku`.
3. **Does the brief already contain the decisions** (file paths, signatures, expected behaviour,
   a test to pass)? → `sonnet`. A good implementation plan exists precisely so that this is
   true; a task from such a plan is `sonnet` work unless something below applies.
4. **Does the agent have to make the decisions itself** (diagnose, design, weigh trade-offs)?
   → `opus`.
5. **Would a wrong answer be expensive and likely to go unnoticed?** → `fable`.

Then adjust once for **verifiability**, which matters as much as difficulty:

- If a test or a command will immediately show whether the result is right, a cheaper model is
  safe: a failure costs one retry. Stay at the tier you picked, or go one lower.
- If nothing will catch a mistake (a review, a research summary you will act on, a design),
  go one tier higher. A confident wrong answer from a cheap model costs more than the tokens
  saved, because you will build on it.

Do not route by how important the *project* is or how long the task is. A long, tedious,
fully-specified task is still `sonnet` or `haiku` work. A two-line change to locking logic may
be `opus` work.

## Escalate instead of over-buying

Start at the tier the rules give. If the agent's result fails its check, or it reports being
stuck or guessing, relaunch **one tier up**, and put what was learned (the failing output, what
was tried) in the new brief. Do not retry at the same tier more than once, and do not jump
straight to `fable`.

Starting high "to be safe" defeats the purpose. One escalation now and then is far cheaper than
running everything a tier too high.

## Cheaper models need better briefs

A lower tier fills gaps in a brief less reliably. Compensate in the brief, not by raising the
model: give exact file paths, the signatures or names to use, what is out of scope, and what
"done" looks like (the command to run and the output that means success). If you cannot write
that brief, the task is not yet `sonnet` work: either finish the thinking yourself first, or it
belongs with `opus`.

## Mechanics to remember

- **Forks ignore `model`.** `subagent_type: "fork"` always runs on the parent's model. Use a
  fork only when the agent truly needs this conversation's context; otherwise launch a fresh
  agent with a proper brief and a chosen model.
- **Named agent types** (for example Explore, Plan) carry a model in their own definition. An
  explicit `model` still overrides it; set one when the default does not match the job.
- **Workflow scripts:** apply the same per-agent choice inside the script wherever the agent
  call accepts a model option (check the workflow-authoring skill for the current API). Do not
  let a fan-out of many agents all inherit the session model.
- **Other skills that launch agents** (subagent-driven development, parallel dispatch, code
  review) do not choose models for you. Apply this skill to each agent they tell you to launch.
  A typical split: implementers on `sonnet`, per-task reviewers on `sonnet`, the final
  whole-branch review on `opus`.
- **The main session's own model is the user's choice.** This skill never changes it.

## Tell the user what you chose

The user cannot see the `model` parameter, and cost is the reason this skill exists. When you
launch agents, say in one line which model each got and why, for example:

> Launching 3 agents: provider client and track buffer on sonnet (specified, test-backed);
> go-around detector on opus (rule design); fixture download on haiku (mechanical).

If you escalate, say so and say what failed.

## Worked examples

**"Find every place we call the adsb.lol API."** One right answer, steps only → `haiku`.

**Plan task: "Implement `detect_squawk(track)`; rules and nine named tests given."** Decisions
are in the brief, tests will catch errors → `sonnet`.

**"The go-around detector fires on normal landings at Denver; find out why."** Unknown cause,
needs diagnosis → `opus`.

**"Review the whole Phase 1 branch before we deploy it publicly."** Nothing downstream catches
a missed problem, and the cost of one is high → `opus`, or `fable` if the deployment handles
anything sensitive.

**"Summarise the licence terms of these three data providers so we can pick one."** Looks like
simple reading, but the summary will be acted on and nothing checks it → one tier up from
`haiku`: `sonnet`.
