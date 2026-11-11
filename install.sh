#!/usr/bin/env bash
# Copy the skill into a project's .claude/skills directory.
# Usage: ./install.sh /path/to/project
set -euo pipefail
project="${1:?usage: ./install.sh /path/to/project}"
src="$(cd "$(dirname "$0")" && pwd)/agent-model-routing"
dest="$project/.claude/skills/agent-model-routing"
mkdir -p "$dest"
cp -r "$src/." "$dest/"
echo "Installed agent-model-routing into $dest"
