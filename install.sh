#!/usr/bin/env bash
# Install agent-model-routing into a project: the skill, the hook that enforces
# it, and the CLAUDE.md rule. Safe to re-run; re-running refreshes the skill.
# Usage: ./install.sh /path/to/project
set -euo pipefail
project="${1:?usage: ./install.sh /path/to/project}"
here="$(cd "$(dirname "$0")" && pwd)"
dest="$project/.claude/skills/agent-model-routing"

mkdir -p "$dest"
cp -r "$here/agent-model-routing/." "$dest/"
echo "Skill:     $dest"

python3 "$here/scripts/merge_settings.py" "$project/.claude/settings.json"
echo "Hook:      $project/.claude/settings.json"

claude_md="$project/CLAUDE.md"
if ! grep -q "agent-model-routing" "$claude_md" 2>/dev/null; then
  { [ -s "$claude_md" ] && echo; cat "$here/scripts/claude_md_rule.md"; } >> "$claude_md"
  echo "CLAUDE.md: rule added"
else
  echo "CLAUDE.md: rule already present"
fi

echo "Done. In a running Claude Code session, open /hooks once (or restart) to load the hook."
