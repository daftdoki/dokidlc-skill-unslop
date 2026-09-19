# dokidlc-skill-unslop

A Claude Code plugin that carries one skill, `unslop`: rules for cutting
AI tells from writing and putting a human voice back. Thirty-three
numbered patterns, a process, a Guards section, and the "Adding soul"
section.

The text is Lauren Tan's pstack skill from
[cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop),
which condenses Siqi Chen's humanizer. This copy keeps the soul section,
five rules, and model invocation that upstream later removed, and adds a
Guards section after woerndl/unsloppify. `SOURCE.md` lists every
difference from the pinned upstream commit. MIT, with all three notices in
`LICENSE`.

## Install

From the dokidlc marketplace:

```
claude plugin install unslop@dokidlc
```

The skill loads as `unslop:unslop`. The plugin also puts the skill body
in context on its own: a `SessionStart` hook prints it at start, resume,
clear, fork, and after compaction, and a `SubagentStart` hook hands it to
every subagent. Nothing outside the plugin holds a path to the file, so
the text follows every update.

## Update from upstream

```
scripts/upstream check     upstream commits since the pin, and the diff
scripts/upstream pull      three-way merge of upstream's changes since the pin, move the pin
```

Both need `gh` logged in. After `pull`, resolve any conflict markers,
confirm the parts `SOURCE.md` lists as kept are still there, and commit.

## Layout

```
.claude-plugin/plugin.json          manifest
skills/unslop/SKILL.md              the skill
hooks/hooks.json                    SessionStart and SubagentStart
hooks/inject.sh                     prints the skill in the shape each event takes
SOURCE.md                           upstream, pin, and the kept, dropped, added list
scripts/upstream                    check and pull
LICENSE                             MIT: Lauren Tan, Siqi Chen, unsloppify contributors
```
