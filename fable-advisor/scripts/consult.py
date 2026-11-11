#!/usr/bin/env python3
"""Consult Claude Fable once, headless, with a curated brief.

Usage: python3 consult.py BRIEF_FILE [--model fable] [--effort high] [--budget 1.00]

Runs `claude -p` with no tools, safe mode, the advisor preamble as the system
prompt, and the brief on stdin. Prints the verdict, then one usage line.
Exit codes: 0 verdict from Fable; 2 failed or not Fable (do not retry, report);
3 CLI missing or not logged in (use the Agent-tool fallback, announced).
"""
import argparse, json, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent.parent

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--model", default="fable")
    ap.add_argument("--effort", default="high")
    ap.add_argument("--budget", default="1.00")
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()

    if shutil.which("claude") is None:
        print("[fable-advisor] claude CLI not found", file=sys.stderr)
        return 3
    preamble = (HERE / "preamble.txt").read_text().strip()
    brief = pathlib.Path(a.brief).read_text()
    cmd = ["claude", "-p", "--model", a.model, "--effort", a.effort,
           "--safe-mode", "--tools", "", "--system-prompt", preamble,
           "--output-format", "json", "--no-session-persistence",
           "--max-turns", "1", "--max-budget-usd", a.budget]
    try:
        p = subprocess.run(cmd, input=brief, capture_output=True, text=True, timeout=a.timeout)
    except subprocess.TimeoutExpired:
        print(f"[fable-advisor] timed out after {a.timeout}s", file=sys.stderr)
        return 2
    try:
        d = json.loads(p.stdout)
    except ValueError:
        err = (p.stderr or p.stdout)[-600:]
        login = any(w in err.lower() for w in ("log in", "login", "not authenticated", "auth"))
        print(f"[fable-advisor] exit {p.returncode}, no JSON: {err}", file=sys.stderr)
        return 3 if login else 2

    usage = d.get("modelUsage") or {}
    fable = {m: u for m, u in usage.items() if "fable" in m and u.get("outputTokens", 0) > 0}
    others = [m for m, u in usage.items() if m not in fable and "haiku" not in m and u.get("outputTokens", 0) > 0]
    ok = (p.returncode == 0 and d.get("type") == "result" and d.get("subtype") == "success"
          and d.get("is_error") is False and isinstance(d.get("result"), str) and d["result"].strip())
    if not ok or not fable or others:
        print(f"[fable-advisor] not a Fable verdict: subtype={d.get('subtype')} "
              f"is_error={d.get('is_error')} models={list(usage)}", file=sys.stderr)
        return 2

    m, u = next(iter(fable.items()))
    inp = u.get("inputTokens", 0) + u.get("cacheReadInputTokens", 0) + u.get("cacheCreationInputTokens", 0)
    print(d["result"].strip())
    print(f"\n[fable-advisor] model={m} input={inp} (cache read {u.get('cacheReadInputTokens', 0)}) "
          f"output={u.get('outputTokens', 0)} (thinking {u.get('thinkingTokens', 0)}) "
          f"cost≈${d.get('total_cost_usd', 0):.3f} time={d.get('duration_ms', 0) / 1000:.0f}s")
    return 0

if __name__ == "__main__":
    sys.exit(main())
