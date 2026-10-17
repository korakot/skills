---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when discussing a project's or wiki's terminology, defining or renaming a term, writing or editing a GLOSSARY.md, or recording or editing an ADR.
---

# Domain Modeling

Actively build and sharpen the project's domain model as you design. This is the *active* discipline: challenging terms, inventing edge-case scenarios, and writing the glossary and decisions down once they crystallise. (Merely *reading* `GLOSSARY.md` for vocabulary is not this skill: that's a one-line habit any skill can do. This skill is for when you're changing the model, not just consuming it.)

## File structure

Most repos have a single context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `GLOSSARY-MAP.md` exists at the root, the repo has multiple contexts. The map points to where each one lives:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files lazily: only when you have something to write. If no `GLOSSARY.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with the existing language in `GLOSSARY.md`, call it out immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses vague or overloaded terms, propose a precise canonical term. "You're saying 'account': do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When domain relationships are being discussed, stress-test them with specific scenarios. Invent scenarios that probe edge cases and force the user to be precise about the boundaries between concepts.

### Cross-reference with the repo

When the user states how something works, check whether the repo agrees: the code, or the wiki pages that already describe the concept. If you find a contradiction, surface it: "Your code cancels entire Orders, but you just said partial cancellation is possible. Which is right?" or "The alignment page uses 'anchor' for the source paragraph, but you're using it for the target. Which is it?"

### Update GLOSSARY.md when a term settles

A term is **settled** when the user states it plainly or accepts the term you proposed ("yes, call it X"). A term the user is still asking about ("is 'anchor' the right word?") is not settled: they want your view, so give it and wait. Writing while they are still weighing it hands them a file to check before they've decided anything.

Once a term settles, write it right then rather than batching to the end of the session, so nothing is lost if the session stops. Then say in one line what you wrote ("Added **Anchor** to the glossary: the source paragraph an index entry points into"), so the user can check it without opening the file. Use the format in [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md).

`GLOSSARY.md` should be totally devoid of implementation details. Do not treat `GLOSSARY.md` as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing else.

The first time you create `GLOSSARY.md` in a repo, also add one pointer line to the repo's `AGENTS.md` (or `CLAUDE.md`), such as "Read `GLOSSARY.md` before working here: it defines this repo's terms", and, if the repo has a `wiki/index.md`, one line there linking the glossary. Other sessions and skills only read the glossary when something points them to it; upstream does that through `docs/agents/domain.md`, which these repos don't have.

When a wiki page already explains the concept in depth, the glossary entry keeps only the tight definition and links that page. The page stays the one home for the detail; restating it in the glossary creates two copies that drift apart.

### Offer ADRs sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse**: the cost of changing your mind later is meaningful
2. **Surprising without context**: a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off**: there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. If the decision was made on a wayfinder ticket, the ticket's resolution comment is already its record: link the ticket from the relevant wiki page instead of writing a second copy as an ADR. Use the format in [ADR-FORMAT.md](./ADR-FORMAT.md).
