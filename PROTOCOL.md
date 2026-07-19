# TRIDENT-DOC Protocol

## Controlled Verbosity for AI-Generated Technical Documentation

**Version:** 1.0
**Author:** W1d0wm4k3r / 1mp3r1um Network
**Inspired by:** ASD-STE100 Simplified Technical English + @geogristle

---

## 1. Overview

TRIDENT-DOC is a three-tier controlled verbosity protocol for AI-generated technical documentation. It solves one problem: **LLMs generate verbose, information-sparse prose filled with hedges, filler transitions, and meta-commentary.**

STE-100 (Simplified Technical English) proved that vocabulary and grammar constraints produce clearer documentation. But STE-100 was designed for non-native readers in aerospace maintenance — not for AI-generated content. Raw STE-100 overcorrects, stripping prose to a skeleton with no room for explanation, examples, or context.

TRIDENT-DOC adapts the STE-100 insight into a tiered system that scales verbosity by document context. The forbidden list stays constant. The density matrix changes by mode.

---

## 2. Core Concepts

### 2.1 The Three Modes

| Mode | Purpose | Readability Level | Example Use |
|------|---------|-------------------|-------------|
| **Terse** | Minimal, direct instructions | ~grade 5 | Procedures, checklists, API reference, CLI help text |
| **Balanced** | Moderate depth with context | ~grade 8 | Developer guides, user manuals, configuration docs |
| **Expanded** | Full explanation with examples | ~grade 10 | Tutorials, onboarding, conceptual deep-dives |

### 2.2 The Three Enforcement Layers

**Layer 1 — Forbidden List (always active)**

Unconditionally banned elements in all modes. These carry zero semantic weight.

**Layer 2 — Density Matrix (mode-specific)**

Sentence length, paragraph limits, tense restrictions, and example allowances vary per mode.

**Layer 3 — Semantic Weight (always active)**

Information density scoring. Each sentence must contain a concrete noun and a specific claim. Filler-to-content ratio must not exceed 0.6.

---

## 3. Layer 1: Forbidden Elements

### 3.1 Vague Modifiers

```
very, really, quite, somewhat, slightly, highly, extremely,
fairly, rather, pretty (as intensifier), too (as excessive), so (as intensifier)
```

### 3.2 Filler Transitions

```
however, therefore, moreover, furthermore, in addition, additionally,
nevertheless, nonetheless, consequently, thus, hence, accordingly,
it is worth noting, it is important to, it should be noted,
as previously mentioned, as discussed earlier, as we discussed,
let's dive in, let's explore, let's take a look, let's examine,
it is worth mentioning, it bears mentioning, as an aside,
on the other hand (unless paired with a specific contrast),
notably, interestingly, importantly,
in order to (replace with "to")
```

### 3.3 Hedging Language

```
may (as hedge; allow for permission), might (remove all uses),
could (as hedge; allow for past ability), would (as hedge),
perhaps, possibly, presumably, supposedly,
generally, typically, often, usually, normally,
in many cases, in most cases, as a general rule,
more often than not, tends to, likely, unlikely (unless probabilistic),
probably, conceivably, potentially
```

### 3.4 Meta-Commentary

```
as you can see, as I mentioned, as we saw,
it is important to note, it should be noted that,
it goes without saying, needless to say,
what this means is, in other words (replace with direct rewrite),
put simply (replace with direct rewrite),
long story short, the bottom line is,
for what it's worth, at the end of the day,
all things considered, when all is said and done
```

### 3.5 Banned Sentence Openers

Avoid starting sentences with:
```
However, Moreover, Furthermore, Additionally, Notably,
Interestingly, Importantly, Essentially, Basically,
Arguably, Admittedly, Fortunately, Unfortunately,
Unsurprisingly, Predictably
```

---

## 4. Layer 2: Density Matrix

### 4.1 Terse Mode

```yaml
mode: terse
max_words_per_sentence: 20
max_sentences_per_paragraph: 3
passive_voice: forbidden
allowed_tenses: [imperative, simple_present]
concepts_per_section: 1
examples_per_concept: 0
edge_cases: skip
allow_contrasts: false
allow_qualifiers: false
```

**Structural rule:** Each sentence must be a standalone instruction or statement. No content paragraph — every paragraph is a list or a set of independent sentences.

**Tone:** Direct, imperative-heavy. Similar to military technical orders or STE-100 procedures.

### 4.2 Balanced Mode

```yaml
mode: balanced
max_words_per_sentence: 25
max_sentences_per_paragraph: 5
passive_voice: allow_when_subject_obvious
allowed_tenses: [simple_present, simple_past, imperative]
concepts_per_section: 1
examples_per_concept: 1
edge_cases: optional
allow_contrasts: true
allow_qualifiers: true
```

**Structural rule:** One concept per paragraph. The first sentence introduces the concept. The remaining sentences expand or give one example.

**Tone:** Explanatory but direct. Sufficient for competent readers who need no handholding.

