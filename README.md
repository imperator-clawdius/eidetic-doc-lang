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

```bash
# Validate a doc against the Balanced register
python3 validator.py sample_doc.md

# Specify a register explicitly
python3 validator.py sample_doc.md --register eidetic-terse

# Run the built-in test suite
python3 -m pytest test_validator.py -v
```

Example document structure:

```markdown
# API Reference: User Endpoints

The authentication endpoint accepts POST requests.
It returns a 201 status on success.
A 401 status indicates invalid credentials.
```

Save as `docs/api.md`, then run `python3 validator.py docs/api.md` to check it against the Balanced register (default).

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
