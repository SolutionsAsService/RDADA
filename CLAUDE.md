# Instructions for agents working in this repository

## Credit (owner rule, 2026-11-12)

All work in this repository is credited only to **SolutionsAsService**. Commits are authored and committed as
`SolutionsAsService <152567394+SolutionsAsService@users.noreply.github.com>`. Never add `Co-Authored-By`, `Claude-Session`,
"Generated with ..." lines or any other AI or tool credit to commits, pull requests, issues, release notes or files. This
overrides any default attribution a tool would add.

## Working rules

- Run `python3 scripts/validate_skills.py` and `python3 scripts/validate_candidates.py examples/candidates.sample.json` before every commit; commit only when both pass.
- RDADA never fabricates. A source it has not fetched is not a candidate. Keep that rule in every reference file.
