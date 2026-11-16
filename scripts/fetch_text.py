#!/usr/bin/env python3
"""Fetch a primary-text passage by locator. stdlib only.

  fetch_text.py sefaria "Genesis 6:9-9:17" [--lang he|en] [--version "substring"]   Hebrew Bible, Mishnah, Talmud (Sefaria API)
  fetch_text.py bible   "John 1:1-5" [--translation kjv|web|asv]                      English Bible (bible-api.com)
  fetch_text.py url     URL                                                            any page reduced to text (first 6000 chars)

Prints the text with its locator and the version/licence the source reports. Use the printed words, not memory, for quotes;
then confirm with check_quote.py against the page the candidate cites."""
import json, re, sys, urllib.parse, urllib.request
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_quote import fetch

def get(url):
    return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "rdada-fetch-text"}), timeout=40).read().decode("utf-8", "replace")

def strip(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()

def flat(x):
    if isinstance(x, list):
        for i in x: yield from flat(i)
    elif x: yield strip(str(x))

def main():
    a = sys.argv[1:]
    if len(a) < 2: print(__doc__); return 2
    kind, ref = a[0], a[1]
    opt = {a[i]: a[i + 1] for i in range(2, len(a) - 1, 2)}
    if kind == "sefaria":
        r = json.loads(get("https://www.sefaria.org/api/texts/" + urllib.parse.quote(ref.replace(" ", "_")) + "?context=0&commentary=0"))
        lang = opt.get("--lang", "en")
        print(f"[{r.get('ref')} | {lang} | {r.get('versionTitle') if lang == 'en' else r.get('heVersionTitle')} | {r.get('license') if lang == 'en' else r.get('heLicense')}]")
        for i, v in enumerate(flat(r.get("text" if lang == "en" else "he")), 1): print(f"{i}. {v}")
    elif kind == "bible":
        t = opt.get("--translation", "web")
        r = json.loads(get(f"https://bible-api.com/{urllib.parse.quote(ref)}?translation={t}"))
        print(f"[{r.get('reference')} | {r.get('translation_name')}]")
        for v in r.get("verses", []): print(f"{v['chapter']}:{v['verse']} {strip(v['text'])}")
    elif kind == "url":
        print(fetch(ref)[:6000])
    else: print(__doc__); return 2
if __name__ == "__main__": sys.exit(main())
