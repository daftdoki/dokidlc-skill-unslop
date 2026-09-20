# dokidlc-skill-unslop

A Claude Code plugin that keeps the `unslop` skill in context: 34 rules for cutting AI tells from writing.

The plugin carries one skill and two hooks. The skill is a process, a Guards section, an "Adding soul" section, and 34 numbered patterns: puffery, AI vocabulary, em dashes, title-case headings, chatbot closers, filler, abstract metaphor nouns, mannered prose, knowing asides. A `SessionStart` hook prints the skill at start, resume, clear, fork, and after compaction, and a `SubagentStart` hook hands it to every subagent, so the agent writes under the rules from the first turn instead of fixing text afterwards. `/unslop` invokes it by hand on a pasted draft.

The text is Lauren Tan's pstack skill from [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop), which condenses Siqi Chen's humanizer. This copy keeps the soul section, five rules, and model invocation that upstream later removed, adds a Guards section after woerndl/unsloppify, and adds rule 34 from a measured run. `SOURCE.md` lists every difference from the pinned upstream commit.

## Why this one

The other public unslop skills, humanizer, theclaymethod, and the rest, are 16k to 29k bytes and built for an on-demand rewrite of one document. This one is 8.7k bytes, small enough to sit in context on every turn and in every subagent, which is the use it exists for. It is not the tool for a heavy rewrite of a long document; humanizer does that better, and can be installed beside it.

Status: maintained, in every dokidlc session since 2026-09-19. Upstream changes come in by hand with `scripts/upstream`.

## Install

From the dokidlc marketplace:

```
claude plugin install unslop@dokidlc
```

Nothing else is needed. Nothing outside the plugin holds a path to the file, so the text follows every update.

## Run it

Start a session and write anything. To see what the hook puts in context:

```
hooks/inject.sh session | head -8
```

```
---
name: unslop
description: Cut AI tells from any writing. Must always apply.
---

# Unslop

Edit text to remove AI patterns and add human voice.
```

On a Slack message written from twelve facts, the same model with and without the skill, from the measured run:

> **Fix:** PR #1462 caps a batch at 5000 rows so a single large import can't hold the lock for that long. Review welcome — I'd like to get this merged before we re-enable the batched writer.

> The fix is in PR #1462, which caps a batch at 5000 rows so one big import can't hold the lock that long again. Reviews welcome, I'd like to get it merged before we re-enable the writer.

## Caveats

- The rules are about tells. They do not stop the agent from dropping a fact: in the measured run both arms lost a date at the same rate, so check the facts yourself.
- The skill body costs about 2,200 tokens in every session and every subagent, including ones that write code.
- CI caps the injected text at 10,000 bytes and it stands at 8,704. A rule added here or upstream is paid for with a cut.

## Other docs

- [skills/unslop/SKILL.md](skills/unslop/SKILL.md) is the skill.
- [SOURCE.md](SOURCE.md) is the upstream pin, the kept, dropped, and added list, and the update procedure.
- [skills/unslop/evals/](skills/unslop/evals/README.md) measures a change: four prompts, a grader, and a runner for the skill-creator loop.

Questions and bugs go to the [issue tracker](https://github.com/daftdoki/dokidlc-skill-unslop/issues).

## License

MIT, with three notices in [LICENSE](LICENSE): Lauren Tan, Siqi Chen, and the unsloppify contributors.
