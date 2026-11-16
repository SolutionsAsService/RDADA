---
name: rdada
description: Use when asked to find new sources for an evidence ledger or map (human-history style), to follow research briefs, or to test a claim by looking for supporting AND sceptical sources. Takes briefs (JSON or plain text), runs parallel researcher subagents, has a verifier subagent re-fetch every candidate, and returns verified, unreviewed candidate sources plus honest gaps. Needs a subagent tool (Agent or Task) and web access; without them, research one brief directly following references/researcher.md.
metadata:
  author: SolutionsAsService
  repository: https://github.com/SolutionsAsService/RDADA
---

# RDADA coordinator

You are the **coordinator**. You read briefs, spawn subagents, and manage files. You do not search the web and you do not judge sources yourself, and you do not read `references/researcher.md` or `references/verifier.md` (the subagents do). You never edit the ledger.

## Process

1. Load briefs
2. Plan the run
3. Spawn researchers (parallel)
4. Spawn verifier(s)
5. Assemble outputs
6. Deliver

### 1. Load briefs

Input is one of: a path to a `briefs.json` (`{"briefs":[...]}` as written by human-history's `ml/hh/sourcing.py`), a pasted brief, or a plain question ("find sources on X"). For a plain question, make one brief yourself: `id`, `records` (may be empty), `asks` (what a source must show), `wanted_kinds`, and `queries` built only from words the user gave. Take the briefs in order of `need`, up to the number requested (default 10). Never invent briefs beyond what was asked.

### 2. Plan the run

Run name: `YYYY-MM-DD short title` (letters, numbers, single spaces). Create `rdada_runs/<run>/notes/` in the directory used earlier in this conversation, else the working directory. Group briefs so one researcher handles one brief, or two closely related briefs, never more. Limit to 8 researchers in parallel; queue the rest in later rounds.

### 3. Spawn researchers

One foreground subagent per brief, all in one turn. Prompt template:

```
Agent(
  description="Research {brief id}",
  prompt="Research this brief for an evidence ledger.

BRIEF (JSON):
{the brief, verbatim}

Save notes to: {abs path}/rdada_runs/{run}/notes/{safe brief id}.md
Save candidates to: {abs path}/rdada_runs/{run}/notes/{safe brief id}.candidates.json

**First, read {path_to_skill}/references/researcher.md and {path_to_skill}/references/candidate-format.md and follow them.**"
)
```

### 4. Spawn verifiers

When researchers finish, spawn one verifier per researcher output (parallel), each pointed at that brief's `.candidates.json`. The verifier is a different agent from the researcher. Prompt: the candidates path, the output paths (`...verified.json`, `...rejected.json`), and "**First read {path_to_skill}/references/verifier.md and follow it.**"

### 5. Assemble outputs

Merge every `.verified.json` into `rdada_runs/<run>/candidates.json` (`{"run":..., "generated":..., "candidates":[...]}`), and every rejected file into `rejected.json`. Run `python3 scripts/validate_candidates.py` if the repo is present; fix only formatting, never content. Do not add, edit or reword a candidate yourself.

### 6. Deliver

Write `report.md`: per brief, how many candidates survived, what stance they take, and the gaps (briefs with no candidates, or with support only and no sceptical material, are flagged "one-sided"). Send `report.md` and `candidates.json` to the user if you can; otherwise give absolute paths. Summarise in 3-5 sentences, saying plainly that candidates are unreviewed leads. Do not say a source "proves" anything.
