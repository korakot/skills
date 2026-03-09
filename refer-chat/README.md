# refer-chat

Precision recall for Claude.ai conversations. Paste a timestamp, get the exact chat — one call, every time.

## Problem

Claude's `conversation_search` often misses chats (wrong keywords, vague matches). `recent_chats` requires guessing counts. This skill gives you **exact** recall via timestamps.

## How it works

1. **Bookmarklet** grabs the current chat's `updated_at` from Claude.ai's React internals, rounds up to the next minute, and copies `refer-chat 2026-03-09T00:22Z` to your clipboard.
2. **Skill** tells Claude: when you see `refer-chat <timestamp>`, call `recent_chats(n=1, before=timestamp)`. One call, exact match.

## Install the Skill

Download [`refer-chat.skill`](https://github.com/korakot/skills/releases/download/refer-chat-v1/refer-chat.skill) and upload it to Claude.ai. You'll see "Copy to your skills" — click it.

## Install the Bookmarklet

Create a new bookmark in your browser with this as the URL:

```
javascript:void(function(){var id=location.pathname.split('/chat/')[1],ts,el=document.querySelector('[data-testid="chat-title-button"]')||document.querySelector('a[href="/chat/'+id+'"]'),f=el&&Object.keys(el).find(function(k){return k.startsWith('__reactFiber$')})&&el[Object.keys(el).find(function(k){return k.startsWith('__reactFiber$')})];while(f&&!ts){var p=f.memoizedProps||{};for(var k in p){var v=p[k];if(v&&v.uuid===id&&v.updated_at){ts=v.updated_at;break}}f=f.return}if(ts){var d=new Date(ts);d.setMinutes(d.getMinutes()+1);ts='refer-chat '+d.toISOString().slice(0,16)+'Z';navigator.clipboard.writeText(ts);document.title=ts}else document.title='Not found'})()
```

## Usage

1. Open any chat on claude.ai
2. Click the bookmarklet — timestamp copied to clipboard
3. In a new (or any) chat, paste it: `refer-chat 2026-03-06T12:19Z`
4. Claude fetches the exact chat instantly

## Requirements

- Claude.ai with **Search and reference past chats** enabled
- Works in Claude Projects (scoped to project chats) and outside projects (scoped to non-project chats)

## License

MIT
