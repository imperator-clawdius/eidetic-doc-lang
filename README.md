# Eidetic Documentation Language (EDL)

The protocol and validator for writing **non-slop technical documentation** using
controlled verbosity. Three tiers. One rule: every word earns its place.

Inspired by ASD-STE100 Simplified Technical English. Built for LLM-generated docs.

## Core Concept

Not one fixed constraint — three **registers** of increasing verbosity:

| Register | Max Words/Sentence | Max Sentences/Paragraph | Passive | Use Case |
|----------|-------------------|----------------------|---------|----------|
| **Eidetic-Terse** | 20 | 3 | Forbidden | Procedures, checklists, API refs |
| **Eidetic-Balanced** | 25 | 5 | Allowed | Developer docs, user guides |
| **Eidetic-Expanded** | 30 | 7 | Allowed | Onboarding, tutorials, explanations |

## How It Works

1. **Write** docs using the prompt templates (see PROTOCOL.md)
2. **Validate** them with the Python validator
3. **Iterate** until PASS

The validator checks:
- **Forbidden words** — filler transitions, hedging, vague modifiers, meta-commentary, banned openers
- **Claim density** — every sentence must contain a concrete noun and an action verb
- **Mode rules** — word caps, paragraph limits, passive voice (terse only)
- **Paragraph leads** — first sentence must deliver a specific claim

## Quick Start

Requires Python 3.10 or newer; no third-party packages are needed. Run module
commands from the repository root (`python` on Windows).

```bash
# Validate a doc against the Balanced register
python3 -m validator.validate --input sample_doc.md

# Specify a register explicitly
python3 -m validator.validate --input sample_doc.md --mode terse

# Validate inline text with a machine-readable report
python3 -m validator.validate --text "The server sends data." --json

# Read UTF-8 text from standard input
python3 -m validator.validate --json < sample_doc.md

# Run the built-in test suite
python3 -m unittest discover -s tests -v
```

The direct script also works: `python3 validator/validate.py --input sample_doc.md`.
From another directory, use the absolute script path. File input, piped input,
and output use UTF-8, including redirected output on Windows. Choose one of
`--input` or `--text`; omitting both reads standard input. Modes are `terse`,
`balanced` (default), and `expanded`.

Exit status is `0` for a passing heuristic verdict, `1` for a failing verdict,
and `2` for invalid usage or unreadable/empty input. With `--json`, input errors
produce an `error` object; argument parsing errors print usage to stderr.
The imported `validate(text, mode)` function and its existing scoring rules are
unchanged. These English word-list and pattern checks assess writing style;
they do not verify facts, evidence, security, or technical correctness. Human
review remains necessary, even when the result is PASS.

Example document structure:

```markdown
# API Reference: User Endpoints

The authentication endpoint accepts POST requests.
It returns a 201 status on success.
A 401 status indicates invalid credentials.
```

Save as `docs/api.md`, then run `python3 -m validator.validate --input docs/api.md` to check it against the Balanced register (default).

See [PROTOCOL.md](PROTOCOL.md) for complete rules, prompt templates, and register definitions.

## Test Results

| Input | Mode | Verdict | Forbidden Violations | Claim Fail Rate | Density |
|-------|------|---------|---------------------|----------------|---------|
| Raw AI slop | Balanced | FAIL | 18 | 61.9% | 69.6 Excellent |
| Eidetic-Terse | Terse | PASS | 0 | 16.7% | 90.7 Excellent |
| Eidetic-Balanced | Balanced | PASS | 0 | 6.7% | 84.6 Excellent |
| Eidetic-Expanded | Expanded | PASS* | 0 | 28.6% | 86.0 Excellent |

*Expanded failed only on paragraph formatting (single blob vs. separated paragraphs)

## Why It Works

Most LLM documentation fails because of **filler**, not **inaccuracy**. The Eidetic validator catches:

- "It is worth noting that..." → deleted
- "Interestingly, ..." → deleted  
- "As previously mentioned..." → deleted
- "This would be a potentially serious security issue" → rewritten as "This creates a security risk."

The result: docs that read like a **technical writer** wrote them, not a chatbot.

## License

MIT — free for anyone to use, fork, or ship with their agent.
