# wayfinder

Plan a piece of work too big for one session as a **map** of decision tickets on GitHub issues, then resolve them one at a time until the way to the destination is clear. It charts decisions, not deliverables: the map is done when nothing is left to decide.

A fork of Matt Pocock's [wayfinder](https://github.com/mattpocock/skills/tree/main/skills/engineering/wayfinder) (MIT), fixed to GitHub issues and adapted for working across many repos from Claude Code and Claude Chat. What differs and why: [`UPSTREAM.md`](UPSTREAM.md).

## Usage

User-invoked only:

```
/wayfinder <loose idea>          # chart a new map
/wayfinder <map issue URL>       # work the next frontier ticket
```

## Files

- [`SKILL.md`](SKILL.md): the method (upstream text plus marked divergences)
- [`github-ops.md`](github-ops.md): GitHub operations, which repo a map lives in, the roster
- [`UPSTREAM.md`](UPSTREAM.md): synced-to commit, divergence list, how to update

## Install

Claude.ai: download `wayfinder.skill` from a release or package this folder, then **Settings → Customize → Skills → Upload a skill**. Claude Code: copy the folder into `.claude/skills/`.
