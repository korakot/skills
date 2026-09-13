---
name: decide
description: Use when 3+ items each need a decision — claim-by-claim synthesis, accept/reject options, multi-point recommendations, 'decide on each'. Skip if 1-2 items, one narrative, or final answer wanted.
---

# decide

A per-point review widget: the user decides on each of a set of claims, leaves per-point notes and one overall comment, and submits the whole batch back as structured text you fold into the next step.

## Why this exists: gen-verify

LLMs generate cheaply and humans verify slowly — verification is the bottleneck of iteration. This skill compresses verification: each row is a discrete decision the user would otherwise have to mentally extract from prose. Surfacing them as scannable units cuts seconds-per-claim into seconds-per-batch, so generate → verify → iterate runs fast enough to be worth doing. Reach for it whenever prose would force the user to do claim-extraction work the UI could do for them.

## When this skill applies

You are about to produce, or have just produced, multi-point synthesis — anything where the user needs to react to several distinct items:

- A decision framework with 8 rules — they should be able to accept some and reject others.
- A comparison of 5 options — they may want a few rows kept and a few dropped.
- A batch of backlog items to triage (resolve / drop).
- A recommendation list where each item has different evidence quality.
- A pile of items to sort into categories (now / later / never), which the same widget handles with category labels instead of verbs.
- A claim-by-claim review of synthesis you generated earlier in the chat.

When in doubt: if the next step is "user reads a list of claims and reacts to each", use this skill. Long prose with claims buried inside is the wrong shape — surface them in rows.

## Render it

`decide.js` from korakot/ui carries the whole widget. Call `mcp__visualize__show_widget` (HTML mode — the review is ephemeral, not a Live Artifact) with a script tag and your data:

```html
<script src="https://cdn.jsdelivr.net/gh/korakot/ui@main/decide.js"></script>
<pre class="decide" topic="skill descriptions" acts="claims">
Title of the point | one line of context | sourced · 2026-05-12
Second point | context, 1–2 lines at most | reasoning
Third point
</pre>
```

- One line per point: `title | context | tag`. Context and tag are optional; `#` starts a comment line.
- `topic` names the review; it comes back in the submission header.
- `acts` sets the buttons — a preset name (`claims` default, `triage`, `select`, `code`, see table below) or a custom `Label:description|…` with two to four of them. The description is what the legend shows, so write it as what the choice *means*.
- Pipes separate fields, so keep `|` out of the text. The block is HTML: escape `<` and `&` as entities.
- Rows start unselected and stay optional. Clicking the selected button again unselects it. An unclicked row with a note in it comes back as-is (the note carries the decision — no `SKIP` tag is stamped on it); an unclicked row left completely untouched is folded into one trailing `[SKIP]` line at the end of the batch, so a mostly-untouched review doesn't cost one line per row.
- Multiple `<pre class="decide">` blocks in one widget share a single Submit button (same convention as `ask.js`) — use this if you need more than one batch of rows reviewed before the next step.

Over 15 rows, batch: visual fatigue eats accuracy. Batch by category (sourced facts vs synthesis), by source, or by priority — render one widget, wait for the submission, then the next.

## Parse the submission and act

Submit sends you one line per row, then an optional overall comment:

```
Review of <topic>:
- [ACTION] <title> | Comment: <comment-or-(none)>
- <title> | <note>
- [SKIP] <title>, <title>, <title>

Overall comment:
<freeform meta-feedback>
```

Three line shapes, by how the row was left:
- **`[ACTION] title | Comment: ...`** — a button was clicked. Take the action (resolve → write the resolution back to the source, drop → remove the item). The comment is the user's note; when the action was Resolve, the comment often *is* the resolution and belongs wherever the item lives.
- **`title | note`** (no bracket, no verb) — nothing was clicked but the row has a note. The note itself is the response — a correction, a question, a "not as written" — act on it directly rather than treating it as skipped.
- **`[SKIP] title, title, ...`** — one compressed line listing every row that was left completely untouched (no click, no note). The user deferred these — leave them in place and don't ask about them individually.

The **Overall comment** block appears only when non-empty, and it is where structural problems surface ("several of these phrases describe what the skill does, not when to use it"). Address it explicitly and let it shape the next iteration.

Confirm what you did in chat, briefly. Don't re-render the widget unless asked.

## Presets and custom labels

| Preset | Slot 1 (teal) | Slot 2 (red) |
|---|---|---|
| `claims` (default) | Accept — take the claim as stated | Reject — drop the claim |
| `triage` | Resolve — close now; comment becomes resolution | Drop — stop tracking |
| `select` | Include — ship this option | Exclude — leave out |
| `code` | Apply — merge this change | Discard — close without merging |

The presets are pairs; a custom `acts` takes two to four. Use three or four when the review sorts items into categories rather than approving them — `Now:this sprint|Later:next quarter|Never:drop it` — and keep the strongest option in slot 1, since slot colors run teal, red, gray, blue regardless of label. A defer slot is never needed: an unclicked row already means defer.

## Anti-patterns

**Four buttons is the ceiling.** decide.js takes the first four labels and drops the rest; beyond that, rows get wide, scanning slows, and committing gets harder. If the choice genuinely has more branches, split the review or ask the question a different way.

**Keep context to 1–2 lines.** A point needing more explanation belongs in its own chat or document, not in a batch review.

**Render rows, not a prose checklist.** Inline checkboxes in prose are slower to scan and capture no notes.

**Hand-written review HTML is the old shape.** Everything visual is in decide.js now; emitting your own rows means a second copy that drifts.
