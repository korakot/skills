---
name: refer-chat
description: Fetch a specific past chat by timestamp. Triggers when the user pastes "refer-chat YYYY-MM-DDTHH:MMZ" — a minute-level ISO timestamp from their bookmarklet. Also triggers when the user asks how to install the chat timestamp bookmarklet or how to reference past chats precisely.
---

# refer-chat

## When the user pastes a timestamp

Example: `refer-chat 2026-03-09T00:22Z`

Action: Call `recent_chats(n=1, before="2026-03-09T00:22Z")`. Use the timestamp directly — it's already rounded up by the bookmarklet.

## Bookmarklet setup

When the user asks about installation, read `scripts/bookmarklet.js` and guide them to create a bookmark with that code as the URL.

The bookmarklet extracts the current chat's `updated_at` from Claude.ai's React fiber tree, rounds up to the next minute, and copies `refer-chat YYYY-MM-DDTHH:MMZ` to clipboard. Works on claude.ai only.
