# HANDOFF — eidetic-doc-lang

**One-liner:** A Python CLI + protocol that lints LLM-generated technical docs for "slop" (filler, hedging, weak claims) against three controlled-verbosity registers.
**Status:** beta — ~85% to shippable
**Monetization:** weak — MIT style linter; indirect via a GitHub Action, a hosted docs-QA API, or a pro tier (custom wordlists / team rules)

## What it is
A validator and written protocol (`PROTOCOL.md`) for "non-slop" technical documentation, inspired by ASD-STE100 Simplified Technical English. It defines three registers (terse/balanced/expanded) and a pure-Python checker that flags filler phrases, low-claim sentences, passive voice, and weak paragraph leads. It is a style/structure linter, not a fact-checker.

## Who pays & why
Target buyer: teams shipping LLM/agent-generated docs (dev-tool companies, API-doc teams, AI-assisted technical writers). Pain: AI docs read like a chatbot and manual review is slow. Willingness to pay: low as a standalone (free linters abound), realistic only as a hosted service or a feature inside a larger doc-gen/agent product.

## Stack
Python 3.10+, standard library only (`json`, `re`, `argparse`, `unittest`). No third-party deps. GitHub Actions CI on ubuntu + windows, Python 3.12.

## Architecture
Input (`--input` file / `--text` / stdin, UTF-8) → `validator/validate.py` splits into paragraphs/sentences → runs checks: forbidden phrases (`templates/forbidden-words.json`), claim density = concrete-noun + action-verb with basic stemming (`validator/wordlists.py`), word caps, passive voice (terse only), banned openers, paragraph-lead → output as human report or `--json`; exit 0 pass / 1 fail / 2 usage. Key files: `validator/validate.py` (core), `validator/wordlists.py`, `templates/forbidden-words.json`, `PROTOCOL.md` (spec + prompt templates), `tests/test_cli.py`.

## What works today
- Three registers with word/paragraph caps and passive rules; density grade.
- Forbidden-phrase, claim-density, banned-opener, and paragraph-lead detection with stemming.
- CLI as both module (`-m validator.validate`) and direct script; JSON + human reports; robust UTF-8/stdin/exit-code handling (incl. legacy Windows encodings).
- Cross-platform CI and a subprocess-based test suite.

## Gaps to ship (ranked)
1. No packaging — no `pyproject.toml`/PyPI/pipx; install means cloning the repo. Blocks adoption.
2. Heuristic coverage — hand-maintained noun/verb wordlists miss domain terms, producing false "claim failures"; needs user-extensible config.
3. No integration surface — no published GitHub Action, pre-commit hook, or editor plugin.

## Run it
```bash
python3 -m validator.validate --input sample_doc.md --mode balanced
python3 -m validator.validate --text "The server sends data." --json
python3 -m unittest discover -s tests -v
```

## Risks / unknowns
- Style heuristics only; a PASS does not mean correct or accurate (README states this).
- Wordlist-based claim checking will frustrate users on specialized domains.
- Low defensibility: the protocol + wordlists are the moat, and both are forkable under MIT.

## Fastest path to revenue
1. Publish to PyPI and ship a free GitHub Action to seed adoption and lead-gen.
2. Offer a hosted API / CI SaaS with team dashboards and custom rule sets (paid tier).
3. Sell as a doc-quality gate bundled into LLM doc-gen pipelines / agent toolchains.
