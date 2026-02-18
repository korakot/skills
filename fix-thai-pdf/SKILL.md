---
name: fix-thai-pdf
description: Fix Thai PDF text extraction issues caused by legacy UPC fonts (DilleniaUPC, IrisUPC, AngsanaNew, BrowalliaNew, etc.). Applies two fixes - (1) PUA CMap repair mapping Private Use Area U+F700-F71A back to correct Thai Unicode using the NECTEC/Microsoft WTT 2.0 standard mapping, and (2) micro-offset Td nudge after zero-width glyphs to fix position collisions that scramble character ordering. Use when user has Thai PDFs with garbled text extraction, missing tone marks, or scrambled diacritics.
---

# Fix Thai PDF

Fix text extraction from Thai PDFs created with legacy Windows UPC fonts.

## Problem

Thai PDFs created with Microsoft Office using DilleniaUPC, IrisUPC, AngsanaNew, BrowalliaNew, and related UPC font families have two systematic text extraction bugs:

1. **PUA Encoding**: Thai combining marks and certain consonant variants are stored as positional-variant glyphs in Private Use Area codepoints U+F700–F71A. These are NOT simple offsets of standard Thai — they are repositioned forms (shifted down, left, or down-left) used by the font's shaping engine for tall consonants (ป ฝ ฟ), descender-less consonants (ญ ฐ), and stacked mark combinations. Text extractors output the raw PUA codepoints, producing garbage.

2. **Position Collisions**: Thai combining marks (ั ิ ี ึ ื ุ ู ่ ้ ๊ ๋ ์ ํ) and repositioned consonant variants have zero advance width in the font. Text extractors sort characters by x-position, so zero-width marks collide with the next base character, scrambling the reading order (e.g. `ผู้ให้` → `ผใู้ห้`).

These issues affect a massive number of Thai PDFs from the 1990s through today: government documents, academic papers, legal filings, anything created with Microsoft Office using these fonts.

## Solution

Two PDF-level fixes applied with pikepdf (preserving exact visual rendering):

### Fix 1: CMap PUA Repair
Rewrites ToUnicode CMap entries in Identity-H fonts, replacing PUA destinations (U+F700–F71A) with correct Thai Unicode. The fix parses all `bfchar` and `bfrange` sections, expands any ranges that target PUA codepoints into individual `bfchar` entries (since PUA→Thai mappings are non-contiguous), then rebuilds the entire CMap cleanly.

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

## PUA Mapping Table (NECTEC/Microsoft WTT 2.0 Standard)

Source: [Thai Script Shaping](https://linux.thai.net/~thep/th-otf/shaping.html) by Theppitak Karoonboonyanan (NECTEC).

These are **positional variant glyphs** — the same Thai character rendered at different vertical/horizontal positions depending on the consonant class. The PUA codepoint encodes position, not identity.

### Descender-less consonants
| PUA    | Thai   | Char | Description                     |
|--------|--------|------|---------------------------------|
| U+F700 | U+0E10 | ฐ    | THO THAN without descender      |
| U+F70F | U+0E0D | ญ    | YO YING without descender       |

### Above-vowels shifted left (for ascending consonants ป ฝ ฟ ฬ)
| PUA    | Thai   | Char | Description        |
|--------|--------|------|--------------------|
| U+F701 | U+0E34 | ิ    | Left SARA I        |
| U+F702 | U+0E35 | ี    | Left SARA II       |
| U+F703 | U+0E36 | ึ    | Left SARA UE       |
| U+F704 | U+0E37 | ื    | Left SARA UEE      |
| U+F710 | U+0E31 | ั    | Left MAI HAN AKAT  |
| U+F711 | U+0E4D | ํ    | Left NIKHAHIT      |
| U+F712 | U+0E47 | ็    | Left MAITAIKHU     |

### Tone marks shifted down-left (for ascending consonants + above vowel)
| PUA    | Thai   | Char | Description              |
|--------|--------|------|--------------------------|
| U+F705 | U+0E48 | ่    | Down-left MAI EK         |
| U+F706 | U+0E49 | ้    | Down-left MAI THO        |
| U+F707 | U+0E4A | ๊    | Down-left MAI TRI        |
| U+F708 | U+0E4B | ๋    | Down-left MAI CHATTAWA   |
| U+F709 | U+0E4C | ์    | Down-left THANTHAKHAT    |

### Tone marks shifted down (for tone without above vowel)
| PUA    | Thai   | Char | Description          |
|--------|--------|------|----------------------|
| U+F70A | U+0E48 | ่    | Low MAI EK           |
| U+F70B | U+0E49 | ้    | Low MAI THO          |
| U+F70C | U+0E4A | ๊    | Low MAI TRI          |
| U+F70D | U+0E4B | ๋    | Low MAI CHATTAWA     |
| U+F70E | U+0E4C | ์    | Low THANTHAKHAT      |

### Tone marks shifted left (for normal consonant + above vowel)
| PUA    | Thai   | Char | Description          |
|--------|--------|------|----------------------|
| U+F713 | U+0E48 | ่    | Left MAI EK          |
| U+F714 | U+0E49 | ้    | Left MAI THO         |
| U+F715 | U+0E4A | ๊    | Left MAI TRI         |
| U+F716 | U+0E4B | ๋    | Left MAI CHATTAWA    |
| U+F717 | U+0E4C | ์    | Left THANTHAKHAT     |

### Below-vowels shifted down (for strict descender consonants ฎ ฏ)
| PUA    | Thai   | Char | Description          |
|--------|--------|------|----------------------|
| U+F718 | U+0E38 | ุ    | Low SARA U           |
| U+F719 | U+0E39 | ู    | Low SARA UU          |
| U+F71A | U+0E3A | ฺ    | Low PHINTHU          |

## Results on Test Document (พุทธธรรม index, 140 pages)

| Metric | Before | After |
|--------|--------|-------|
| PUA codepoints (471K chars) | ~13,000 | 0 |
| Thai text readable | ❌ garbled | ✅ correct |

Example: `มาสูชคติแหชง` → `มาสู่คติแห่ง` (F70A was ช, now correctly ่)

## Known Limitations

- Only fixes Identity-H encoded fonts (the main Thai text carriers). WinAnsi-encoded fonts in these PDFs typically carry only punctuation/numbers and do not use PUA.
- The PUA mapping table covers the 27 entries defined in the Microsoft Windows Thai PUA extension (WTT 2.0). Apple MacOS Thai fonts use a different PUA range (U+F880–F89E) which is not yet supported.
- Does not fix text-level issues (wrong character order already baked into extracted strings). This is a PDF-level fix that must be applied before extraction.

## Status

**v0.2 — Corrected PUA mapping.** v0.1 used a wrong simple-offset mapping (F7xx→0Exx) which mapped all 27 PUA entries to wrong Thai characters. v0.2 uses the authoritative NECTEC/Microsoft WTT 2.0 mapping. Tested on พุทธธรรม ฉบับปรับขยาย index (140 pages, 471K chars, 0 PUA remaining after fix).

Contributions welcome — see the GitHub repo for issues and PRs.
