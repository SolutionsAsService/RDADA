#!/usr/bin/env python3
"""Validate an RDADA candidates file (stdlib only). Exit 1 on any problem.
Checks the rules that keep the output honest: https URL, quote length, reliability unassessed, review unreviewed,
no duplicate URL, verified marker present, and (per brief) a one-sided warning when only one stance family is present."""
import json, re, sys
from collections import defaultdict
KINDS = {"primary", "secondary", "alternative", "official", "skeptical"}
STANCES = {"supports", "fails_to_support", "contradicts", "context"}
REQ = ["brief", "title", "url", "accessed", "kind", "stance", "quote", "summary", "reliability", "review"]

def check(c, i, errs):
    p = f"candidate {i} ({c.get('title', '?')[:40]})"
    for k in REQ:
        if k not in c or c[k] in ("", None): errs.append(f"{p}: missing {k}")
    if errs and errs[-1].startswith(p): return
    if not str(c["url"]).startswith("https://"): errs.append(f"{p}: url must be https")
    if c["kind"] not in KINDS: errs.append(f"{p}: bad kind {c['kind']}")
    if c["stance"] not in STANCES: errs.append(f"{p}: bad stance {c['stance']}")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", c["accessed"]): errs.append(f"{p}: accessed must be YYYY-MM-DD")
    if len(c["quote"].split()) > 25: errs.append(f"{p}: quote longer than 25 words")
    if c["reliability"] != "unassessed": errs.append(f"{p}: reliability must be 'unassessed'")
    if c["review"].get("status") != "unreviewed": errs.append(f"{p}: review.status must be 'unreviewed'")
    if c.get("doi") and not re.fullmatch(r"10\.\d{4,9}/\S+", c["doi"]): errs.append(f"{p}: malformed doi")
    if "verified" not in c: errs.append(f"{p}: no verifier marker")

def main(path):
    data = json.load(open(path)); cands = data["candidates"] if isinstance(data, dict) else data
    errs, seen, fam = [], set(), defaultdict(set)
    for i, c in enumerate(cands):
        check(c, i, errs)
        u = str(c.get("url", "")).rstrip("/").lower()
        if u in seen: errs.append(f"candidate {i}: duplicate url")
        seen.add(u)
        fam[c.get("brief")].add("for" if c.get("stance") == "supports" else "against" if c.get("stance") in ("contradicts", "fails_to_support") else "other")
    for b, s in fam.items():
        if s == {"for"}: print(f"warning: brief {b} is one-sided (support only)")
    for e in errs: print("error:", e)
    print(f"{len(cands)} candidates, {len(errs)} error(s)")
    return 1 if errs else 0
if __name__ == "__main__": sys.exit(main(sys.argv[1]))
