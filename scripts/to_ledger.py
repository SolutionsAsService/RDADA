#!/usr/bin/env python3
"""Print human-history `Source` lines (src/data/sources.ts style) for REVIEWED-BY-A-HUMAN candidate files.
Every line is a placeholder with reliability 'unassessed': a person must read the original before changing that."""
import json, re, sys
data = json.load(open(sys.argv[1])); cands = data["candidates"] if isinstance(data, dict) else data
def esc(s): return str(s).replace("\\", "\\\\").replace("'", "\\'")
seen = {}
for c in cands:      # one Source per work: several passages from the same URL collapse into one line
    if c["url"] in seen: continue
    seen[c["url"]] = 1
    au = c.get("authors") or "Unknown"; fam = re.split(r"[ ,]", au)[0].lower() or "src"; yr = c.get("year") or "nd"
    sid = re.sub(r"[^a-z0-9]", "", f"{fam}{yr}")
    cite = f"{au} ({yr}) {c['title']}. {c.get('venue') or ''}".strip().rstrip(".") + "." + (f" doi:{c['doi']}" if c.get("doi") else "") + f" {c['url']} (accessed {c['accessed']})."
    note = f"RDADA candidate for {', '.join(c.get('records') or [c['brief']])}; stance {c['stance']}. {c.get('limits') or ''}".strip()
    print(f"  s('{sid}', '{esc(cite)}', '{c['kind']}', '{esc(c.get('discipline') or 'Unclassified')}', 'unassessed', '{esc(note)}', true),")
