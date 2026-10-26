#!/usr/bin/env python3
"""Check domain registration status against each TLD registry's RDAP server.

Usage:
  check.py nophai bugsfound.com           # bare names get every --tlds suffix
  check.py -f names.txt -t com,dev,app,net
  check.py --raw nophai                   # one line per domain instead of a grid

Status per domain: FREE (registry 404), taken (registry 200), or ?<reason>
(?429 rate-limited after retries, ?noRDAP when the TLD has no RDAP server,
?403 / ?URLError when the registry or the network refused the request).

Registry endpoints come from IANA's bootstrap file, so new TLDs work without
edits. The rdap.org redirector is avoided on purpose: under bulk load it
returns 429s.
"""
import argparse, concurrent.futures as cf, json, os, ssl, sys, time
import urllib.error, urllib.request

BOOTSTRAP = "https://data.iana.org/rdap/dns.json"

# ccTLDs missing from IANA's bootstrap whose registry back-end answers RDAP
# anyway (tested 26 Oct 2026: google.io/.sh/.ac -> 200, nophai.io -> 404).
FALLBACK = {t: "https://rdap.identitydigital.services/rdap/" for t in ("io", "sh", "ac")}


def ssl_context():
    # Sandboxes behind an egress proxy ship their own CA bundle.
    for path in (os.environ.get("SSL_CERT_FILE"), os.environ.get("REQUESTS_CA_BUNDLE"),
                 "/root/.ccr/ca-bundle.crt"):
        if path and os.path.exists(path):
            return ssl.create_default_context(cafile=path)
    return ssl.create_default_context()


CTX = ssl_context()


def get(url):
    # Some registries (PIR for .org, Identity Digital for .ai) answer 403 to
    # Python's default User-Agent, so send a descriptive one.
    req = urllib.request.Request(url, headers={
        "Accept": "application/rdap+json",
        "User-Agent": "domain-check/1.0 (+https://github.com/korakot/skills)"})
    return urllib.request.urlopen(req, timeout=15, context=CTX)


def load_servers():
    data = json.load(get(BOOTSTRAP))
    servers = dict(FALLBACK)
    for tlds, urls in data["services"]:
        for tld in tlds:
            servers[tld.lower()] = urls[0].rstrip("/") + "/"
    return servers


def check(domain, servers):
    tld = domain.rsplit(".", 1)[1]
    base = servers.get(tld)
    if not base:
        return domain, "?noRDAP"
    ascii_name = domain.encode("idna").decode()  # Thai or other IDN -> xn--...
    for attempt in range(5):
        try:
            get(base + "domain/" + ascii_name)
            return domain, "taken"
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return domain, "FREE"
            if e.code == 429:
                time.sleep(2 * (attempt + 1))
                continue
            return domain, f"?{e.code}"
        except Exception as e:
            return domain, "?" + type(e).__name__
    return domain, "?429"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="*")
    ap.add_argument("-f", "--file", help="one name per line")
    ap.add_argument("-t", "--tlds", default="com,dev,app,net")
    ap.add_argument("--raw", action="store_true", help="one line per domain")
    ap.add_argument("-w", "--workers", type=int, default=3)
    a = ap.parse_args()

    names = list(a.names)
    if a.file:
        names += [l.strip() for l in open(a.file) if l.strip() and not l.startswith("#")]
    tlds = [t.strip().lstrip(".").lower() for t in a.tlds.split(",") if t.strip()]

    domains, rows = [], []  # rows: (label, [domains])
    for n in names:
        n = n.lower()
        group = [n] if "." in n else [f"{n}.{t}" for t in tlds]
        rows.append((n, group))
        domains += [d for d in group if d not in domains]
    if not domains:
        ap.error("no names given")

    servers = load_servers()
    with cf.ThreadPoolExecutor(a.workers) as ex:
        status = dict(ex.map(lambda d: check(d, servers), domains))

    if a.raw:
        for d in domains:
            print(f"{status[d]:8} {d}")
        return
    mark = {"FREE": "✓", "taken": "✗"}
    width = max(len(label) for label, _ in rows)
    for label, group in rows:
        cells = []
        for d in group:
            s = status[d]
            cells.append(f"{d.rsplit('.', 1)[1] if '.' not in label else d}:{mark.get(s, s)}")
        print(f"{label:<{width}}  " + "  ".join(cells))


if __name__ == "__main__":
    sys.exit(main())
