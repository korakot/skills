#!/usr/bin/env python3
"""fix_thai_pdf.py — Fix Thai PDF text extraction (PUA CMap + micro-offset).

Fixes two bugs in Thai PDFs created with legacy Windows UPC fonts
(DilleniaUPC, IrisUPC, AngsanaNew, BrowalliaNew, etc.):

1. PUA Encoding: Rewrites ToUnicode CMap to map Private Use Area
   U+F700-F71A back to correct Thai Unicode per NECTEC/Microsoft WTT 2.0.
   Reference: https://linux.thai.net/~thep/th-otf/shaping.html

2. Position Collisions: Inserts micro-offset Td nudge after zero-width
   glyphs so text extractors sort combining marks correctly.
"""
import pikepdf, re, sys

# ─── NECTEC/Microsoft WTT 2.0 PUA Mapping ───────────────────────────
# These are POSITIONAL VARIANT glyphs, not simple offsets.
# Each PUA codepoint represents a standard Thai character rendered at a
# different position (shifted left, down, or down-left) depending on the
# consonant class (ascending, strict-descender, removable-descender).
PUA_TO_THAI = {
    # Descender-less consonants
    0xF700: 0x0E10,  # ฐ THO THAN (no descender, used when BV present)
    0xF70F: 0x0E0D,  # ญ YO YING (no descender, used when BV present)
    # Above-vowels shifted left (for ascending consonants ป ฝ ฟ ฬ)
    0xF701: 0x0E34,  # ิ  Left SARA I
    0xF702: 0x0E35,  # ี  Left SARA II
    0xF703: 0x0E36,  # ึ  Left SARA UE
    0xF704: 0x0E37,  # ื  Left SARA UEE
    0xF710: 0x0E31,  # ั  Left MAI HAN AKAT
    0xF711: 0x0E4D,  # ํ  Left NIKHAHIT
    0xF712: 0x0E47,  # ็  Left MAITAIKHU
    # Tone marks shifted down-left (ascending consonant + above vowel)
    0xF705: 0x0E48,  # ่  Down-left MAI EK
    0xF706: 0x0E49,  # ้  Down-left MAI THO
    0xF707: 0x0E4A,  # ๊  Down-left MAI TRI
    0xF708: 0x0E4B,  # ๋  Down-left MAI CHATTAWA
    0xF709: 0x0E4C,  # ์  Down-left THANTHAKHAT
    # Tone marks shifted down (tone without above vowel)
    0xF70A: 0x0E48,  # ่  Low MAI EK
    0xF70B: 0x0E49,  # ้  Low MAI THO
    0xF70C: 0x0E4A,  # ๊  Low MAI TRI
    0xF70D: 0x0E4B,  # ๋  Low MAI CHATTAWA
    0xF70E: 0x0E4C,  # ์  Low THANTHAKHAT
    # Tone marks shifted left (normal consonant + above vowel)
    0xF713: 0x0E48,  # ่  Left MAI EK
    0xF714: 0x0E49,  # ้  Left MAI THO
    0xF715: 0x0E4A,  # ๊  Left MAI TRI
    0xF716: 0x0E4B,  # ๋  Left MAI CHATTAWA
    0xF717: 0x0E4C,  # ์  Left THANTHAKHAT
    # Below-vowels shifted down (strict descender consonants ฎ ฏ)
    0xF718: 0x0E38,  # ุ  Low SARA U
    0xF719: 0x0E39,  # ู  Low SARA UU
    0xF71A: 0x0E3A,  # ฺ  Low PHINTHU
}

NUDGE = '0.01'


# ─── Fix 1: CMap PUA Repair ──────────────────────────────────────────

def fix_cmap_pua(cmap_bytes):
    """Parse a ToUnicode CMap, fix all PUA→Thai mappings, rebuild cleanly.

    Unlike simple regex replacement, this fully parses bfchar and bfrange
    sections, expands ranges that target PUA codepoints (since PUA→Thai
    mappings are non-contiguous), and rebuilds the CMap from scratch.

    Returns (new_cmap_bytes, count_of_fixed_mappings).
    """
    text = cmap_bytes.decode('latin-1')

    # ── Parse all existing mappings ──
    all_mappings = {}  # src_gid -> dst_unicode

    bfchar_pat = re.compile(r'<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>')

    for section in re.finditer(
        r'\d+\s+beginbfchar\s*(.*?)\s*endbfchar', text, re.DOTALL
    ):
        for m in bfchar_pat.finditer(section.group(1)):
            all_mappings[int(m.group(1), 16)] = int(m.group(2), 16)

    bfrange_pat = re.compile(
        r'<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>'
    )
    for section in re.finditer(
        r'\d+\s+beginbfrange\s*(.*?)\s*endbfrange', text, re.DOTALL
    ):
        for m in bfrange_pat.finditer(section.group(1)):
            start = int(m.group(1), 16)
            end = int(m.group(2), 16)
            dst = int(m.group(3), 16)
            for i in range(end - start + 1):
                all_mappings[start + i] = dst + i

    # ── Fix PUA targets ──
    fixed = 0
    for src, dst in list(all_mappings.items()):
        if dst in PUA_TO_THAI:
            all_mappings[src] = PUA_TO_THAI[dst]
            fixed += 1

    if fixed == 0:
        return cmap_bytes, 0

    # ── Extract codespace range from original ──
    cs_match = re.search(
        r'<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>\s*endcodespacerange', text
    )
    if cs_match:
        cs_start, cs_end = cs_match.group(1), cs_match.group(2)
    else:
        cs_start = f"{min(all_mappings):04X}"
        cs_end = f"{max(all_mappings):04X}"
    hex_len = max(len(cs_start), 4)

    # ── Rebuild CMap ──
    lines = [
        "/CIDInit /ProcSet findresource begin",
        "12 dict begin",
        "begincmap",
        "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) "
        "/Supplement 0 >> def",
        "/CMapName /Adobe-Identity-UCS def",
        "/CMapType 2 def",
        "1 begincodespacerange",
        f"<{cs_start}> <{cs_end}>",
        "endcodespacerange",
    ]

    sorted_maps = sorted(all_mappings.items())
    # CMap spec allows max 100 entries per bfchar section
    for chunk_start in range(0, len(sorted_maps), 100):
        chunk = sorted_maps[chunk_start:chunk_start + 100]
        lines.append(f"{len(chunk)} beginbfchar")
        for src, dst in chunk:
            lines.append(f"<{src:0{hex_len}X}> <{dst:04X}>")
        lines.append("endbfchar")

    lines.extend([
        "endcmap",
        "CMapName currentdict /CMap defineresource pop",
        "end",
        "end",
    ])
    return "\n".join(lines).encode('latin-1'), fixed


