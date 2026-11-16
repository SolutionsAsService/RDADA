#!/usr/bin/env python3
"""Build a review queue for a run folder (stdlib only). Inspired by the evidence atlas idea of listing what the builder
REFUSED to guess: rejected candidates with reasons, quotes that are second-hand or abstract-only, undated or approximated
dates, strands with no counter-evidence, and hosts that did not open.

  review_queue.py "rdada_runs/<run>"   ->  <run>/review-queue.json and <run>/review-queue.md"""
import glob, json, re, sys
from pathlib import Path
run = Path(sys.argv[1]); notes = run / "notes"
q = {"rejected": [], "second_hand": [], "abstract_only": [], "undated_text": [], "one_sided": [], "failed_hosts": {}}
for f in sorted(glob.glob(str(notes / "*.rejected.json"))):
    for r in json.load(open(f)):
        c = r.get("candidate", {}); q["rejected"].append({"brief": Path(f).name.split(".")[0], "title": c.get("title"), "url": c.get("url"), "reason": r.get("reason")})
by_brief = {}
for f in sorted(glob.glob(str(notes / "*.verified.json"))):
    b = Path(f).name.split(".")[0]
    for c in json.load(open(f)):
        lim = (c.get("limits") or "").lower(); tag = {"brief": b, "title": c.get("title"), "url": c.get("url")}
        if "second-hand" in lim or "second hand" in lim: q["second_hand"].append(tag)
        if "abstract only" in lim or "abstract-only" in lim or "abstract page" in lim: q["abstract_only"].append(tag)
        tx = c.get("text")
        if tx and (tx.get("composition") or {}).get("start") is None and (tx.get("composition") or {}).get("end") is None: q["undated_text"].append({**tag, "work": tx.get("work")})
        st = c.get("strand")
        if st: by_brief.setdefault((b, st.get("from"), st.get("to")), []).append(c)
for (b, a, z), cs in by_brief.items():
    if all(c.get("stance") in ("supports", "context") for c in cs) and any((c.get("strand") or {}).get("directness") == "debated" for c in cs):
        q["one_sided"].append({"brief": b, "from": a, "to": z, "n": len(cs)})
for f in sorted(glob.glob(str(notes / "*.md"))):
    t = open(f, encoding="utf-8", errors="replace").read(); m = re.search(r"(?is)(failed hosts|hosts that failed|blocked or failed)[^\n]*\n(.+?)(\n#|\Z)", t)
    if m:
        for h in re.findall(r"[a-z0-9.-]+\.(?:com|org|net|edu|ac\.uk|gov|int|io|fr|de|es|il|jp|cn)\b", m.group(2).lower()): q["failed_hosts"][h] = q["failed_hosts"].get(h, 0) + 1
json.dump(q, open(run / "review-queue.json", "w"), indent=1)
L = [f"# Review queue: {run.name}", "", "What this run could not settle. Nothing here is hidden.", ""]
for k, title in (("rejected", "Rejected by the verifier"), ("second_hand", "Second-hand quotations (a scholar quoted through another)"), ("abstract_only", "Abstract-only sources"), ("undated_text", "Primary passages with no composition date"), ("one_sided", "Debated strands whose sources only support or give context")):
    L += [f"## {title} ({len(q[k])})", ""] + [f"- {json.dumps(x, ensure_ascii=False)}" for x in q[k]] + [""]
L += [f"## Hosts that did not open ({len(q['failed_hosts'])})", ""] + [f"- {h} ×{n}" for h, n in sorted(q["failed_hosts"].items(), key=lambda x: -x[1])]
(run / "review-queue.md").write_text("\n".join(L) + "\n")
print({k: (len(v) if not isinstance(v, dict) else len(v)) for k, v in q.items()})