### 4.3 Expanded Mode

```yaml
mode: expanded
max_words_per_sentence: 30
max_sentences_per_paragraph: 7
passive_voice: allow_normally
allowed_tenses: [simple_present, simple_past, future_simple, imperative, present_perfect]
concepts_per_section: 1
examples_per_concept: 2-3
edge_cases: include
allow_contrasts: true
allow_qualifiers: true
```

**Structural rule:** One concept per section. Open with a framing statement. Provide explanation, 2-3 examples, and edge cases. Close with a summary or transition to the next concept.

**Tone:** Explanatory and thorough. Suitable for readers who need full context.

### 4.4 Grammatical Constraints (All Modes)

1. **Do not use continuous/progressive tenses.** No "is running," "was processing," "will be configuring."
2. **Write in the affirmative.** Negate only when the negation is the information: "The feature does not support WebSocket connections." — not "It is not possible to use WebSocket connections with this feature."
3. **Avoid nominalization.** Prefer verbs over noun forms. Write "the system authenticates the user" not "authentication of the user is done by the system."
4. **Place the subject early.** No long introductory phrases before the subject.
5. **One idea per sentence.** If two ideas are related, write two sentences.
6. **Use technical terms precisely.** Do not use synonyms for technical terms within the same document.

---

## 5. Layer 3: Semantic Weight Scoring

### 5.1 Scoring Formula

For each sentence, compute:

```
weight_score = (content_tokens / total_tokens) * 100

where:
  content_tokens = nouns + verbs + adjectives + adverbs
  total_tokens = all tokens in sentence
  filler_tokens = articles + prepositions + conjunctions + auxiliary verbs
```

**Thresholds:**
- `weight_score < 35` — **FAIL.** Sentence is filler-dominant. Rewrite required.
- `weight_score 35-50` — **WARN.** Sentence may be weak. Review recommended.
- `weight_score > 50` — **PASS.** Acceptable density.

### 5.2 Claim Presence Check

Each sentence must satisfy:
1. Contains at least one **concrete noun** (not "thing," "stuff," "area," "aspect")
2. Makes a **specific claim** — not a generic statement that applies to anything

**Criteria:**
- A concrete noun is a real-world entity, technology, or measurable concept
- A specific claim cannot be transferred to another document without modification

### 5.3 Paragraph Lead Check

The first sentence of each paragraph must:
- State the topic of the paragraph
- Contain the primary specific claim
- Not be a transition sentence

**Rejected patterns:**
- "Let's talk about configuration." → FAILED. No claim.
- "Configuration is important." → FAILED. Generic.
- "Configuration happens during application startup." → PASSED. Specific.

---

## 6. Mode Selection Guide

Use this decision tree to select the appropriate mode:

```
Is the document a reference or step-by-step procedure?
  ├── Yes → Terse
  └── No ↓
Is the document a developer guide or user manual?
  ├── Yes → Balanced
  └── No ↓
Is the document a tutorial, onboarding walkthrough, or conceptual guide?
  ├── Yes → Expanded
  └── No → Balanced (default)
```

---

## 7. Prompt Templates

### 7.1 System Prompt — All Modes

```
You write technical documentation following the TRIDENT-DOC protocol.
TRIDENT-DOC eliminates AI-slop: no filler transitions, no hedging, 
no vague modifiers, no meta-commentary.

PERMANENT RULES (all modes):
- Every sentence must contain a concrete noun and a specific claim
- No filler transitions: however, therefore, moreover, furthermore, 
  additionally, in addition, it is worth noting, as previously mentioned
- No hedging: may, might, could (as hedge), perhaps, possibly, 
  generally, typically, often, usually
- No vague modifiers: very, really, quite, somewhat, slightly, highly
- No meta-commentary: as you can see, interestingly, notably, it should be noted
- Do not use continuous/progressive tenses
- Place the subject early in each sentence
- One idea per sentence
- Use technical terms consistently — do not synonymize
- Prefer verbs over nominalizations
```

### 7.2 Mode-Specific Instructions

**Terse mode block:**
```
CURRENT MODE: Terse
- Maximum 20 words per sentence
- Maximum 3 sentences per paragraph
- Forbid passive voice
- Use imperative mood for instructions and simple present for facts
- No examples — each sentence is a standalone instruction or statement
- No qualifiers or contrasts
- Each sentence must be independently useful
```

**Balanced mode block:**
```
CURRENT MODE: Balanced
- Maximum 25 words per sentence
- Maximum 5 sentences per paragraph
- Passive voice: allow only when the subject receiving the action is the obvious focus
- Allowed tenses: simple present, simple past, imperative
- One example per concept maximum
- Edge cases: optional
- First sentence in each paragraph must introduce the paragraph topic
```

