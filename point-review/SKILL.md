---
name: point-review
description: Use when 3+ items each need a decision — claim-by-claim synthesis, accept/reject options, multi-point recommendations, 'decide on each'. Skip if 1-2 items, one narrative, or final answer wanted.
---

# point-review

A per-point review widget: the user decides on each of a set of items, leaves per-point notes and one overall comment, and submits the batch back as structured text you act on.

## Use it when

- The user needs to react to several distinct items — claims to accept or reject, options to keep or drop, a backlog to triage, a pile to sort into now / later / never.
- You are about to emit multi-point synthesis, or are revisiting synthesis from earlier in the chat.
- Over 15 rows, batch it: render one widget, wait for the submission, then the next.

Wrong shape: one or two items, a single narrative, or a request for your final answer. Long prose with claims buried inside is wrong too — surface them as rows.

## Render it

Call `mcp__visualize__show_widget` in HTML mode — the review is ephemeral, not a Live Artifact. Two input forms, one widget:

**Rich mode** — the default for anything non-trivial. Any element with a `review` attribute becomes a point; its content is whatever makes the judgment easiest — a paragraph, a table, a `mm.js` / `cy.js` diagram (load that script too). `title` is the short decidable statement; `topic` and `acts` sit on a wrapper and are inherited.

```html
<script src="https://cdn.jsdelivr.net/gh/korakot/ui@main/points.js"></script>
<script src="https://cdn.jsdelivr.net/gh/korakot/ui@main/mm.js"></script>
<div topic="auth redesign" acts="claims">
  <div review title="Token refresh matches the spec">
    <pre class="mm">sequenceDiagram; Client->>Server: refresh; Server-->>Client: 200</pre>
  </div>
  <div review title="Latency budget is realistic">
    <p>Measured p95 is 180 ms against a 250 ms budget; the 70 ms headroom covers the extra hop.</p>
  </div>
</div>
```

**Line mode** — shorthand for atomic items (rename this, drop that):

```html
<script src="https://cdn.jsdelivr.net/gh/korakot/ui@main/points.js"></script>
<pre class="points" topic="skill descriptions" acts="claims">
Title of the point | one line of context
Second point | context — as much as the reader needs to decide
Third point
</pre>
```

- One line per point: `title | context` — the same two-field shape as ask.js. Context is everything after the first `|`; `#` comments a line out; escape `<` and `&`.
- Context length has one test: could the reader decide this row without asking a follow-up? If not, it is too short. A few sentences is normal — what the claim rests on, what changes if accepted, what the alternative was. Thin context is the main reason reviews stall. If the explanation wants formatting or a picture, move that point to rich mode.
- Don't add a third field. If provenance matters for a particular row, lead the context with it (`inferred: …`); when every row shares a source, say nothing.
- Pick granularity by what is being decided: one diagram with one verdict when the whole is the decision; several small points when the parts are.
- `topic` names the review and comes back in the submission header.
- `acts` — a preset (`claims` default, `triage`, `select`, `code`) or two to four custom labels, e.g. `Now|Later|Never`. The legend shows a colored dot and the label, nothing else, so each label has to carry its own meaning. Slot colors run teal, red, gray, blue — strongest option first.
- `lang="th"` / `lang="en"` sets the widget's own copy; omit it and Thai is detected from the topic and rows. Write the rows in the user's language and the UI follows.
- Every button is optional, and an untouched row means defer. Each row has an Explain ↗ button that sends `Explain this point: <title> (review of <topic>)` to chat — answer it and let the user return to the open review; don't re-render.
- Everything in one widget shares a single Submit; points are grouped into sections by `topic`.

| Preset | Slot 1 | Slot 2 |
|---|---|---|
| `claims` | Accept / ยอมรับ | Reject / ปฏิเสธ |
| `triage` | Resolve / แก้แล้ว | Drop / ทิ้ง |
| `select` | Include / รวม | Exclude / ไม่รวม |
| `code` | Apply / ใช้ | Discard / ทิ้ง |

## Act on the submission

```
Review of <topic>:
- [ACTION] <title> | Comment: <comment-or-(none)>
- <title> | <note>
- [SKIP] <title>, <title>, <title>

Overall comment:
<freeform meta-feedback>
```

- `[ACTION] title | Comment: …` — a button was clicked; take the action. When it was Resolve, the comment usually *is* the resolution and belongs wherever the item lives.
- `title | note` — nothing clicked, but a note was left. The note is the response — a correction, a question, a "not as written". Act on it rather than treating the row as skipped.
- `[SKIP] title, …` — left completely untouched. Deferred: leave them in place, don't ask about them one by one.
- **Overall comment** appears only when non-empty, and is where structural problems surface. Address it explicitly and let it shape the next iteration.

The keys are always English; `ACTION` is the button label itself, so a Thai review returns `[ยอมรับ]`, `[แก้แล้ว]` and so on — map the label back to the preset. Confirm briefly what you did, and don't re-render unless asked.

## Keep in mind

Four buttons is the ceiling — points.js drops the rest silently, so split the review instead. The legend already says the buttons are optional, so don't re-explain the widget in your chat text. Never hand-write the footer or buttons: everything visual about the review lives in points.js, and a second copy drifts — rich mode is for the *content* of a point, not for redrawing the widget. Don't attach `review` to everything on the page: a footer only where a verdict is actually wanted back.

Full widget spec: https://github.com/korakot/ui/blob/main/points.md