# ─── Fix 2: Micro-Offset (Td Nudge) ─────────────────────────────────

def get_zw_glyphs(font):
    """Extract set of zero-width glyph IDs from an Identity-H font."""
    enc = str(font.get("/Encoding", ""))
    if enc != "/Identity-H":
        return set()
    zw = set()
    desc = font.get("/DescendantFonts")
    if not desc:
        return zw
    w_arr = desc[0].get("/W")
    if not w_arr:
        return zw
    wl = list(w_arr)
    i = 0
    while i < len(wl):
        c = int(wl[i])
        i += 1
        if i >= len(wl):
            break
        nv = wl[i]
        if isinstance(nv, pikepdf.Array):
            for j, w in enumerate(nv):
                if int(w) == 0:
                    zw.add(c + j)
            i += 1
        else:
            ce = int(nv)
            i += 1
            if i >= len(wl):
                break
            w = int(wl[i])
            if w == 0:
                for x in range(c, ce + 1):
                    zw.add(x)
            i += 1
    return zw


def apply_nudge(content_bytes, font_zw):
    """Insert Td nudge after zero-width glyph Tj operations."""
    text = content_bytes.decode('latin-1')
    fc = [
        (m.start(), '/' + m.group(1))
        for m in re.finditer(r'/(\w+)\s+\d+\s+Tf', text)
    ]

    def get_font(pos):
        cur = None
        for fp, fn in fc:
            if fp < pos:
                cur = fn
            else:
                break
        return cur

    count = [0]

    def do_nudge(m):
        h = m.group(1)
        f = get_font(m.start())
        if not f or f not in font_zw:
            return m.group(0)
        if len(h) < 4:
            return m.group(0)
        last = int(h[-4:], 16)
        if last in font_zw[f]:
            count[0] += 1
            return m.group(0) + f'\n{NUDGE} 0 Td'
        return m.group(0)

    new = re.sub(r'<([0-9A-Fa-f]+)>Tj', do_nudge, text)
    return new.encode('latin-1'), count[0]


# ─── Main ────────────────────────────────────────────────────────────

def fix_thai_pdf(input_path, output_path, verbose=True):
    """Apply PUA CMap fix and micro-offset nudge to a Thai PDF."""
    pdf = pikepdf.open(input_path)
    tp, tn = 0, 0
    processed_streams = set()  # track by objgen to avoid double-fixing

    for pi in range(len(pdf.pages)):
        page = pdf.pages[pi]
        res = page.get("/Resources", {})
        fonts = res.get("/Font", {})

        # Fix 1: CMap PUA repair
        pp = 0
        for fn, fo in fonts.items():
            to_unicode = fo.get("/ToUnicode")
            if to_unicode:
                stream_id = to_unicode.objgen
                if stream_id in processed_streams:
                    continue
                processed_streams.add(stream_id)
                nc, c = fix_cmap_pua(to_unicode.read_bytes())
                if c > 0:
                    to_unicode.write(nc)
                    pp += c

        # Fix 2: Micro-offset nudge
        fzw = {}
        for fn, fo in fonts.items():
            zw = get_zw_glyphs(fo)
            if zw:
                fzw[str(fn)] = zw

        pn = 0
        contents = page.get("/Contents")
        if contents is None:
            streams = []
        elif isinstance(contents, pikepdf.Array):
            streams = list(contents)
        else:
            streams = [contents]

        for si, stream in enumerate(streams):
            data = stream.read_bytes()
            data, n = apply_nudge(data, fzw)
            pn += n
            if n > 0:
                if isinstance(contents, pikepdf.Array):
                    contents[si] = pdf.make_stream(data)
                else:
                    page["/Contents"] = pdf.make_stream(data)

        tp += pp
        tn += pn
        if verbose and (pp or pn):
            print(f"  Page {pi+1}: PUA={pp} nudges={pn}")

    pdf.save(output_path)
    pdf.close()
    if verbose:
        print(f"\nTotal: PUA_fixed={tp} nudges={tn}")
    return tp, tn


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_thai_pdf.py input.pdf [output.pdf]")
        print("  output defaults to input_fixed.pdf")
        sys.exit(1)
    inp = sys.argv[1]
    if len(sys.argv) > 2:
        out = sys.argv[2]
    else:
        out = inp.rsplit('.', 1)[0] + '_fixed.pdf'
    fix_thai_pdf(inp, out)
