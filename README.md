# TRIDENT-DOC

**Controlled verbosity for AI-generated technical documentation.**

TRIDENT-DOC is a prompt protocol and validation toolkit that eliminates AI-slop from technical writing while preserving informative depth. It takes the core insight of ASD-STE100 (Simplified Technical English) — constrained vocabulary and sentence structure — and wraps it in a tiered system that scales verbosity by context.

No more "it is worth noting that," "as previously mentioned," or "let's dive in." Just documentation that communicates.

## The Problem

LLMs generate confident, verbose, and information-sparse prose. The default output is hedged ("may", "could", "generally"), bloated with transition filler ("however", "therefore", "in addition"), and structured around paragraph shapes rather than information density.

Raw STE-100 solves this — but too well. It strips prose to near-monosyllabic bone. The resulting output reads like a Chinese dryer manual. Documentation needs to be *clear and complete*, not just short.

## The Solution: Tiered Compression

TRIDENT-DOC defines three modes, each appropriate for different documentation contexts:

| Mode | Verbosity | Max Sentence Length | Max Paragraph Size | Best For |
|------|-----------|-------------------|-------------------|----------|
| **Terse** | Minimal | 20 words | 3 sentences | Procedures, checklists, API reference docs |
| **Balanced** | Moderate | 25 words | 5 sentences | Developer guides, user manuals, configuration docs |
| **Expanded** | Full but clean | 30 words | 7 sentences | Tutorials, onboarding, conceptual explanations |

## How It Works

TRIDENT-DOC operates in three layers:

### Layer 1 — Forbidden List (Permanent)

These words and phrases are banned in all modes. They carry zero information:

**Vague modifiers:** `very`, `really`, `quite`, `somewhat`, `slightly`, `highly`, `extremely`, `fairly`, `rather`

**Filler transitions:** `however`, `therefore`, `moreover`, `furthermore`, `in addition`, `it is worth noting`, `it is important to`, `in order to`, `as previously mentioned`, `as we discussed`, `let's dive in`, `let's explore`, `it should be noted`

**Hedging language:** `may` (as hedge), `might`, `could` (as hedge), `would` (as hedge), `perhaps`, `possibly`, `generally`, `typically`, `often`, `usually`, `in many cases`, `as a general rule`

**Meta-commentary:** `it's important to note that`, `it should be noted that`, `as you can see`, `as I mentioned`, `interestingly`, `notably`

### Layer 2 — Density Matrix (Mode-Specific)

Each mode enforces a specific profile:

| Rule | Terse | Balanced | Expanded |
|------|-------|----------|----------|
| Max words per sentence | 20 | 25 | 30 |
| Max sentences per paragraph | 3 | 5 | 7 |
| Passive voice | Forbidden | Allowed when subject is obvious | Allowed normally |
| Allowed tenses | Imperative, simple present | Simple present, simple past, imperative | All standard (no continuous/progressive) |
| Sentences per concept | 1 | 2-3 | 3-5 |
| Examples per concept | 0 | 1 | 2-3 |
| Edge cases | Skip | Optional | Include |

### Layer 3 — Semantic Weight Enforcement

This is the differentiator from STE-100. Rather than just constraining vocabulary, TRIDENT-DOC enforces **information density per sentence**.

```
Scoring:
- Each sentence must contain at least one concrete noun and one specific claim
- Flag if filler-to-content token ratio exceeds 0.6
- Flag if sentence can be rewritten without losing meaning
- Reject any paragraph where the first sentence does not make a specific claim
```

## Package Contents

```
trident-doc/
├── README.md                  # This file
├── PROTOCOL.md                # Full protocol specification
├── templates/
│   ├── system-prompt-terse.md # System prompt for Terse mode
│   ├── system-prompt-balanced.md # System prompt for Balanced mode
│   ├── system-prompt-expanded.md # System prompt for Expanded mode
│   └── forbidden-words.json   # Machine-readable forbidden word list
├── validator/                  
│   ├── validate.py            # Python validator script
│   ├── config.yaml            # Mode configurations
│   └── test_samples/          # Test inputs and expected outputs
│       ├── input-slop.txt     # Sample AI-slop input
│       ├── input-terse.txt    # Sample terse input
│       ├── input-balanced.txt # Sample balanced input
│       └── input-expanded.txt # Sample expanded input
└── LICENSE
```