**Expanded mode block:**
```
CURRENT MODE: Expanded
- Maximum 30 words per sentence
- Maximum 7 sentences per paragraph
- Passive voice: allow normally
- Allowed tenses: simple present, simple past, future simple, imperative, present perfect
- 2-3 examples per concept
- Edge cases: include
- Open each section with a framing statement
- Close with a summary or transition to the next concept
- Avoid continuous/progressive tenses
```

---

## 8. Validation Pipeline

### 8.1 Architecture

```
┌──────────┐    ┌───────────────┐    ┌──────────────┐    ┌─────────────┐
│  Input   │ →  │  Layer 1:     │ →  │  Layer 2:    │ →  │  Layer 3:   │
│  Text    │    │  Forbidden    │    │  Density     │    │  Semantic   │
│          │    │  Scanner      │    │  Matrix      │    │  Weight     │
└──────────┘    └───────────────┘    └──────────────┘    └─────────────┘
                       │                    │                   │
                       ▼                    ▼                   ▼
               ┌──────────────────────────────────────────────────┐
               │              Report Generator                    │
               │  - PASS/FAIL per check                           │
               │  - Line-level flags with text context            │
               │  - Density score (0-100)                         │
               │  - Rewrite suggestions (optional)                │
               └──────────────────────────────────────────────────┘
```

### 8.2 Pass/Fail Criteria

A document **PASSES** validation when:
1. Zero forbidden word violations
2. At least 90% of sentences pass semantic weight scoring (>35)
3. At least 90% of paragraphs pass lead check
4. Sentence length within mode limits for at least 95% of sentences
5. No structural violations (passive in terse, wrong tenses, etc.)

A document **FAILS** validation when:
1. More than 5 forbidden word violations
2. More than 10% of sentences fail semantic weight scoring
3. More than 10% of paragraphs fail lead check
4. More than 5% of sentences exceed mode length limits
5. Two or more structural violations

### 8.3 Rewrite Protocol

When a document fails:
1. Run the verbatim text through the same LLM with a "rewrite to pass TRIDENT-DOC validation" instruction
2. Append the validation report to the rewrite prompt
3. Re-validate the output
4. Repeat until pass or manual intervention

---

## 9. Example Outputs

**Prompt:** *"Explain how environment variables work in SuiteScrape"*

### Terse

```
Environment variables control SuiteScrape connections.
Store them in the .env file in the root directory.

Configure the API key with API_KEY.
Configure the database URL with DATABASE_URL.
Configure the log level with LOG_LEVEL.
Save the file and restart SuiteScrape.
```

### Balanced

```
Environment variables control how SuiteScrape connects to external services.
They are stored in a single .env file in the root directory.

The most common variables are API_KEY, DATABASE_URL, and LOG_LEVEL.
Set API_KEY to your API authentication token.
Set DATABASE_URL to your PostgreSQL connection string.
Set LOG_LEVEL to debug, info, warn, or error.

Save the file and restart SuiteScrape before the changes take effect.
```

### Expanded

```
Environment variables let you configure SuiteScrape without modifying source code.
They manage connections to APIs, databases, and storage services.

The application reads a .env file in the root directory on startup.
Open this file in any text editor. Each line sets one variable.
The variable names are case-sensitive. Spaces around the equals sign are not allowed.

The most common variables are API_KEY for external service access,
DATABASE_URL for the PostgreSQL connection string,
and LOG_LEVEL for verbosity control.

Set LOG_LEVEL to "debug" to see all request details during troubleshooting.
Set it to "error" in production for minimal log output.

After editing the file, save your changes and restart SuiteScrape.
On Linux, use `systemctl restart suitescraper`.
On Docker, use `docker restart suitescraper`.

For production deployments, use your orchestrator's secrets manager
instead of a .env file for sensitive values. The variable names remain the same.
```

---

## 10. Implementation Notes

### 10.1 LLM Compatibility

TRIDENT-DOC works with any instruction-following LLM. The permanent forbidden list and mode-specific rules should be placed:
- **System prompt** — permanent forbidden list (Layer 1)
- **User prompt prefix** — mode-specific instructions (Layer 2)

The semantic weight scoring (Layer 3) is a post-processing step best done with a script or programmatic call.

### 10.2 Known Failure Modes

1. **Over-correction.** In Terse mode, the output can become cryptic. If readers need more context, switch to Balanced.
2. **Example starvation.** In Terse mode, no examples are permitted. For audiences that learn by example, use Balanced or Expanded.
3. **Tone mismatch.** The Terse imperative style can read as blunt or rude. Add "please" to procedural steps if audience sensitivity requires it.

### 10.3 Extending the Forbidden List

The forbidden word list in this protocol is the core set. Add domain-specific filler words as discovered:
- JavaScript developers: "robust," "seamless," "intuitive"
- Business writing: "leverage," "optimize," "streamline," "holistic"
- Academic: "thusly," "henceforth," "utilize"

Document any additions with evidence (a real sentence that failed the protocol) to justify the inclusion.

---

## 11. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-19 | Initial release. Three-mode protocol with forbidden list, density matrix, and semantic weight scoring. |
