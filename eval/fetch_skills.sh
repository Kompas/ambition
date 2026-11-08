#!/usr/bin/env bash
# Fetch the two skills this eval compares against into eval/skills/.
set -euo pipefail
cd "$(dirname "$0")" && mkdir -p skills
# Nick Beaird's ambition (MIT)
tmp=$(mktemp -d); curl -fsSL https://nickbeaird.com/ambition/ambition.zip -o "$tmp/a.zip"
unzip -qo "$tmp/a.zip" -d "$tmp" && cp "$(find "$tmp" -name SKILL.md | head -1)" skills/ambition.md
# RoboNuggets' be-ambitious (MIT)
curl -fsSL https://raw.githubusercontent.com/robonuggets/be-ambitious/main/SKILL.md -o skills/be-ambitious.md
wc -w skills/*.md
