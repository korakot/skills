# decide

Decide on many items at once. When Claude hands you 3+ things that each need a call — claims to accept or reject, options to keep or drop, a list to triage — this skill renders them as a widget: a button per row, an optional note per row, one overall comment, one Submit. Claude then acts on the whole batch.

**Claude Chat (claude.ai) only** — it renders through the Visualizer (`show_widget`), which Claude Code and the API don't have.

[ภาษาไทย](#ภาษาไทย)

## Usage

Triggers on its own for multi-point synthesis, or ask:

```
decide on each of these
triage this list — now / later / never
```

Presets: `claims` (Accept/Reject), `triage` (Resolve/Drop), `select` (Include/Exclude), `code` (Apply/Discard), or 2–4 custom labels. Untouched rows are deferred, not rejected.

## Install

Download [`SKILL.md`](SKILL.md) → Claude.ai **Settings → Customize → Skills → Add → Upload a skill**.

Requires Visualizer enabled. The widget itself is [`decide.js`](https://github.com/korakot/ui/blob/main/decide.js) in [korakot/ui](https://github.com/korakot/ui) (spec: [`decide.md`](https://github.com/korakot/ui/blob/main/decide.md)).

---

## ภาษาไทย

ตัดสินใจหลายข้อพร้อมกัน — เมื่อ Claude ส่งรายการ 3 ข้อขึ้นไปให้ตัดสิน (ยอมรับ/ปฏิเสธ เก็บ/ทิ้ง จัดลำดับ) สกิลนี้แสดงเป็นวิดเจ็ต: ปุ่มต่อแถว โน้ตต่อแถว ความเห็นรวมหนึ่งช่อง Submit ทีเดียว แล้ว Claude ทำตามทั้งชุด

**ใช้ได้กับ Claude Chat (claude.ai) เท่านั้น** — แสดงผ่าน Visualizer (`show_widget`)

### วิธีใช้

ทำงานเองเมื่อมีหลายข้อให้ตัดสิน หรือสั่งตรง:

```
ให้ตัดสินทีละข้อ
จัดลำดับรายการนี้ — ทำเลย / ไว้ก่อน / ไม่ทำ
```

ชุดปุ่ม: `claims` (ยอมรับ/ปฏิเสธ), `triage` (แก้แล้ว/ทิ้ง), `select` (รวม/ไม่รวม), `code` (ใช้/ทิ้ง) หรือกำหนดเอง 2–4 ปุ่ม แถวที่ไม่กดถือว่าพักไว้ ไม่ใช่ปฏิเสธ

### ติดตั้ง

ดาวน์โหลด [`SKILL.md`](SKILL.md) → Claude.ai **Settings → Customize → Skills → Add → Upload a skill** (ต้องเปิด Visualizer)

---

## License

MIT
