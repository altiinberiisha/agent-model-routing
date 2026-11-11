## Launching agents

Before launching any subagent (Agent tool, Workflow script, or a skill that dispatches agents),
use the `agent-model-routing` skill to choose that agent's model, and pass `model` explicitly.
Agents must not inherit the session model by default: use the cheapest model that can do each
job reliably, and tell the user in one line which model each agent got.
