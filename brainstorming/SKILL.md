---
name: brainstorming
description: Use when a task is open-ended or the user wants to settle on an approach before producing a deliverable. One question at a time, 2-3 alternatives with recommendation, approval before output.
---

<!-- Adapted from obra/superpowers (v5.1.0), CC-specifics removed. Applies to any creative work — code, writing, evals, plans, communications. -->

# Brainstorming

Help turn ideas into concrete approaches through collaborative dialogue. Start by understanding context, then ask questions one at a time to refine the idea. Once direction is clear, present an approach and get user approval before producing the deliverable.

<HARD-GATE>
Do NOT produce the final deliverable (draft the doc, build the artifact, run the eval, write the code, generate the output) until you have presented an approach and the user has approved it. This applies to every project regardless of perceived simplicity.
</HARD-GATE>

## Anti-Pattern: "This Is Too Simple"

Every project goes through this. A short blog post, a single eval question, a quick email — all of them. "Simple" tasks are where unexamined assumptions cause the most wasted work. The agreed direction can be short (a sentence or two for truly small tasks), but it MUST be presented and approved.

## Checklist

1. **Explore context** — check uploaded files, project files, prior chats if relevant
2. **Scope check** — if the task spans multiple independent pieces, surface that and propose decomposition before drilling into details
3. **Ask clarifying questions** — one at a time, multiple-choice preferred when possible. Focus on purpose, constraints, success criteria.
4. **Propose 2-3 approaches** — with trade-offs and your recommendation, lead with the one you'd pick
5. **Present the approach** — in sections scaled to complexity. Ask after each section whether it lands.
6. **Wait for approval** — explicit go-ahead before producing the final deliverable
7. **Self-review** — before declaring the approach final, scan for placeholders (TBD/TODO), internal contradictions, ambiguity (could a requirement be read two ways?), and scope creep. Fix inline.

## Process

**Understanding the idea:**

- Check the current state first — uploaded files, project context, recent chat history if relevant
- Before detailed questions, assess scope: if the request spans independent subsystems ("build a platform with chat, billing, and analytics" or "write a book covering A, B, C"), surface this and propose decomposition. Each piece gets its own brainstorm → approach → execution cycle.
- For appropriately-scoped tasks, ask questions one at a time
- Prefer multiple choice when possible, open-ended when the space is too large
- Only one question per message
- Focus on: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 approaches with trade-offs
- Lead with your recommended option and explain why
- Present conversationally; use a formal table only if complexity warrants it

**Presenting the approach:**

- Scale each section to complexity: a sentence or two for simple things, up to a few hundred words for nuanced ones
- Ask after each section whether it looks right
- Be ready to go back and clarify if something doesn't fit

**Visual content:**

For questions that genuinely benefit from visual treatment (layout choices, diagrams, side-by-side comparisons), use `show_widget` rather than describing in text. A topic being visual-adjacent (e.g. "what should the homepage say?") is not automatically a visual question — only use a widget when seeing it would land better than reading it.

## Key Principles

- **One question at a time** — don't overwhelm
- **Multiple choice preferred** — easier to answer than open-ended
- **YAGNI ruthlessly** — strip unnecessary features from any approach
- **Explore alternatives** — always 2-3 before settling
- **Incremental validation** — get approval section by section, not all at once
- **Be flexible** — go back and clarify when something doesn't fit

## After Approval

Produce the deliverable as agreed. The skill ends at approval — execution is whatever the task requires.
