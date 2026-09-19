Vendored from https://github.com/cursor/plugins
Upstream: pstack/skills/unslop
File: SKILL.md -> skills/unslop/SKILL.md
Commit: e8d856f0273b42ebafe0ec3546bd645709e7c1b0 (2026-09-07)
Merge: three-way
Pulled: 2026-09-19
License: MIT (pstack/LICENSE, Lauren Tan)
Lineage: Wikipedia "Signs of AI writing", then blader/humanizer (MIT, Siqi Chen), then poteto/noodle, then cursor/plugins pstack

The lines above are read by scripts/upstream. `Upstream:` is the
directory the pin tracks, `File:` the vendored file as UPSTREAM_NAME ->
LOCAL_PATH, `Commit:` the newest upstream commit to that directory when
the file was last merged, and `Merge: three-way` means a pull runs `git
merge-file` with the pinned upstream version as base, so only upstream's
changes after the pin come in.

## Kept, dropped, added

The shipped file is upstream e8d856f with these differences. Upstream's
99559f2 (2026-08-02) is the version the kept parts come from; 73f8be4
(2026-09-01) added the model-invocation flag; e8d856f (2026-09-07) was a
density pass.

Dropped from e8d856f:
- `disable-model-invocation: true` in the frontmatter, so the agent
  applies the skill on its own instead of waiting for `/unslop`.
- The line "Rule numbers are stable ids that other skills cite. A removed
  rule leaves a gap."

Kept from 99559f2, where e8d856f changed or removed them:
- The tagline "Edit text to remove AI patterns and add human voice."
- Process step 3, "Add soul", with the pointer reworded to "see 'Adding
  soul' below" (99559f2 said "see next section", and the Guards section
  now sits between).
- The "Adding soul" section.
- Rules 1 (Puffery), 2 (Name-dropping), 4 (Promotional language), 6
  (Formulaic challenges), and 21 (Cutoff disclaimers).
- Rule 13's longer wording, with the sentence on why parentheses are no
  better than em dashes.

Added:
- A Guards section after Process: facts and quoted text outrank the
  rules, and overcorrection into anti-slop register is itself a tell.
  The two bullets are near-verbatim from woerndl/unsloppify (MIT,
  "unsloppify contributors"), whose notice LICENSE carries.

Taken from e8d856f as upstream wrote them: rules 32 (Mannered prose) and
33 (Over-compression).

The research that chose these is in the wellactually repository under
unslop-and-writing-for-agents-skills, 2026-09-12.

To update: `scripts/upstream check` lists upstream commits since the pin
and shows the diff; `scripts/upstream pull` merges upstream's changes
since the pin into the file and moves the pin. Resolve any conflict
markers, check that the kept parts above survived, and commit.
