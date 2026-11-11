#!/usr/bin/env python3
"""PreToolUse hook: refuse agent launches that do not choose a model.

Reads the hook payload on stdin. Allows the call (prints nothing) when the
launch names a model; otherwise prints a deny decision telling Claude to use
the agent-model-routing skill and retry.
"""
import json
import sys

MODELS = ("haiku", "sonnet", "opus", "fable")


def deny(reason: str) -> None:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))


def main() -> None:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return  # unreadable payload: do not block work
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return

    if tool_input.get("subagent_type") == "fork":
        deny(
            "Blocked by agent-model-routing: a fork always runs on the session's "
            "model and ignores `model`. Launch a fresh agent with a complete brief "
            "and an explicit `model` (" + ", ".join(MODELS) + ") instead. If this "
            "work truly needs the whole conversation's context, do it yourself in "
            "the main session."
        )
        return

    if not str(tool_input.get("model") or "").strip():
        deny(
            "Blocked by agent-model-routing: this agent launch has no `model`, so "
            "it would inherit the session's model. Use the agent-model-routing "
            "skill to pick the cheapest model that can do this job reliably, then "
            "retry with `model` set to one of: " + ", ".join(MODELS) + ". Tell the "
            "user in one line which model you chose and why."
        )


if __name__ == "__main__":
    main()
