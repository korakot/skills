# Upstream and divergence

**Upstream:** [mattpocock/skills](https://github.com/mattpocock/skills) → `skills/engineering/domain-modeling/` (MIT, © 2026 Matt Pocock).

**Synced to:** upstream commit `49dd158` (2026-10-09). This folder's first commit is that upstream version verbatim, so `git diff <first commit> -- domain-modeling/` shows exactly what this fork changed.

## How to update from upstream

Diff upstream's `domain-modeling/` between the "synced to" commit and its HEAD, and apply each change unless it touches a divergence below. Bump "Synced to" when done.

## Divergences (and why)

1. **Glossary beside the entry point, not at the root** (SKILL.md "File structure"; GLOSSARY-FORMAT.md "Single vs multi-context"). Wiki repos keep `wiki/GLOSSARY.md` next to `wiki/index.md`, because that's where readers start. ADRs follow to `wiki/adr/`. Code repos with no wiki keep upstream's layout.
2. **Write when a term settles, not mid-discussion** (SKILL.md "Update GLOSSARY.md when a term settles"). Upstream writes "the moment" a term crystallises. Here "settled" means the user stated it or accepted the proposed term; a question is a request for comment. Each write is confirmed with a one-line gist, so the user can verify without opening the file.
3. **Link, don't restate** (SKILL.md, same section; GLOSSARY-FORMAT.md rules). When a wiki page already explains the concept, the glossary keeps the one-line definition and links the page, so the detail has one home.
4. **Cross-reference with the repo, not only code** (SKILL.md heading renamed). In wiki repos the existing pages are what a claim gets checked against.
5. **ADRs defer to wayfinder tickets** (SKILL.md "Offer ADRs sparingly", added sentence). A decision resolved on a ticket already has its record there.
6. **`_Also_` for other-language forms** (GLOSSARY-FORMAT.md, new rule and example). For Thai/English projects, an equivalent term in the other language is sanctioned, not to be avoided.
7. **"General programming concepts" generalised to "general concepts of the field"** (GLOSSARY-FORMAT.md rules), since most of these repos aren't code.
8. **Description** widened to wiki terminology and to defining or renaming a term, so it also triggers outside code work.
