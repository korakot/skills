# Upstream and divergence

**Upstream:** [mattpocock/skills](https://github.com/mattpocock/skills) → `skills/productivity/grilling/` (MIT, © 2026 Matt Pocock).

**Synced to:** upstream commit `49dd158` (2026-10-09). The last upstream change to grilling in it is `95249b0` (2026-10-07): word questions so "yes" accepts the recommendation. This folder's first commit is that upstream version verbatim, so `git diff <first commit> -- grilling/` shows exactly what this fork changed.

**Before this fork (to 19 Oct 2026),** Kora's installed grilling was an older upstream version (before `a4b2009`, 31 Jul 2026) that asked one question at a time and asked for ambiguous terms to be defined first. Upstream moved to rounds; the term-definition step now lives in [domain-modeling](../domain-modeling).

## How to update from upstream

Diff upstream's `skills/productivity/grilling/` between the "synced to" commit and its HEAD, and apply each change unless it touches the divergence below. Upstream changes this skill's round format often (seven commits between 31 Jul and 7 Oct 2026), so check the one paragraph below against each new format. Bump "Synced to" when done.

## Divergence (and why)

1. **Rounds of three or more questions render as a point-review widget** (SKILL.md, the paragraph after "Word each question so 'yes' accepts…"). Kora reads long numbered messages slowly; deciding row by row and submitting once is cheaper. The fit is exact: upstream's "yes accepts the recommendation" is point-review's Accept, Reject or a note is his own answer, and an untouched row is deferred, so it stays on the frontier. Hosts without widgets keep upstream's markdown format. Named explicitly here because a second skill is rarely loaded mid-flow unless the first one names it.
