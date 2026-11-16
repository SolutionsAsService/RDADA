# Candidate format

One object per source (full schema: `schemas/candidate.schema.json`).

```json
{
  "brief": "rec:phaistos-disc",
  "records": ["phaistos-disc"],
  "title": "Exact title of the work as shown on the page",
  "authors": "Surname I., Surname I.",
  "year": 2020,
  "venue": "Journal, publisher or archive",
  "url": "https://...",
  "doi": "10.xxxx/...",
  "accessed": "YYYY-MM-DD",
  "kind": "primary",
  "discipline": "Archaeology",
  "stance": "supports",
  "ask_addressed": "the ask text this bears on",
  "quote": "verbatim, at most 25 words, from the page",
  "summary": "One or two sentences: what the source shows, and what it does not.",
  "limits": "What the source does not establish; conflicts of interest if stated.",
  "reliability": "unassessed",
  "review": {"status": "unreviewed", "by": null}
}
```

Rules: `kind` is one of primary, secondary, alternative, official, skeptical. `stance` is one of supports, fails_to_support, contradicts, context. `reliability` is always `unassessed`. `review.status` is always `unreviewed`. `doi` only when printed on the page. `accessed` is today's date. Unknown authors or year: use `null`, never a guess.

## Thread briefs (transmission between cultures)

When the brief's `kind` is `thread`, each candidate also carries a `strand` describing what one source says was passed on:

```json
"strand": {"from": "Achaemenid Persia", "to": "Second Temple Judaism", "carried": "idea", "what": "angelology and eschatological dualism",
           "medium": "court_or_empire", "start": -539, "end": -330, "directness": "debated"}
```

`carried` is language, writing, religion, idea, technology, crop_or_animal, people, institution or custom. `medium` is migration, conquest, trade, translation, text, teaching, court_or_empire or unknown. `directness`: `documented` (a dated text, inscription or dated aDNA/archaeology shows the transfer), `inferred` (similarity plus plausible contact), `debated` (specialists disagree). Years are CE (negative = BCE). A strand needs a source that says it; a similarity the researcher noticed is not a strand.
