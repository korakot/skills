#!/usr/bin/env python3
"""fix_thai_pdf.py — Fix Thai PDF text extraction (PUA CMap + micro-offset)."""
import pikepdf, re, sys

PUA_TO_THAI = {
    0xF700:0x0E00,0xF701:0x0E01,0xF702:0x0E02,0xF703:0x0E03,0xF704:0x0E04,
    0xF705:0x0E05,0xF706:0x0E06,0xF707:0x0E07,0xF708:0x0E08,0xF709:0x0E09,
    0xF70A:0x0E0A,0xF70B:0x0E0B,0xF70C:0x0E0C,0xF70D:0x0E0D,0xF70E:0x0E0E,
    0xF70F:0x0E0F,0xF710:0x0E10,0xF711:0x0E31,0xF712:0x0E34,0xF713:0x0E35,
    0xF714:0x0E36,0xF715:0x0E37,0xF716:0x0E47,0xF717:0x0E48,0xF718:0x0E49,
    0xF719:0x0E4A,0xF71A:0x0E4B,
}
NUDGE = '0.01'

def fix_cmap_pua(cmap_bytes):
    text = cmap_bytes.decode('latin-1')
    fixed = [0]
    def repl(m):
        s, d = m.group(1), m.group(2)
        dv = int(d, 16)
        if dv in PUA_TO_THAI:
            fixed[0] += 1
            return f'<{s}> <{PUA_TO_THAI[dv]:04X}>'
        return m.group(0)
    def fix_bfchar(m):
        return 'beginbfchar\n' + re.sub(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', repl, m.group(1)) + 'endbfchar'
    text = re.sub(r'beginbfchar\n(.*?)endbfchar', fix_bfchar, text, flags=re.DOTALL)
    def fix_bfrange(m):
        rt = re.search(r'beginbfrange\n(.*?)endbfrange', m.group(0), re.DOTALL).group(1)
        ranges = re.findall(r'<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>', rt)
        nr, ec = [], []
        for sh, eh, dh in ranges:
            s, e, d = int(sh,16), int(eh,16), int(dh,16)
            if not any((d+o) in PUA_TO_THAI for o in range(e-s+1)):
                nr.append(f'<{sh}> <{eh}> <{dh}>')
            else:
                i = 0
                while i <= e-s:
                    dv = d+i
                    if dv in PUA_TO_THAI:
                        ec.append(f'<{s+i:04X}> <{PUA_TO_THAI[dv]:04X}>')
                        fixed[0] += 1; i += 1
                    else:
                        rs = i
                        while i <= e-s and (d+i) not in PUA_TO_THAI: i += 1
                        nr.append(f'<{s+rs:04X}> <{s+i-1:04X}> <{d+rs:04X}>')
        r = ''
        if nr: r += f'{len(nr)} beginbfrange\n' + '\n'.join(nr) + '\nendbfrange\n'
        if ec: r += f'{len(ec)} beginbfchar\n' + '\n'.join(ec) + '\nendbfchar\n'
        return r
    text = re.sub(r'\d+\s+beginbfrange\n.*?endbfrange', fix_bfrange, text, flags=re.DOTALL)
    return text.encode('latin-1'), fixed[0]

def get_zw_glyphs(font):
    enc = str(font.get("/Encoding", ""))
    if enc != "/Identity-H": return set()
    zw = set()
    desc = font.get("/DescendantFonts")
    if not desc: return zw
    w_arr = desc[0].get("/W")
    if not w_arr: return zw
    wl = list(w_arr); i = 0
    while i < len(wl):
        c = int(wl[i]); i += 1
        if i >= len(wl): break
        nv = wl[i]
        if isinstance(nv, pikepdf.Array):
            for j, w in enumerate(nv):
                if int(w) == 0: zw.add(c+j)
            i += 1
        else:
            ce = int(nv); i += 1
            if i >= len(wl): break
            w = int(wl[i])
            if w == 0:
                for x in range(c, ce+1): zw.add(x)
            i += 1
    return zw

def apply_nudge(content_bytes, font_zw):
    text = content_bytes.decode('latin-1')
    fc = [(m.start(), '/'+m.group(1)) for m in re.finditer(r'/(\w+)\s+\d+\s+Tf', text)]
    def get_font(pos):
        cur = None
        for fp, fn in fc:
            if fp < pos: cur = fn
            else: break
        return cur
    count = [0]
    def do_nudge(m):
        h = m.group(1)
        f = get_font(m.start())
        if not f or f not in font_zw: return m.group(0)
        if len(h) < 4: return m.group(0)
        last = int(h[-4:], 16)
        if last in font_zw[f]:
            count[0] += 1
            return m.group(0) + f'\n{NUDGE} 0 Td'
        return m.group(0)
    new = re.sub(r'<([0-9A-Fa-f]+)>Tj', do_nudge, text)
    return new.encode('latin-1'), count[0]

def fix_thai_pdf(input_path, output_path, verbose=True):
    pdf = pikepdf.open(input_path)
    tp, tn = 0, 0
    for pi in range(len(pdf.pages)):
        page = pdf.pages[pi]
        res = page.get("/Resources", {})
        fonts = res.get("/Font", {})
        pp = 0
        for fn, fo in fonts.items():
            if "/ToUnicode" in fo:
                nc, c = fix_cmap_pua(fo["/ToUnicode"].read_bytes())
                if c > 0: fo["/ToUnicode"] = pdf.make_stream(nc); pp += c
        fzw = {}
        for fn, fo in fonts.items():
            zw = get_zw_glyphs(fo)
            if zw: fzw[str(fn)] = zw
        pn = 0
        contents = page.get("/Contents")
        streams = list(contents) if isinstance(contents, pikepdf.Array) else [contents] if contents else []
        for si, stream in enumerate(streams):
            data = stream.read_bytes()
            data, n = apply_nudge(data, fzw)
            pn += n
            if n > 0:
                if isinstance(contents, pikepdf.Array):
                    contents[si] = pdf.make_stream(data)
                else:
                    page["/Contents"] = pdf.make_stream(data)
        tp += pp; tn += pn
        if verbose and (pp or pn):
            print(f"  Page {pi+1}: PUA={pp} nudges={pn}")
    pdf.save(output_path)
    pdf.close()
    if verbose:
        print(f"\nTotal: PUA_fixed={tp} nudges={tn}")
    return tp, tn

if __name__ == '__main__':
    inp = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/index_sample_5pages.pdf'
    out = sys.argv[2] if len(sys.argv) > 2 else '/home/claude/index_sample_fixed.pdf'
    fix_thai_pdf(inp, out)
