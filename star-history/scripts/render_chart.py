#!/usr/bin/env python3
"""Render star history SVG chart as standalone HTML file.

Usage: python3 fetch_stars.py owner/repo | python3 render_chart.py [-o output.html] [--open]
       python3 render_chart.py -i data.json [-o output.html] [--open]

Reads JSON from fetch_stars.py (stdin or -i file), writes HTML with embedded SVG.
"""
import sys, json, argparse, math, webbrowser, os
from datetime import datetime

COLORS = ["#534AB7", "#1D9E75", "#D85A30", "#378ADD"]
FILL_OPACITY = "0.10"

# Chart area
X_MIN, X_MAX = 60, 680
Y_MIN, Y_MAX = 30, 330  # top=max stars, bottom=zero
W, H = 700, 400

def parse_date(s):
    return datetime.strptime(s[:10], "%Y-%m-%d")

def fmt_stars(n):
    if n >= 1000:
        v = n / 1000
        return f"{v:.1f}K" if v != int(v) else f"{int(v)}K"
    return str(n)

def date_label(d):
    return d.strftime("%b %y")  # e.g. "Mar 25"

def build_svg(repos):
    """Return SVG string for the star history chart."""
    # Collect all dates and find global max stars
    all_dates = []
    max_stars = 0
    for r in repos:
        for p in r["stars"]:
            all_dates.append(parse_date(p["date"]))
            max_stars = max(max_stars, p["cumulative"])
    if not all_dates or max_stars == 0:
        return '<svg viewBox="0 0 700 100" xmlns="http://www.w3.org/2000/svg"><text x="350" y="50" text-anchor="middle" font-size="14" fill="#888">No star data available</text></svg>'

    date_min = min(all_dates)
    date_max = max(all_dates)
    date_range = (date_max - date_min).total_seconds() or 1

    # Round max_stars up to nice number for Y axis
    def nice_max(v):
        if v <= 10: return 10
        mag = 10 ** (len(str(int(v))) - 1)
        return math.ceil(v / mag) * mag

    y_top = nice_max(max_stars)
    y_ticks = 5
    y_step = y_top / y_ticks

    def map_x(d):
        t = (parse_date(d) if isinstance(d, str) else d)
        frac = (t - date_min).total_seconds() / date_range
        return X_MIN + frac * (X_MAX - X_MIN)

    def map_y(v):
        return Y_MAX - (v / y_top) * (Y_MAX - Y_MIN)

    parts = []
    parts.append(f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" style="width:100%;max-width:720px;font-family:system-ui,-apple-system,sans-serif">')

    # Gradient defs
    parts.append("<defs>")
    for i, color in enumerate(COLORS[:len(repos)]):
        parts.append(f'<linearGradient id="g{i}" x1="0" y1="0" x2="0" y2="1">'
                     f'<stop offset="0%" stop-color="{color}" stop-opacity="{FILL_OPACITY}"/>'
                     f'<stop offset="100%" stop-color="{color}" stop-opacity="0"/>'
                     f'</linearGradient>')
    parts.append("</defs>")

    # Grid lines
    parts.append(f'<line x1="{X_MIN}" y1="{Y_MAX}" x2="{X_MAX}" y2="{Y_MAX}" stroke="#ddd" stroke-width="0.5"/>')
    for i in range(1, y_ticks + 1):
        y = map_y(i * y_step)
        parts.append(f'<line x1="{X_MIN}" y1="{y:.1f}" x2="{X_MAX}" y2="{y:.1f}" stroke="#eee" stroke-width="0.5" stroke-dasharray="4"/>')

    # Y-axis labels
    for i in range(y_ticks + 1):
        val = i * y_step
        y = map_y(val)
        label = fmt_stars(int(val)) if val > 0 else "0"
        parts.append(f'<text x="{X_MIN - 8}" y="{y + 4:.1f}" text-anchor="end" fill="#999" font-size="11">{label}</text>')

    # X-axis labels (~6 labels)
    n_xlabels = 6
    for i in range(n_xlabels):
        frac = i / (n_xlabels - 1)
        from datetime import timedelta
        d = date_min + timedelta(seconds=frac * date_range)
        x = X_MIN + frac * (X_MAX - X_MIN)
        parts.append(f'<text x="{x:.1f}" y="{Y_MAX + 18}" text-anchor="middle" fill="#999" font-size="11">{date_label(d)}</text>')

    # Plot each repo
    for idx, r in enumerate(repos):
        color = COLORS[idx % len(COLORS)]
        points = r["stars"]
        if not points:
            continue

        coords = [(map_x(p["date"]), map_y(p["cumulative"])) for p in points]
        poly_str = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)

        # Fill polygon (close to baseline)
        first_x = coords[0][0]
        last_x = coords[-1][0]
        fill_str = f"{first_x:.1f},{Y_MAX} {poly_str} {last_x:.1f},{Y_MAX}"
        parts.append(f'<polygon points="{fill_str}" fill="url(#g{idx})"/>')

        # Line
        parts.append(f'<polyline points="{poly_str}" fill="none" stroke="{color}" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>')

        # End dot + label
        ex, ey = coords[-1]
        total = r.get("total_stars", points[-1]["cumulative"])
        parts.append(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="3.5" fill="{color}"/>')
        parts.append(f'<text x="{ex:.1f}" y="{ey - 8:.1f}" text-anchor="middle" fill="{color}" font-size="11" font-weight="500">{fmt_stars(total)}</text>')

    # Legend
    legend_y = H - 16
    legend_x = X_MIN + 20
    for idx, r in enumerate(repos):
        color = COLORS[idx % len(COLORS)]
        parts.append(f'<rect x="{legend_x}" y="{legend_y - 9}" width="10" height="10" rx="2" fill="{color}"/>')
        parts.append(f'<text x="{legend_x + 15}" y="{legend_y}" fill="#666" font-size="12">{r["repo"]}</text>')
        legend_x += len(r["repo"]) * 7.5 + 40

    # star-history.com link
    sh_repos = "&".join(r["repo"] for r in repos)
    sh_url = f"https://star-history.com/#{sh_repos}&Date"
    parts.append(f'<a href="{sh_url}" target="_blank">')
    parts.append(f'<text x="{X_MAX}" y="{H - 5}" text-anchor="end" fill="#999" font-size="11" text-decoration="underline">star-history.com</text>')
    parts.append("</a>")

    parts.append("</svg>")
    return "\n".join(parts)

def wrap_html(svg, repos):
    sh_repos = "&".join(r["repo"] for r in repos)
    sh_url = f"https://star-history.com/#{sh_repos}&Date"
    title = "Star History"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<style>
body {{ font-family: system-ui,-apple-system,sans-serif; margin: 2rem auto; max-width: 760px; color: #333; }}
@media (prefers-color-scheme: dark) {{ body {{ background: #1a1a1a; color: #ccc; }} }}
h1 {{ font-size: 1.3rem; font-weight: 500; }}
.meta {{ font-size: 0.85rem; color: #888; margin-top: 0.5rem; }}
.meta a {{ color: #534AB7; }}
</style>
</head>
<body>
<h1>Star History</h1>
{svg}
<p class="meta">Data sampled from GitHub API &middot; <a href="{sh_url}" target="_blank">View interactive chart on star-history.com</a></p>
</body>
</html>"""

def main():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", help="JSON input file (default: stdin)")
    p.add_argument("-o", "--output", help="Output HTML file (default: star-history.html)")
    p.add_argument("--open", action="store_true", help="Open in browser after writing")
    p.add_argument("--svg-only", action="store_true", help="Output raw SVG to stdout instead of HTML")
    a = p.parse_args()

    if a.input:
        with open(a.input) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    svg = build_svg(data)

    if a.svg_only:
        print(svg)
        return

    out = a.output or "star-history.html"
    html = wrap_html(svg, data)
    with open(out, "w") as f:
        f.write(html)
    print(f"Written: {out}", file=sys.stderr)

    if a.open:
        webbrowser.open(f"file://{os.path.abspath(out)}")

if __name__ == "__main__":
    main()
