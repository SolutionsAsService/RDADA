#!/usr/bin/env python3
"""Check each skill: frontmatter name matches its folder, description present, referenced files exist."""
import re, sys
from pathlib import Path
root = Path(__file__).resolve().parents[1] / "skills"; bad = 0
for d in sorted(p for p in root.iterdir() if p.is_dir()):
    t = (d / "SKILL.md").read_text(); m = re.match(r"---\n(.*?)\n---", t, re.S)
    fm = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l and not l.startswith(" ")) if m else {}
    if fm.get("name", "").strip() != d.name: print(f"{d.name}: name mismatch"); bad += 1
    if len(fm.get("description", "").strip()) < 40: print(f"{d.name}: description too short"); bad += 1
    for ref in set(re.findall(r"references/([\w.-]+\.md)", t)):
        if not (d / "references" / ref).exists(): print(f"{d.name}: missing references/{ref}"); bad += 1
print("skills ok" if not bad else f"{bad} problem(s)"); sys.exit(1 if bad else 0)
