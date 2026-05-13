#!/usr/bin/env python3
"""BIA Archive search and read tool.
Usage:
  bia.py search QUERY [--type publications|manuscripts] [--limit N] [--page N] [--year-start N] [--year-end N]
  bia.py read ID   (UUID or referenceCode)
"""
import argparse, json, re, sys
from urllib.request import urlopen, Request
from urllib.parse import urlencode
from html.parser import HTMLParser

PROXY = "https://bia-proxy.korakot.workers.dev/api/metadata"
URL_BASE = "https://bia-archive.psu.ac.th"

KEEP_TAGS = {"p", "ol", "ul", "li", "br"}


class HTMLCleaner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self._skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("o:p", "xml", "style", "script"):
            self._skip += 1
            return
        if self._skip:
            return
        if tag in KEEP_TAGS:
            self.parts.append(f"<{tag}>")

    def handle_endtag(self, tag):
        if tag in ("o:p", "xml", "style", "script"):
            self._skip = max(0, self._skip - 1)
            return
        if self._skip:
            return
        if tag in KEEP_TAGS:
            self.parts.append(f"</{tag}>")

    def handle_data(self, data):
        if not self._skip:
            self.parts.append(data)

    def handle_comment(self, data):
        pass


def clean_html(raw: str) -> str:
    if not raw:
        return ""
    p = HTMLCleaner()
    p.feed(raw)
    text = "".join(p.parts)
    # collapse excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return text


def fetch(url: str) -> dict:
    req = Request(url, headers={"Accept": "application/json", "User-Agent": "Mozilla/5.0"})
    with urlopen(req, timeout=15) as r:
        return json.loads(r.read())


def format_date(start: str, end: str, with_ce=False) -> str:
    def to_year(s):
        if not s:
            return None
        y = s.split("-")[0]
        return int(y) if y.isdigit() and int(y) > 0 else None

    ys, ye = to_year(start), to_year(end)
    if not ys and not ye:
        return "ไม่ระบุปี"
    if ys == ye or not ye:
        label = f"พ.ศ. {ys}"
        if with_ce:
            label += f" / ค.ศ. {ys - 543}"
        return label
    label = f"พ.ศ. {ys}–{ye}"
    if with_ce:
        label += f" / ค.ศ. {ys - 543}–{ye - 543}"
    return label


def reading_url(ref_code: str, item_type: str) -> str:
    path = "manuscripts" if item_type == "manuscripts" else "printed"
    return f"{URL_BASE}/{path}/{ref_code}"


def is_uuid(s: str) -> bool:
    return bool(re.fullmatch(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", s, re.I
    ))


def cmd_search(args):
    params = {
        "search": args.query,
        "limit": args.limit,
        "page": args.page,
        "yearStart": args.year_start,
        "yearEnd": args.year_end,
    }
    if args.type:
        params["types"] = args.type
    url = f"{PROXY}/search?{urlencode(params)}"
    data = fetch(url)
    meta = data.get("meta", {})
    results = []
    for item in data.get("data", []):
        ref = item.get("referenceCode", "")
        itype = item.get("type", "")
        results.append({
            "title": item.get("title", ""),
            "type": itype,
            "dateDisplay": format_date(item.get("dateStart"), item.get("dateEnd")),
            "pages": item.get("imageCount") or 0,
            "referenceCode": ref,
            "url": reading_url(ref, itype),
        })
    print(json.dumps({
        "query": args.query,
        "total": meta.get("total", 0),
        "page": meta.get("page", 1),
        "totalPages": meta.get("totalPages", 1),
        "results": results,
    }, ensure_ascii=False, indent=2))


def cmd_read(args):
    uid = args.id
    if not is_uuid(uid):
        # Resolve refCode → UUID via search
        data = fetch(f"{PROXY}/search?{urlencode({'search': uid, 'limit': 1})}")
        items = data.get("data", [])
        if not items:
            print(json.dumps({"error": f"No item found for: {uid}"}, ensure_ascii=False))
            sys.exit(1)
        uid = items[0]["id"]

    detail = fetch(f"{PROXY}/{uid}/detail")
    item = detail.get("item", {})
    ref = item.get("referenceCode", "")
    itype = item.get("type") or (
        "manuscripts" if "manuscript" in ref.lower() else "publications"
    )

    # Infer type from referenceCode pattern if not set
    dr = item.get("dateRange", "")
    parts = dr.split(" - ") if dr else []
    ds = parts[0].strip() if parts else item.get("dateStart", "")
    de = parts[1].strip() if len(parts) > 1 else ds

    images = sorted(detail.get("images", []), key=lambda x: x.get("pageNumber", 0))

    print(json.dumps({
        "title": item.get("title", ""),
        "type": itype,
        "dateDisplay": format_date(ds, de, with_ce=True),
        "pages": len(images),
        "extent": item.get("physicalExtent") or "",
        "description": clean_html(item.get("scopeAndContent") or ""),
        "referenceCode": ref,
        "url": reading_url(ref, itype),
    }, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")

    s = sub.add_parser("search")
    s.add_argument("query")
    s.add_argument("--type", choices=["publications", "manuscripts"])
    s.add_argument("--limit", type=int, default=12)
    s.add_argument("--page", type=int, default=1)
    s.add_argument("--year-start", type=int, default=0, dest="year_start")
    s.add_argument("--year-end", type=int, default=2600, dest="year_end")

    r = sub.add_parser("read")
    r.add_argument("id")

    args = parser.parse_args()
    if args.cmd == "search":
        cmd_search(args)
    elif args.cmd == "read":
        cmd_read(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
