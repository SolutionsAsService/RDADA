# RDADA — Research Directed Ambition Design Agent

A research agent skill for evidence ledgers. It takes **briefs** (what a new source would need to show, and why it matters), sends parallel researchers to the open web, has an independent verifier re-fetch every claim, and returns **candidate sources** for a human to review. It builds on the coordinator pattern of [deep-research](https://github.com/SolutionsAsService/deep-research).

It was made for [human-history](https://github.com/SolutionsAsService/human-history): that repo's learning pipeline (`ml/`) ranks where a new source would change the ledger most and writes `ml/out/briefs.json`; RDADA goes and looks.

```
ledger gaps + model flags ──▶ briefs.json ──▶ researchers (parallel) ──▶ verifier ──▶ candidates.json ──▶ human review ──▶ ledger
```

## Rules it will not break

1. **No candidate without a fetch.** Every candidate has a URL the researcher opened and a short verbatim quote from the page. Recalled citations are not candidates.
2. **Both directions.** Each brief is searched for support *and* for sceptical, contradicting and alternative sources. A run that returns only confirming material is incomplete.
3. **Stance is relative to the brief**, not to what anyone hopes is true: `supports`, `fails_to_support`, `contradicts`, `context`.
4. **Nothing is promoted.** Candidates arrive `unreviewed`; reliability is `unassessed` until a person assesses it. RDADA never edits the ledger and never sets an evidence status.
5. **"Found nothing" is a result.** A brief may end with an honest gap and no candidates.
6. **Verification is separate.** A second agent re-fetches each URL and checks the quote and the stance. Failed candidates are dropped and listed, not repaired.

## Use

Install the skill (`skills/rdada`) and say, for example: *"Run RDADA on ml/out/briefs.json, top 10 briefs."* Outputs, in the working directory:

```
rdada_runs/<run>/notes/<brief-id>.md     researcher notes (cited, with gaps)
rdada_runs/<run>/candidates.json         verified candidates (schema: schemas/candidate.schema.json)
rdada_runs/<run>/rejected.json           candidates that failed verification, with the reason
rdada_runs/<run>/report.md               what was found, what was not
```

Then:

```
python3 scripts/validate_candidates.py rdada_runs/<run>/candidates.json
python3 scripts/check_urls.py        rdada_runs/<run>/candidates.json    # optional live check
python3 scripts/to_ledger.py         rdada_runs/<run>/candidates.json    # prints TypeScript Source lines for review
```

`to_ledger.py` marks every line `placeholder` and reliability `unassessed`: the human-history rule is that a source is a lead until a person has read the original.

## Layout

```
skills/rdada/SKILL.md                 coordinator
skills/rdada/references/              researcher, verifier, candidate format
schemas/candidate.schema.json         the return format
scripts/                              validators and the ledger formatter (stdlib only)
examples/                             a sample briefs file and a sample candidates file
```
