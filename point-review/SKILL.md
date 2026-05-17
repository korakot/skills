---
name: point-review
description: Use when 3+ items each need a decision — claim-by-claim synthesis, accept/reject options, multi-point recommendations, 'decide on each'. Skip if 1-2 items, one narrative, or final answer wanted.
---

# point-review

A per-point review widget that lets the user accept/reject/skip each of a set of claims, leave per-point comments, and submit the whole batch back to you as structured feedback you fold into the next step.

## Why this exists: gen-verify

In Karpathy's Software 3.0 framing, LLMs generate cheaply and humans verify slowly — verification is the bottleneck of iteration. This skill compresses verification: each row is a discrete decision the user would otherwise have to mentally extract from prose. Surfacing them as scannable units cuts seconds-per-claim into seconds-per-batch, so generate → verify → iterate runs fast enough to be worth doing. Reach for it whenever prose would force the user to do claim-extraction work the UI could do for them.

## When this skill applies

You are about to produce, or have just produced, multi-point synthesis — anything where the user needs to react to several distinct items. Examples:

- A decision framework with 8 rules — they should be able to accept some and reject others.
- A comparison of 5 options across criteria — they may want a few rows kept and a few dropped.
- A batch of backlog items the user wants to triage (resolve / drop / keep).
- A recommendation list with several items, each with different evidence quality.
- A claim-by-claim review of synthesis you generated earlier in the chat.

When in doubt: if the next step is "user reads a list of claims and reacts to each", use this skill. Long prose with claims buried inside is the wrong shape — surface them in rows.

## What the widget looks like

The widget is an HTML page rendered via `mcp__visualize__show_widget`, **not** a Live Artifact — the review is ephemeral, one-shot, and shouldn't persist.

The widget has, top to bottom:

1. **Inline legend** — one line at the top showing each action label with a colored dot and a one-line description ("Resolve — close now; comment becomes resolution", etc.). This is required, not optional: verb labels alone don't always convey what the action does, especially when the verb pair is unfamiliar in context.
2. **Rows**, each containing:
   - **Title** — short label for the claim (14px, weight 500).
   - **Context** — 1–2 lines of supporting context, evidence, or origin (13px, secondary text color).
   - **Provenance chip** (optional) — small tag like `sourced · 2026-05-12`, `reasoning`, `guess`, `parked`, `followup`. 11px in a tinted pill.
   - **Comment input** — single-line text field for a per-row note. Full width within the row.
   - **Action buttons** — three buttons in a row: the verb pair you picked, e.g. `Resolve` / `Drop` / `Keep`. Right-aligned. One button is selected at a time per row.
3. **Overall comment textarea** — a multi-line freeform input below the rows for meta-feedback that doesn't belong on any single row. Often the most valuable feedback (e.g. "several of these phrases describe what the skill does, not when to use it") is meta to all rows and would be lost if there were only per-row inputs. Always include this textarea, even if you don't expect overall feedback — its absence is the kind of friction that surfaces too late.
4. **Submit button** and inline status message area.

## The data shape you accept

The caller (you, the model) passes in a list of points. Each point can have:

- `title` (required) — the claim itself, short and scannable.
- `context` (optional) — supporting detail. Keep to 1–2 lines; if you need more, the row probably shouldn't be in this widget.
- `tag` (optional) — provenance label. Examples: `sourced · 2026-05-12`, `reasoning`, `parked`, `followup`. Used to render the chip.
- `default` (optional) — pre-selected action. Only set this for items that are genuinely safe defaults (e.g., Anthropic-official sources for an Accept default). Most items should start with nothing selected.

## How to render the widget

### Step 1: Sizing check

If the list has more than 15 rows, **batch**. Don't render a 20-row widget — visual fatigue eats accuracy. Reasonable batch axes: by category (sourced facts vs synthesis), by source (this report vs that report), or by priority (committed followups vs parked items). Render the first widget, wait for submit, then the second.

### Step 2: Verify visual contract on first use (skip on subsequent uses in same session)

The selected/unselected visual state has historically been hard to make obviously visible. The first time you use this skill in a session, render a **2-row test widget** with real items from the list and ask the user "is the selected state unmistakable?" Only after they confirm, render the full review. On subsequent invocations in the same session, you can skip the test — the visual contract is already verified.

If the user reports the selection isn't visible, fall back to native `<input type="radio">` controls grouped per row. Custom styling is preferred when it works, but visibility wins over aesthetics.

### Step 3: Render the real widget

