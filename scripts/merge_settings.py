#!/usr/bin/env python3
"""Add the agent-model-routing PreToolUse hook to a Claude Code settings file.

Preserves everything already in the file and does nothing if the hook is
already there. Usage: merge_settings.py /path/to/.claude/settings.json
"""
import json
import sys
from pathlib import Path

MATCHER = "Agent|Task"
COMMAND = (
    'python3 "$CLAUDE_PROJECT_DIR/.claude/skills/agent-model-routing/'
    'hooks/require_agent_model.py"'
)
MARKER = "agent-model-routing/hooks/require_agent_model.py"


def main() -> None:
    path = Path(sys.argv[1])
    settings = json.loads(path.read_text()) if path.exists() and path.read_text().strip() else {}
    entries = settings.setdefault("hooks", {}).setdefault("PreToolUse", [])

    for entry in entries:
        for hook in entry.get("hooks", []):
            if MARKER in hook.get("command", ""):
                return

    entries.append({
        "matcher": MATCHER,
        "hooks": [{"type": "command", "command": COMMAND, "timeout": 10}],
    })
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(settings, indent=2) + "\n")


if __name__ == "__main__":
    main()
