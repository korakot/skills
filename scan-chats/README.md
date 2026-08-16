# scan-chats

Walk through your past Claude.ai chats under cursor control — search a window of chats for something, or process every chat in it (classify, summarize, timeline…).

**Works with Claude Chat (claude.ai) only** — it drives the `recent_chats` tool, which doesn't exist in Claude Code or the API.

[ภาษาไทยด้านล่าง](#ภาษาไทย)

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

Download [`SKILL.md`](SKILL.md), then on Claude.ai go to **Settings → Customize → Skills → Add → Upload a skill** and select the file. That's it.

## Requirements

- Claude.ai with **Search and reference past chats** enabled
- Works in Claude Projects (scoped to project chats) and outside projects (scoped to non-project chats)

---

## ภาษาไทย

สกิลสำหรับไล่อ่านแชทเก่าใน Claude.ai อย่างเป็นระบบ — ค้นหาเรื่องที่ต้องการย้อนหลังทีละชุด หรือประมวลผลทุกแชทในช่วงที่กำหนด (จัดหมวด สรุป ทำไทม์ไลน์ ฯลฯ)

**ใช้ได้กับ Claude Chat (claude.ai) เท่านั้น** — สกิลนี้เรียกใช้เครื่องมือ `recent_chats` ซึ่งไม่มีใน Claude Code หรือ API

### ปัญหาที่แก้

`conversation_search` หาแชทเจอบ้างไม่เจอบ้างตามดวงของคีย์เวิร์ด แต่ถ้าต้องการความครอบคลุม เช่น "เดือนมีนาคมคุยเรื่อง X ไว้ในแชทไหนบ้าง" หรือ "จัดหมวด 100 แชทล่าสุด" ต้องไล่ย้อนประวัติทีละชุดแบบมี cursor ที่หยุดแล้วทำต่อได้ — สกิลนี้ทำหน้าที่นั้น

### วิธีใช้

ค้นหา (โหมดปกติ):

```
scan 100 chats for MCP server ideas
scan-chats since Feb for anything about the wiki migration
```

ประมวลผล (ใส่คำกริยาสั่งงาน เช่น classify, summarize):

```
scan 50 chats and classify by topic
scan chats in March and summarize
```

จบแต่ละรอบ Claude จะให้บรรทัดสำหรับ "ทำต่อ" (`scan N chats for X before '...'`) — วางในแชทเดิมหรือแชทใหม่ก็ได้ แล้วมันจะไล่ต่อจากจุดที่ค้างไว้พอดี

### วิธีติดตั้ง

ดาวน์โหลดไฟล์ [`SKILL.md`](SKILL.md) แล้วไปที่ Claude.ai: **Settings → Customize → Skills → Add → Upload a skill** เลือกไฟล์นั้น เท่านี้ก็ใช้ได้เลย

### สิ่งที่ต้องมี

- Claude.ai ที่เปิดใช้ **Search and reference past chats**
- ใช้ได้ทั้งใน Claude Projects (เห็นเฉพาะแชทในโปรเจกต์) และนอกโปรเจกต์ (เห็นเฉพาะแชทนอกโปรเจกต์)

---

## License

MIT
