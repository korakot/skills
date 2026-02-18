---
name: fix-thai-pdf
description: Fix Thai PDF text extraction issues caused by legacy UPC fonts (DilleniaUPC, IrisUPC, AngsanaNew, BrowalliaNew, etc.). Applies two fixes - (1) PUA CMap repair mapping Private Use Area U+F700-F71A back to correct Thai Unicode, and (2) micro-offset Td nudge after zero-width glyphs to fix position collisions that scramble character ordering. Use when user has Thai PDFs with garbled text extraction, missing consonants, or scrambled diacritics.
---

# Fix Thai PDF

Fix text extraction from Thai PDFs created with legacy Windows UPC fonts.

## Problem

Thai PDFs created with Microsoft Office using DilleniaUPC, IrisUPC, AngsanaNew, BrowalliaNew, and related UPC font families have two systematic text extraction bugs:

1. **PUA Encoding**: Repositioned glyph variants (for tall consonants like ช ซ ฎ ฐ and shifted combining marks) are stored as Private Use Area codepoints U+F700–F71A instead of standard Thai Unicode. Text extractors output garbage characters.

2. **Position Collisions**: Thai combining marks (ั ิ ี ึ ื ุ ู ่ ้ ๊ ๋ ์ ํ) and repositioned consonant variants have zero advance width in the font. Text extractors sort characters by x-position, so zero-width marks collide with the next base character, scrambling the reading order (e.g. `ผู้ให้` → `ผใู้ห้`).

These issues affect a massive number of Thai PDFs from the 1990s through today: government documents, academic papers, legal filings, anything created with Microsoft Office using these fonts.

## Solution

Two PDF-level fixes applied with pikepdf (preserving exact visual rendering):

### Fix 1: CMap PUA Repair
Rewrites ToUnicode CMap entries in Identity-H fonts, replacing PUA destinations (U+F700–F71A) with correct Thai Unicode (U+0E00–0E4B). Handles both `bfchar` and `bfrange` sections, splitting ranges that span PUA boundaries.

### Fix 2: Micro-Offset (Td Nudge)
Inserts `0.01 0 Td` after every zero-width glyph's `Tj` operation in Identity-H font content streams. This advances the text matrix by 0.01 text-space units (~0.05mm at 14pt — invisible to the eye) but breaks position ties so extractors sort characters correctly.

## Usage

```bash
pip install pikepdf pdfplumber
python fix_thai_pdf.py input.pdf output.pdf
```

## Dependencies

- `pikepdf` — PDF content stream and CMap modification
- `pdfplumber` — verification only (optional, not needed for the fix itself)

## PUA Mapping Table

| PUA | Thai | Char | PUA | Thai | Char |
|------|------|------|------|------|------|
| F700 | 0E00 | — | F710 | 0E10 | ฐ |
| F701 | 0E01 | ก | F711 | 0E31 | ั |
| F702 | 0E02 | ข | F712 | 0E34 | ิ |
| F703 | 0E03 | ฃ | F713 | 0E35 | ี |
| F704 | 0E04 | ค | F714 | 0E36 | ึ |
| F705 | 0E05 | ฅ | F715 | 0E37 | ื |
| F706 | 0E06 | ฆ | F716 | 0E47 | ็ |
| F707 | 0E07 | ง | F717 | 0E48 | ่ |
| F708 | 0E08 | จ | F718 | 0E49 | ้ |
| F709 | 0E09 | ฉ | F719 | 0E4A | ๊ |
| F70A | 0E0A | ช | F71A | 0E4B | ๋ |
| F70B | 0E0B | ซ | | | |
| F70C | 0E0C | ฌ | | | |
| F70D | 0E0D | ญ | | | |
| F70E | 0E0E | ฎ | | | |
| F70F | 0E0F | ฏ | | | |

## Results on Test Sample (5 pages from พุทธธรรม index)

| Metric | Before | After |
|--------|--------|-------|
| PUA codepoints | 711 | 0 |
| Position collisions | 930 | 1 |

The 1 remaining collision is a double-stacked zero-width pair (ู + ช variant) on the same host consonant — both get the same nudge so they still tie.

## Known Limitations

- Only fixes Identity-H encoded fonts (the main Thai text carriers). WinAnsi-encoded fonts in these PDFs typically carry only punctuation/numbers.
- The PUA mapping table covers the 27 entries found in DilleniaUPC/UPC family. Other legacy Thai fonts may use different PUA ranges.
- Does not fix text-level issues (wrong character order already baked into extracted strings). This is a PDF-level fix.

## Status

**v0.1 — First working version.** Tested on a single document (พุทธธรรม ฉบับปรับขยาย index, 140 pages). Needs testing on more Thai PDFs with different font combinations.

Contributions welcome — see the GitHub repo for issues and PRs.
