#!/bin/sh
# Put the unslop skill in context. Claude Code adds a hook's plain stdout to
# context for SessionStart; SubagentStart takes text only inside a JSON
# envelope. One script, one argument: session or subagent.
# A missing skill file prints nothing and exits 0, so a broken install costs
# the text, never the session.
skill="$(dirname "$0")/../skills/unslop/SKILL.md"
[ -f "$skill" ] || exit 0
case "${1:-session}" in
  session)
    cat "$skill" ;;
  subagent)
    python3 -c 'import json, sys; print(json.dumps({"hookSpecificOutput": {"hookEventName": "SubagentStart", "additionalContext": open(sys.argv[1]).read()}}))' "$skill" ;;
  *)
    echo "inject.sh: session or subagent" >&2; exit 2 ;;
esac
