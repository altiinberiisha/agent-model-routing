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

This copies the skill to `<project>/.claude/skills/agent-model-routing/`. Re-run it after
updating this repo to refresh a project's copy.

A skill is triggered by Claude's judgement, so for reliable use also add this to the project's
`CLAUDE.md`:

```markdown
## Launching agents

Before launching any subagent (Agent tool, Workflow script, or a skill that dispatches agents),
use the `agent-model-routing` skill to choose that agent's model, and pass `model` explicitly.
Agents must not inherit the session model by default: use the cheapest model that can do each
job reliably, and tell the user in one line which model each agent got.
```

## Layout

- `agent-model-routing/SKILL.md` — the skill
- `install.sh` — copies it into a project

## Status

First draft. Not yet evaluated against test prompts.