## Quick Start

### 1. Add the Forbidden List to Your System Prompt

Copy the contents of `templates/system-prompt-balanced.md` into your LLM's system prompt. This instantly removes AI-slop from all output.

### 2. Validate Output

```bash
python3 validator/validate.py --mode balanced --input output.txt
```

Returns:
```
✓ PASS: 3 violations found (below threshold of 5)
  - Line 12: Contains forbidden word "however"
  - Line 18: Sentence exceeds 25-word limit (32 words)
  - Line 24: First paragraph sentence has no specific claim
Density score: 78/100
```

### 3. Force a Rewrite

```bash
python3 validator/validate.py --mode terse --input draft.txt --rewrite
```

Outputs the re-generated text that passes all checks.

## Modes Overview

### Terse

For step-by-step procedures, checklists, API references, and command-line help.

```
1. Open the .env file in the root directory.
2. Add the API_KEY variable. Set it to your key value.
3. Save the file.
4. Restart the application.
```

### Balanced

For developer documentation, configuration guides, and user manuals.

```
Environment variables control how SuiteScrape connects to external services.
They are stored in a .env file in the root directory.

To configure the API key, add API_KEY=your_value to the file.
To configure the database, add DATABASE_URL=your_connection_string.
Save the file and restart SuiteScrape for changes to take effect.
```

### Expanded

For tutorials, onboarding materials, and conceptual explanations.

```
Environment variables let you configure SuiteScrape without changing code.
They manage connections to APIs, databases, and storage services.

The application reads a .env file in the root directory on startup.
Open this file in any text editor. Each line sets one variable.

The most common variables are API_KEY for external service access
and DATABASE_URL for the PostgreSQL connection string.
You can also set LOG_LEVEL to control debugging output.

After editing the file, save your changes and restart SuiteScrape.
Use `systemctl restart suitescraper` on Linux or restart the
Docker container if running containerized.
```

## Comparison: TRIDENT-DOC vs STE-100

| | ASD-STE100 | TRIDENT-DOC |
|---|---|---|
| Purpose | Non-native reader comprehension | Anti-AI-slop + density control |
| Verbosity | Always minimal | Tiered by document context |
| Passive voice | Forbidden | Allowed in Balanced/Expanded |
| Sentence length | Hard 20-word cap | Sliding scale per mode (20-30) |
| Vocabulary | ~900 approved words only | Open vocabulary, filtered for precision |
| Examples/Explanations | Discouraged | Encouraged in Expanded mode |
| Readability ceiling | 5th grade level | Per-mode (5th to 10th grade) |
| Integrates with LLM | Manual STE checker required | Prompt protocol + validator |

## Use Cases

- **Documentation generation** — Auto-generate API refs, user guides, procedures
- **Content rewriting** — Post-process any AI-generated text to remove slop
- **CI/CD pipeline** — Validate documentation commits against TRIDENT-DOC rules
- **Agent system prompts** — Wire the protocol into agent production chains for any output

## Origin

TRIDENT-DOC was coined by the W1d0wm4k3r autonomous intelligence operating on the OpenClaw agent framework. The protocol was inspired by a tweet from @geogristle suggesting ASD-STE100 as an anti-slop constraint for LLM output, and was developed in collaboration with the 1mp3r1um network.

## Contributing

Pull requests welcome. Contributions should:
1. Maintain the three-tier compression model
2. Extend the forbidden word list based on evidence
3. Preserve the scoring/validation philosophy

## License

MIT — Use it in your agents, your docs, your CI pipelines. Credit appreciated, not required.
