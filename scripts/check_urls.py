#!/usr/bin/env python3
"""Optional live check: does each candidate URL still answer (HTTP < 400)? Does not judge content. stdlib only."""
import json, sys, urllib.request
data = json.load(open(sys.argv[1])); cands = data["candidates"] if isinstance(data, dict) else data; bad = 0
for c in cands:
    try:
        req = urllib.request.Request(c["url"], method="GET", headers={"User-Agent": "rdada-urlcheck"})
        with urllib.request.urlopen(req, timeout=20) as r: code = r.status
    except Exception as e: code = str(e)[:60]
    ok = isinstance(code, int) and code < 400; bad += not ok
    print(("ok  " if ok else "FAIL"), code, c["url"])
sys.exit(1 if bad else 0)