Use `mcp__visualize__show_widget` (HTML mode). The widget code template is in `assets/widget_template.html` — copy and substitute the rows list. Key invariants you must preserve:

- **Toggle colors**: Use the proven mid-ramp hex values for selected state. These work in both light and dark mode:
  - Resolve / Accept: `#0F6E56` (teal 600)
  - Drop / Reject: `#A32D2D` (red 600)
  - Keep / Skip: `#5F5E5A` (gray 600)
- **Redundant signal**: Add a `<i class="ti ti-check">` icon to the selected button so color is not the only cue. Some users have low-contrast modes or environment quirks; the icon is the safety net.
- **Unselected state**: transparent background, `var(--color-text-secondary)` text, `0.5px solid var(--color-border-tertiary)` border. Weight 400.
- **Selected state**: solid hex background, `#ffffff` text, no border (or matching hex border), weight 500.
- **Submit binding**: the Submit button must call `sendPrompt()` with a structured summary, not a free-form string. Use this format so you can parse it predictably on the return trip:
  ```
  Review of <topic>:
  - [ACTION] <title> | Comment: <comment-or-empty>
  - [ACTION] <title> | Comment: <comment-or-empty>
  ```
  Where ACTION is one of the action verbs you used.

### Step 4: Parse the response and act

When the widget submits, the user's selections come back as a `sendPrompt` message you receive. The format is:

```
Review of <topic>:
- [ACTION] <title> | Comment: <comment-or-(none)>
- [ACTION] <title> | Comment: <comment-or-(none)>

Overall comment:
<freeform meta-feedback>
```

Parse line by line. For each row:
- If ACTION was set, take the action (resolve → write resolution back to source, drop → remove item, keep → leave in place).
- The comment is the user's per-row note. If the action was Resolve, the comment often IS the resolution and should be folded into where the item lives.
- If ACTION is missing/none for a row, treat as "user skipped this; defer".

The **Overall comment** block (only present if non-empty) is meta-feedback that applies to the whole review. Treat it with high priority — it's often where the user surfaces a structural issue you missed (e.g. "several phrases are what-it-does framings, not when-to-use"). Don't bury it; address it explicitly in your response and let it shape the next iteration.

Confirm what you did in chat, briefly. Don't re-render the widget unless explicitly asked.

## Anti-patterns

**Don't render claims as a prose checklist with checkboxes inline.** That's slower for the user than the widget and doesn't capture comments.

**Don't pre-select Resolve/Accept on everything to be "helpful".** This biases the review. Only pre-select when the item has genuinely earned a default (sourced from authoritative reference, etc.). Most items start unselected.

**Don't use light tinted fills for the selected state** (`var(--color-background-success)` etc.). They've failed visibility tests twice. Use the solid mid-ramp hex values listed above.

**Don't add a fourth or fifth action button to be more nuanced.** Three actions cover almost every review (positive / negative / defer). More than three makes rows wider, harder to scan, and harder for the user to commit to.

**Don't embed long context in rows.** If a row needs more than 2 lines of explanation, the item probably belongs in a separate chat or document, not in a batch review.

## Default action verb conventions

Adapt action verb labels to the review type, but keep three slots and always pair each label with a 1-line legend description (the widget renders it at the top automatically):

| Use case | Positive (teal) | Negative (red) | Defer (gray) |
|---|---|---|---|
| Synthesis review (claims) | Accept — take the claim as stated | Reject — drop the claim | Skip — defer; revisit later |
| Backlog triage | Resolve — close now; comment becomes resolution | Drop — stop tracking | Keep — leave as-is |
| Feature/option selection | Include — ship this option | Exclude — leave out | Maybe — needs more info |
| Code review batch | Apply — merge this change | Discard — close without merging | Defer — needs follow-up |

The skill's CSS colors stay the same regardless of label — teal for positive, red for negative, gray for defer. Pass labels and descriptions as parallel arrays (`ACTION_LABELS` and `ACTION_DESCRIPTIONS`) to the widget template.

## Worked example

Earlier this session I needed to render a 5-row test widget for a synthesis review. The pattern:
1. Pass 5 rows with titles + 1-line context each + provenance tags.
2. Render via show_widget using the template.
3. User clicked Accept on 3, Reject on 1, Skip on 1, with a comment on one rejected row explaining the reason.
4. The skill parsed the submission and the model folded accepts into the main document, dropped the rejected claim, and queued the skipped one as a followup with the comment as context.

See `assets/widget_template.html` for the HTML scaffold.
