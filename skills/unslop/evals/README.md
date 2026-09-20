# Measuring a change to the skill

Four writing prompts, none of which says "unslop": a slop release note to
rewrite, a PR description from a diff, a Slack incident message from a list
of facts, and a plain README intro with a vendor quote to keep. `evals.json`
lists each prompt, the facts its output must keep, the quoted text that must
survive as written, and a length band. `inputs/` holds the files the prompts
name. `tells.py` grades one output on the rules a regex can find: dashes,
curly quotes, title case, emoji, the vocabulary lists, filler, chatbot
closers, bold-label lines, fact survival, quote survival, length, a
fragment share, and a phrase list for rule 34. Soul, rhythm, and invented
claims are for a person in the viewer.

One run of one eval in one arm:

```
run.sh WORKSPACE ITERATION EVAL_ID with_skill|without_skill RUN
```

Both arms are `claude -p --setting-sources ""` in a scratch directory, so
nothing on the machine reaches the baseline. The with-skill arm adds
`--plugin-dir` for this repository, and the hook delivers the skill the way
an install does. `MODEL` and `SKILL_DIR` override the defaults. The run
writes `outputs/`, `result.json`, `timing.json`, and `grading.json` under
`WORKSPACE/iteration-N/eval-ID-NAME/ARM/run-N/`, in the shape the
skill-creator plugin's `scripts.aggregate_benchmark` and
`eval-viewer/generate_review.py` read.

The 2026-09-20 run, claude-opus-5, three runs per arm: before the change,
6 of 12 with-skill outputs carried a reflective aside and 0 of 12 baseline
outputs did; after it, 0 and 0, with the pass rate at 96% against 89%.
