# scan-chats

Walk through your past Claude.ai chats under cursor control — search a window of chats for something, or process every chat in it (classify, summarize, timeline…).

**Works with Claude Chat (claude.ai) only** — it drives the `recent_chats` tool, which doesn't exist in Claude Code or the API.

## Problem

`conversation_search` finds chats by keyword luck. When you need coverage — "which chats in March discussed X?", "classify my last 100 chats" — you want a systematic walk backward through history, batch by batch, with a resumable cursor. That's what this skill does.

## Usage

Search (default):

```
scan 100 chats for MCP server ideas
scan-chats since Feb for anything about the wiki migration
```

Process (any action verb):

```
scan 50 chats and classify by topic
scan chats in March and summarize
```

Each run ends with a paste-ready resume line (`scan N chats for X before '...'`) so you can continue exactly where it stopped — in the same chat or a fresh one.

## Install

Download this folder, zip it, rename to `scan-chats.skill`, and upload it to Claude.ai (Settings → Capabilities → Skills). You'll see "Copy to your skills" — click it.

## Requirements

- Claude.ai with **Search and reference past chats** enabled
- Works in Claude Projects (scoped to project chats) and outside projects (scoped to non-project chats)

## License

MIT
