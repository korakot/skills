---
name: bia
description: Use when searching or reading works by Buddhadasa Bhikkhu (พุทธทาสภิกขุ). Triggers on mentions of Buddhadasa, พุทธทาส, อินทปัญโญ, สวนโมกข์, ธรรมโฆษณ์, BIA archive, BIA reference codes (BIA-...), or requests to search the Buddhadasa Indapanno Archives.
---

# BIA Archive

Buddhadasa Indapanno Archives (หอจดหมายเหตุพุทธทาส อินทปัญโญ) — publications and manuscripts by Buddhadasa Bhikkhu, accessed via a Cloudflare proxy at `https://bia-proxy.korakot.workers.dev`.

## Running queries

Use `bia.py` via bash for all queries. The script handles proxy routing, UUID resolution, and response cleaning.

```bash
python3 /mnt/skills/user/bia/bia.py search "อตัมม"
python3 /mnt/skills/user/bia/bia.py search "นิพพาน" --type publications --limit 12
python3 /mnt/skills/user/bia/bia.py read BIA-P02010000-0360-000-0_0000-00
python3 /mnt/skills/user/bia/bia.py read d2beb4c9-520c-4d9b-9f5e-864d98e767d2
```

**`search` options:**
- `--type publications|manuscripts` (default: both)
- `--limit N` (default: 12, max: 100)
- `--page N` (default: 1)
- `--year-start N` / `--year-end N` (Buddhist Era; default 0–2600)

**`read` ID:** accepts either a UUID or a referenceCode (auto-detected).

## Script output

Both subcommands return clean JSON. Always render as a widget afterward.

### search JSON
```json
{
  "query": "อตัมม",
  "total": 23, "page": 1, "totalPages": 2,
  "results": [
    {
      "title": "อตัมมยตาประยุกต์",
      "type": "publications",
      "dateDisplay": "พ.ศ. 2533",
      "pages": 350,
      "referenceCode": "BIA-P02010000-0360-000-0_0000-00",
      "url": "https://bia-archive.psu.ac.th/printed/BIA-P02010000-0360-000-0_0000-00"
    }
  ]
}
```

### read JSON
```json
{
  "title": "อตัมมยตาประยุกต์",
  "type": "publications",
  "dateDisplay": "พ.ศ. 2533 / ค.ศ. 1990",
  "pages": 350,
  "extent": "สิ่งพิมพ์บนกระดาษ ปกแข็ง จำนวน 350 หน้า",
  "description": "...",
  "referenceCode": "BIA-P02010000-0360-000-0_0000-00",
  "url": "https://bia-archive.psu.ac.th/printed/BIA-P02010000-0360-000-0_0000-00"
}
```

## Widget rendering

After running the script, render results as an inline widget using CSS variables for theming.

### Search widget

Responsive card grid: `repeat(auto-fill, minmax(180px, 1fr))`, gap 8px. Header shows query + total. Each card is an `<a href=url>`:
- Title: 14px/500, 2-line clamp
- Meta row: type icon (ti-book for publications, ti-pencil for manuscripts) + date at left; pages at **right** — both 12px secondary color
- RefCode: 10px **tertiary** mono, bottom of card

### Detail widget

Single full-width card:
- Title: 18px/500
- Meta strip (date · type · pages), bordered top/bottom, 13px secondary
- Extent row (if non-empty)
- Description: cleaned HTML, preserve `<p>` / `<ol>` / `<ul>` / `<li>` structure
- Footer: refCode (11px mono tertiary, left) + "Read on BIA" link (right)

## Notes

- **Date display**: `0000-00-00` → `ไม่ระบุปี`. Same start/end → `พ.ศ. YYYY`. Different → `พ.ศ. YYYY–YYYY`. Detail view adds `/ ค.ศ. YYYY`.
- **Types**: only `publications` (2,993 items) and `manuscripts` (1,408 items) exist in the archive.
- **`scopeAndContent`** is rich for publications; often empty for manuscripts. If empty in a `read` result, note this to the user and suggest clicking through to the scan.
- **Page images**: scanned only, no OCR. Not fetched in v1.
