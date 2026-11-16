#!/usr/bin/env python3
"""Check that a quote is on a page, and show it in context. stdlib only.

  check_quote.py URL "quote"            exit 0 and print context if found, exit 1 if not
  check_quote.py --text FILE "quote"    same, against a local text file

The page is fetched with a plain User-Agent, HTML is reduced to text, and whitespace, soft hyphens, line-break hyphenation,
curly quotes and case are normalised before matching. A page that returns a CAPTCHA, cookie wall or login page counts as NOT found.
PDFs are read with `pdftotext` when it is installed."""
import html, re, subprocess, sys, tempfile, urllib.request
from html.parser import HTMLParser

WALL = re.compile(r"(recaptcha|unusual traffic|are you a robot|enable javascript|cookie consent|just a moment|access denied)", re.I)

class T(HTMLParser):
    def __init__(self): super().__init__(); self.out = []; self.skip = 0
    def handle_starttag(self, t, a):
        if t in ("script", "style", "noscript"): self.skip += 1
        if t in ("p", "br", "div", "li", "tr", "h1", "h2", "h3", "h4"): self.out.append(" ")
    def handle_endtag(self, t):
        if t in ("script", "style", "noscript") and self.skip: self.skip -= 1
    def handle_data(self, d):
        if not self.skip: self.out.append(d)

def norm(s):
    s = html.unescape(s).replace("­", "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    s = re.sub(r"-\s*\n\s*", "", s)           # line-break hyphenation
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (rdada-check-quote)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read(); ctype = r.headers.get("content-type", "")
    if "pdf" in ctype or url.lower().split("?")[0].endswith(".pdf"):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
            f.write(data); f.flush()
            return subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True, text=True).stdout
    txt = data.decode("utf-8", "replace")
    if "html" in ctype or "<html" in txt[:500].lower():
        p = T(); p.feed(txt); txt = " ".join(p.out)
    return txt

def main():
    a = sys.argv[1:]
    if len(a) == 3 and a[0] == "--text": text = open(a[1], encoding="utf-8", errors="replace").read(); quote = a[2]
    elif len(a) == 2: text = fetch(a[0]); quote = a[1]
    else: print(__doc__); return 2
    n, q = norm(text), norm(quote)
    if len(n) < 200 or (WALL.search(n[:3000]) and q not in n): print("NOT FOUND (page unreadable, walled or empty)"); return 1
    i = n.find(q)
    if i < 0: print("NOT FOUND"); return 1
    print("FOUND:", "..." + n[max(0, i - 120): i + len(q) + 120] + "..."); return 0
if __name__ == "__main__": sys.exit(main())
