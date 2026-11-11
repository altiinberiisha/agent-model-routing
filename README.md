# agent-model-routing

A Claude Code skill that makes the main session choose a model for every subagent it launches,
so expensive models are not spent on work a cheaper one does well.

Without it, agents inherit the session's model. With it, each agent gets the cheapest tier that
can do its job reliably (`haiku`, `sonnet`, `opus` or `fable`), the choice is escalated only when
a result fails its check, and the user is told which model each agent got.

## Install into a project

```bash
./install.sh /path/to/project
```

This sets up three things, and is safe to re-run (re-running refreshes the skill):

1. **The skill** at `<project>/.claude/skills/agent-model-routing/` — how to choose a model.
2. **A hook** in `<project>/.claude/settings.json` — Claude Code runs it before every agent
   launch and blocks any launch that does not name a model, telling Claude to use the skill and
   retry. Existing settings are preserved.
3. **A rule** appended to `<project>/CLAUDE.md` — so the instruction is in every session.

In an already-running Claude Code session, open `/hooks` once or restart to load the hook.

## What the hook does and does not do

- It guarantees a model is chosen for each launch. It cannot judge whether the choice was a
  good one; that is the skill's job.
- It blocks forks (`subagent_type: "fork"`), because a fork always runs on the session's model.
- Agents started inside Workflow scripts may not pass through it.

To remove the enforcement, delete the `agent-model-routing` entry from `hooks.PreToolUse` in
the project's `.claude/settings.json`.

## Layout

- `agent-model-routing/SKILL.md` — the skill
- `agent-model-routing/hooks/require_agent_model.py` — the hook
- `scripts/` — used by `install.sh`
- `field-notes/` — measurements behind the rules
- `install.sh` — installs all three into a project

## Status

First draft. The hook is tested; the skill's model choices are not yet evaluated against test
prompts.
