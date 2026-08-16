---
name: scan-chats
description: Walk through past chats under cursor control — search or process a window.
---

# scan-chats

Two modes, detected from the command.

## Modes

**Search** (default, no action verb). `scan-chats for X`, `scan 100 chats for X`, `scan-chats since Feb for X`. Walk back hunting for matches. Output = matches + borderlines.

**Process** (requires an action verb: `classify`, `summarize`, `list`, `extract`, `timeline`, `group`, `bucket`, etc.). `scan 100 chats and classify for X`, `scan chats in March and summarize`. Apply the verb to every chat in the window.

Detection: action verb present → Process. Otherwise → Search. Announce mode at turn 1. Always require criteria X — ask if missing.

## N (chat count)

N is chat count, not batch count. `scan 50 chats` = 20 + 20 + 10. `scan 17 chats` = 1 batch of 17.

Default N for Search = 100. Default for Process = the window if specified; otherwise ask.

## Windows

`in March`, `since Feb`, `from X to Y`, `before Z` attach to either mode. A window replaces N as the stop condition — traverse until the window is exhausted.

## Execution

Tool is `recent_chats(n=20, before=...)`. Auto-scopes to current chat location (inside project / outside). Confirm scope if ambiguous.

**User-driven single batch** (`scan 20 chats for X`, or any bare paging turn): one call per turn, end with paste-ready cursor.

**Autonomous runs** (Search with N > 20, multi-batch Process, windowed): chain calls within one turn until N reached or window exhausted. **Do not auto-stop on empty batches** — the user may be hunting something rare and willing to pay for the full N.

## Output density

Search, many matches (≥ 10): one-liner per match — `date · [title](url) · one-line reason`. Link = `https://claude.ai/chat/{uri}`.

Search, few matches (< 10): 2–3 sentences per match — what the chat was actually about, why it matched, anything distinctive. User decides whether to click.

Search borderlines: always one-liner regardless of count.

Process (classify): always one-liner, same format as Search many-match.

Process (other verbs): density dictated by the verb — summarize → prose, list → bullets, timeline → chronology.

Note context-explained gaps briefly when relevant (retreat, holiday, pre-migration).

## Cursor & resume

Next `before=` is oldest `updated_at` from the latest batch, second precision, microseconds dropped. No rounding.

End of any autonomous run: emit a paste-ready resume line:

```
scan <N> chats [and <verb>] for X before 'YYYY-MM-DDTHH:MM:SSZ'
```

User pastes as new message (keep prior answer) or edits old prompt (new branch). If the scan suggests a useful narrowing (matches clustered in one month, nothing found hinting at a criteria tweak), offer a Reframe variant alongside Continue.

User-driven single-batch mode: same paste-ready line at every turn — that's the cursor handoff.

Fully-traversed windowed runs: no Continue line (the window is the stop). Offer a Reframe if useful.

## Closing summary

Date range scanned, total chats seen, counts (matches + borderlines for Search; bucket counts for classify; or the requested shape for other Process verbs). Don't re-list inline entries — they're already the record.

## Don'ts

- Don't narrate the tool call ("let me search…"). Execute and classify.
- Don't chain batches in user-driven single-batch mode.
- Don't ask "should I continue?" — the user drives the cursor.
- Don't auto-stop Search on empty batches. Run the full N.
- Don't round timestamps.
- Don't skip the mode announcement on turn 1 or the paste-ready resume line at end of autonomous runs.
