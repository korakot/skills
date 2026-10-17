# Upstream and divergence

**Upstream:** [mattpocock/skills](https://github.com/mattpocock/skills) → `skills/engineering/wayfinder/` (MIT, © 2026 Matt Pocock).

**Synced to:** upstream commit `49dd158` (2026-10-09). The last upstream change to wayfinder in it is `8295b8e` (2026-10-07): wayfinder-only labels, real ids in cross-references, no research PRs, resolve by label type.

**History of this fork:**
- Before 2026-08-19: first adapted for Claude Chat + Linear. That copy is preserved as this folder's first commit ("record the installed Linear-tracker version").
- 2026-10-17: re-based onto upstream `49dd158`, with the tracker switched from Linear to GitHub issues.

## How to update from upstream

Diff upstream's `SKILL.md` between the "synced to" commit and its current HEAD, then apply each upstream change here unless it touches one of the divergences below. `SKILL.md` keeps upstream wording everywhere else, so most changes apply as-is. For the GitHub operations, also diff upstream's `setup-matt-pocock-skills/issue-tracker-github.md` ("Wayfinding operations"), which `TRACKER.md` adapts. Bump "Synced to" when done.

## Divergences (and why)

Each one names where it sits, so an upstream edit to that spot can be judged rather than pasted over.

1. **Tracker is fixed to GitHub issues** (SKILL.md "The Map", tracker paragraph → `TRACKER.md`). Upstream reads a per-repo tracker doc made by `/setup-matt-pocock-skills`. This fork has no setup skill, works across many repos, and runs from Claude Chat as well as Claude Code, so the operations live beside the skill. `TRACKER.md` adds what upstream leaves to setup: which repo a map belongs in, the roster, label creation, and GitHub MCP fallbacks.
2. **Research resolves to a resolution comment, not a branch** (Ticket Types → Research; Chart step 5). Upstream's `research` skill writes a Markdown file on a throwaway `research/<name>` branch. Here the findings go in the ticket's comment so any tool reading the issue sees them. Subagents are the default; the Claude Chat launch link is the fallback where there are no subagents.
3. **Prototype asset wording** (Ticket Types → Prototype). Names a published artifact URL or committed file, plus an optional session pointer.
4. **Home repo picked during charting** (Chart step 1). Replaces the earlier Linear team routing.
5. **Roster line** (Chart step 6, new). Cross-repo discovery, since maps are spread over many repos.
6. **Self-contained resolution comment, and the three resolve writes as one action** (Work step 4, added sentences). Guards against the most common failure seen in use: closing a ticket without the map line.
7. **Stall check** (end of Work section, new paragraph). Flags maps that keep deciding without producing output.

Not carried over from the Linear version: the Linear workspace and team routing (replaced by divergence 4 and the routing note in `TRACKER.md`), and memory-file pointers (generalised into the roster).

`domain-modeling` is used as upstream does (paired with every grilling call); this repo carries its own fork of it in [`../domain-modeling`](../domain-modeling).
