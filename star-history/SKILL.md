---
name: star-history
description: Show GitHub star history charts. Triggers on star history, star chart, repo popularity, comparing repos by stars.
---

# Star History Skill

Show GitHub repository star history as an inline chart with a link to star-history.com.

## Input Parsing

Accept repos in any of these formats:
- `owner/repo` → use directly
- `https://github.com/owner/repo` → extract `owner/repo`
- `https://star-history.com/#owner/repo&Date` → extract `owner/repo`
- `https://star-history.com/#owner/repo1&owner/repo2&Date` → extract multiple repos
- Just `name` when owner equals repo name (e.g., `star-history` → `star-history/star-history`)

## Workflow

### Step 1: Fetch star data

```bash
python3 SKILL_DIR/scripts/fetch_stars.py owner/repo [owner/repo2 ...] 2>/dev/null > /tmp/star_data.json
```

Output: JSON array of `{repo, total_stars, stars: [{date, cumulative}]}`.
The script samples ~20 evenly-spaced pages from the stargazers API (~40 data points per repo), staying within GitHub's 60 req/hr unauthenticated limit.

### Step 2: Render chart (environment-dependent)

#### Path A — Claude.ai (Visualizer available)

Use `visualize:show_widget` to render a **pure SVG** chart inline.

**IMPORTANT: Chart.js does NOT work in the Visualizer sandbox. Use hand-drawn SVG only.**

You can use `render_chart.py --svg-only` to generate the SVG, or construct it directly. Either way, pass the raw SVG string as `widget_code`.

```bash
python3 SKILL_DIR/scripts/render_chart.py -i /tmp/star_data.json --svg-only
```

#### Path B — Claude Code / Cowork / CLI (no Visualizer)

Generate a standalone HTML file and open it in the browser:

```bash
python3 SKILL_DIR/scripts/render_chart.py -i /tmp/star_data.json -o star-history.html --open
```

The `--open` flag calls `webbrowser.open()` to launch it. On headless environments, skip `--open` and tell the user the file path.

### Step 3: Always provide the star-history.com link

Star-history.com URL format:
- Single: `https://star-history.com/#owner/repo&Date`
- Multiple: `https://star-history.com/#owner/repo1&owner/repo2&Date`

Include the link:
1. Inside the SVG (the render script adds it automatically as a clickable `<a>`)
2. In the prose response text as a fallback

### Step 4: Handle errors gracefully

- **Rate limited (HTTP 403)**: GitHub's unauthenticated limit is 60 req/hr. Suggest trying later or use the star-history.com link directly.
- **Repo not found (HTTP 404)**: Report the repo doesn't exist or is private.
- **Very small repos (<5 stars)**: Skip the chart, just report the count and provide the star-history.com link.

## SVG Chart Design (for Path A manual construction)

If constructing SVG directly instead of using render_chart.py:

- Coordinate system: `viewBox="0 0 700 400"`, chart area (60,30) to (680,330)
- Map dates to X (60–680), cumulative stars to Y (330→30, inverted)
- Horizontal dashed grid lines at Y-axis tick positions
- Y-axis labels with K-suffix (e.g., "10K"). X-axis with month labels (e.g., "Mar 25")
- `<polyline>` per repo, `<polygon>` with gradient fill underneath
- End-point dots + total star count annotation
- Legend: colored squares + repo names
- Clickable `<a>` to star-history.com at bottom-right

Color palette (in order): `#534AB7` (purple), `#1D9E75` (teal), `#D85A30` (coral), `#378ADD` (blue).

## Notes

- For repos with many stars (>10K), total_stars is approximate (pages × 100).
- If GITHUB_TOKEN env var is set, authenticated requests get 5000 req/hr.
- Up to ~4 repos can be compared before unauthenticated rate limits become an issue.
