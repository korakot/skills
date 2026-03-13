#!/usr/bin/env python3
"""Fetch GitHub star history with smart page-sampling.

Usage: python3 fetch_stars.py owner/repo [owner/repo2 ...]
Output: JSON to stdout — array of {repo, stars: [{date, cumulative}]}
Designed to stay well within GitHub's 60 req/hr unauthenticated limit.
"""
import sys, json, urllib.request, urllib.error, re, math, os
from datetime import datetime, timezone

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
MAX_SAMPLE_PAGES = 20          # pages to sample per repo
PER_PAGE = 100                 # max allowed by GitHub

def _headers():
    h = {"Accept": "application/vnd.github.star+json",
         "User-Agent": "star-history-skill"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h

def _get(url):
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=15) as r:
        link = r.headers.get("Link", "")
        return json.loads(r.read()), link

def _total_pages(link_header):
    """Extract last page number from Link header."""
    m = re.search(r'page=(\d+)>;\s*rel="last"', link_header)
    return int(m.group(1)) if m else 1

def _sample_pages(total):
    """Return sorted list of page numbers to fetch (always includes 1 and last)."""
    if total <= MAX_SAMPLE_PAGES:
        return list(range(1, total + 1))
    pages = {1, total}
    step = total / (MAX_SAMPLE_PAGES - 1)
    for i in range(1, MAX_SAMPLE_PAGES - 1):
        pages.add(max(1, min(total, round(i * step))))
    return sorted(pages)

def fetch_repo(repo):
    """Return {repo, total_stars, stars: [{date, cumulative}]}"""
    base = f"https://api.github.com/repos/{repo}/stargazers"
    # First request to get total pages
    try:
        data0, link0 = _get(f"{base}?per_page={PER_PAGE}&page=1")
    except urllib.error.HTTPError as e:
        return {"repo": repo, "error": f"HTTP {e.code}", "stars": []}

    total_pages = _total_pages(link0)
    total_stars = total_pages * PER_PAGE  # approximate
    pages_to_fetch = _sample_pages(total_pages)

    points = []  # (page_num, starred_at_str, cumulative_index)

    for pg in pages_to_fetch:
        if pg == 1:
            page_data = data0
        else:
            try:
                page_data, _ = _get(f"{base}?per_page={PER_PAGE}&page={pg}")
            except Exception:
                continue
        if not page_data:
            continue
        # Use first and last entry of each page as sample points
        for idx in (0, len(page_data) - 1):
            entry = page_data[idx]
            sa = entry.get("starred_at", "")
            cumulative = (pg - 1) * PER_PAGE + idx + 1
            if sa:
                points.append({"date": sa[:10], "cumulative": cumulative})

    # Deduplicate and sort
    seen = set()
    unique = []
    for p in sorted(points, key=lambda x: x["cumulative"]):
        key = (p["date"], p["cumulative"])
        if key not in seen:
            seen.add(key)
            unique.append(p)

    return {"repo": repo, "total_stars": total_stars, "stars": unique}

def parse_repo(arg):
    """Normalise input: full URL, owner/repo, or just 'name' (when owner==name)."""
    arg = arg.strip().rstrip("/")
    # Full GitHub URL
    m = re.match(r'https?://github\.com/([^/]+/[^/]+)', arg)
    if m:
        return m.group(1)
    # star-history URL
    m = re.match(r'https?://star-history\.com/#([^&]+)', arg)
    if m:
        return m.group(1)
    # owner/repo
    if "/" in arg:
        return arg
    return arg  # will likely fail but let API report error

def main():
    if len(sys.argv) < 2:
        sys.exit("Usage: fetch_stars.py owner/repo [owner/repo2 ...]")

    repos = [parse_repo(a) for a in sys.argv[1:]]
    results = []
    for r in repos:
        print(f"Fetching {r} ...", file=sys.stderr)
        results.append(fetch_repo(r))

    json.dump(results, sys.stdout, indent=2)

if __name__ == "__main__":
    main()
