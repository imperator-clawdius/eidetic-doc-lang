#!/usr/bin/env python3
"""
Eidetic Documentation Language (EDL) Validator v1.0
Validates text against the Eidetic Documentation Language (EDL) controlled verbosity protocol.
Modes: terse | balanced | expanded
"""

import json
import re
import sys
from pathlib import Path

# Load word lists
from validator.wordlists import CONCRETE_NOUNS, ACTION_VERBS

FW_PATH = Path(__file__).resolve().parent.parent / "templates" / "forbidden-words.json"
with open(FW_PATH) as f:
    FORBIDDEN = json.load(f)

MODES = {
    "terse": {
        "max_words": 20,
        "max_paragraph_sentences": 3,
        "passive_allowed": False,
        "max_violations": 3,
    },
    "balanced": {
        "max_words": 25,
        "max_paragraph_sentences": 5,
        "passive_allowed": True,
        "max_violations": 5,
    },
    "expanded": {
        "max_words": 30,
        "max_paragraph_sentences": 7,
        "passive_allowed": True,
        "max_violations": 8,
    },
}

_FLAT = []
for cat, words in FORBIDDEN.items():
    _FLAT.extend(words)
_FLAT = sorted(set(_FLAT), key=len, reverse=True)

NOUNS_LOOKUP = {n.lower() for n in CONCRETE_NOUNS}
VERBS_LOOKUP = {v.lower() for v in ACTION_VERBS}

FILLERS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "in", "on", "at", "to", "for", "of", "with", "by",
    "from", "as", "and", "or", "but", "so", "if", "then", "than",
    "that", "this", "it", "its", "they", "them", "their", "we",
    "our", "there",
}


def _stem(token):
    """Basic English stemming for claim checking."""
    t = token.lower()
    if t in NOUNS_LOOKUP or t in VERBS_LOOKUP:
        return t, True
    # Plurals: -ies -> -y
    if t.endswith("ies") and len(t) > 4:
        for base in (t[:-3] + "y",):
            if base in NOUNS_LOOKUP or base in VERBS_LOOKUP:
                return base, True
    # -ves -> -f / -fe
    if t.endswith("ves") and len(t) > 4:
        for base in (t[:-3] + "f", t[:-3] + "fe"):
            if base in NOUNS_LOOKUP or base in VERBS_LOOKUP:
                return base, True
    # -es -> -e / -s
    if t.endswith("es") and len(t) > 3:
        for base in (t[:-2], t[:-1]):
            if base in NOUNS_LOOKUP or base in VERBS_LOOKUP:
                return base, True
    # -s -> singular
    if t.endswith("s") and not t.endswith("ss") and len(t) > 2:
        base = t[:-1]
        if base in NOUNS_LOOKUP or base in VERBS_LOOKUP:
            return base, True
    # -ing -> verb base
    if t.endswith("ing") and len(t) > 5:
        for base in (t[:-3], t[:-3] + "e"):
            if base in VERBS_LOOKUP:
                return base, True
    # -ed -> verb base
    if t.endswith("ed") and len(t) > 3:
        for base in (t[:-2], t[:-1]):
            if base in VERBS_LOOKUP:
                return base, True
        if t.endswith("ied"):
            base = t[:-3] + "y"
            if base in VERBS_LOOKUP:
                return base, True
    # Uppercase identifiers (API_KEY, LOG_LEVEL) - check for noun tokens
    if "_" in t:
        parts = t.split("_")
        for p in parts:
            if p.lower() in NOUNS_LOOKUP or p.lower() in VERBS_LOOKUP:
                return p.lower(), True
    return t, False


def _tokenize(sentence):
    return sentence.strip().split()


def _count_words(sentence):
    return len(_tokenize(sentence))


def _has_passive(text):
    return bool(re.search(
        r'\b(is|are|was|were|been|being)\s+\w+ed\b', text, re.IGNORECASE
    ))


def _check_forbidden(text):
    text_lower = text.lower()
    violations = []
    seen = set()
    for phrase in _FLAT:
        if phrase.lower() in text_lower:
            key = phrase.lower()
            if key not in seen:
                violations.append(phrase)
                seen.add(key)
    return sorted(violations)


def _check_banned_openers(sentence):
    stripped = sentence.strip()
    for opener in FORBIDDEN.get("banned_openers", []):
        if stripped.startswith(opener):
            return True
    return False


def _weight_score(sentence):
    tokens = _tokenize(sentence)
    if not tokens:
        return 100.0, 0
    total = len(tokens)
    filler_count = sum(1 for t in tokens if t.lower() in FILLERS)
    content = total - filler_count
    score = (content / total) * 100
    return round(score, 1), content


def _has_concrete_noun_and_claim(sentence):
    """Check if sentence has at least one recognized concrete noun
    and one recognized action verb (with basic stemming)."""
    words = sentence.lower().split()
    has_noun = any(_stem(w)[1] and _stem(w)[0] in NOUNS_LOOKUP for w in words)
    has_verb = any(_stem(w)[1] and _stem(w)[0] in VERBS_LOOKUP for w in words)
    return has_noun and has_verb


def validate(text, mode="balanced"):
    if mode not in MODES:
        return {"error": f"Unknown mode: {mode}. Use terse, balanced, or expanded."}

    cfg = MODES[mode]
    paragraphs = [p.strip() for p in text.replace("\r", "").split("\n\n") if p.strip()]

    results = {
        "mode": mode,
        "pass": True,
        "stats": {"sentences": 0, "paragraphs": len(paragraphs)},
        "forbidden_violations": [],
        "length_violations": [],
        "passive_violations": [],
        "opener_violations": [],
        "weight_scores": [],
        "claim_failures": [],
        "paragraph_issues": [],
    }

    for pi, para in enumerate(paragraphs):
        sentences = [s.strip() for s in re.split(r'(?<=[.!?])\s+', para) if s.strip()]

        # Paragraph lead check
        if sentences:
            lead_claim = _has_concrete_noun_and_claim(sentences[0])
            if not lead_claim:
                results["paragraph_issues"].append({
                    "paragraph": pi,
                    "issue": "First sentence has no specific claim or concrete noun",
                    "text": sentences[0][:100],
                })

        for si, sentence in enumerate(sentences):
            results["stats"]["sentences"] += 1

            fwd = _check_forbidden(sentence)
            if fwd:
                results["forbidden_violations"].append({
                    "paragraph": pi,
                    "sentence": si,
                    "violations": fwd,
                    "text": sentence[:100],
                })

            wc = _count_words(sentence)
            if wc > cfg["max_words"]:
                results["length_violations"].append({
                    "paragraph": pi,
                    "sentence": si,
                    "word_count": wc,
                    "max": cfg["max_words"],
                    "text": sentence[:100],
                })

            if not cfg["passive_allowed"] and _has_passive(sentence):
                results["passive_violations"].append({
                    "paragraph": pi,
                    "sentence": si,
                    "text": sentence[:100],
                })

            if _check_banned_openers(sentence):
                results["opener_violations"].append({
                    "paragraph": pi,
                    "sentence": si,
                    "text": sentence[:100],
                })

            ws, _ = _weight_score(sentence)
            results["weight_scores"].append(ws)

            if not _has_concrete_noun_and_claim(sentence):
                results["claim_failures"].append({
                    "paragraph": pi,
                    "sentence": si,
                    "weight_score": ws,
                    "text": sentence[:100],
                })

    total_s = results["stats"]["sentences"]
    total_v = (
        len(results["forbidden_violations"])
        + len(results["passive_violations"])
        + len(results["opener_violations"])
    )
    avg_w = sum(results["weight_scores"]) / total_s if total_s > 0 else 0
    fail_rate = round(len(results["claim_failures"]) / max(total_s, 1) * 100, 1)

    results["stats"]["total_violations"] = total_v
    results["stats"]["fail_rate"] = fail_rate
    results["stats"]["avg_weight_score"] = round(avg_w, 1)
    results["stats"]["density_grade"] = _density_grade(avg_w)

    fails = 0
    if len(results["forbidden_violations"]) >= cfg["max_violations"]:
        fails += 1
    if results["stats"]["fail_rate"] > 10:
        fails += 1
    para_issue_threshold = max(1, int(results["stats"]["paragraphs"] * 0.1))
    if len(results["paragraph_issues"]) > para_issue_threshold:
        fails += 1

    results["pass"] = fails == 0
    return results


def _density_grade(score):
    if score >= 60: return "Excellent"
    if score >= 50: return "Good"
    if score >= 40: return "Adequate"
    if score >= 35: return "Weak"
    return "Poor"


def format_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("Eidetic Documentation Language (EDL) VALIDATION REPORT")
    lines.append("=" * 60)
    lines.append(f"Mode:              {results['mode'].upper()}")
    lines.append(f"Verdict:           {'PASS' if results['pass'] else 'FAIL'}")
    lines.append(f"Sentences checked: {results['stats']['sentences']}")
    lines.append(f"Paragraphs:        {results['stats']['paragraphs']}")
    lines.append(f"Total violations:  {results['stats']['total_violations']}")
    lines.append(f"Claim fail rate:   {results['stats']['fail_rate']}%")
    lines.append(f"Density score:     {results['stats']['avg_weight_score']}/100 ({results['stats']['density_grade']})")
    lines.append("")

    if results["forbidden_violations"]:
        lines.append("[FORBIDDEN WORDS/PHRASES]")
        for v in results["forbidden_violations"]:
            lines.append(f"  P{v['paragraph']}:S{v['sentence']} - {', '.join(v['violations'])}")
            lines.append(f'    "{v["text"]}"')
        lines.append("")

    if results["length_violations"]:
        lines.append("[SENTENCE TOO LONG]")
        for v in results["length_violations"]:
            lines.append(f"  P{v['paragraph']}:S{v['sentence']} - {v['word_count']} words (max {v['max']})")
            lines.append(f'    "{v["text"]}"')
        lines.append("")

    if results["passive_violations"]:
        lines.append(f"[PASSIVE VOICE] (forbidden in {results['mode']} mode)")
        for v in results["passive_violations"]:
            lines.append(f"  P{v['paragraph']}:S{v['sentence']}")
            lines.append(f'    "{v["text"]}"')
        lines.append("")

    if results["opener_violations"]:
        lines.append("[BANNED SENTENCE OPENER]")
        for v in results["opener_violations"]:
            lines.append(f"  P{v['paragraph']}:S{v['sentence']}")
            lines.append(f'    "{v["text"]}"')
        lines.append("")

    if results["claim_failures"]:
        lines.append("[CLAIM/NOUN FAILURE] (no concrete noun or action verb)")
        for v in results["claim_failures"]:
            lines.append(f"  P{v['paragraph']}:S{v['sentence']} (density: {v['weight_score']})")
            lines.append(f'    "{v["text"]}"')
        lines.append("")

    if results["paragraph_issues"]:
        lines.append("[PARAGRAPH LEAD FAILURE]")
        for v in results["paragraph_issues"]:
            lines.append(f"  P{v['paragraph']}: {v['issue']}")
            lines.append(f'    "{v["text"]}"')
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Eidetic Documentation Language (EDL) Validator")
    parser.add_argument("--mode", choices=["terse", "balanced", "expanded"], default="balanced")
    parser.add_argument("--input", "-i", help="Input file path")
    parser.add_argument("--text", "-t", help="Inline text")
    parser.add_argument("--json", action="store_true", help="Output JSON")

    args = parser.parse_args()

    if args.input:
        with open(args.input) as f:
            text = f.read()
    elif args.text:
        text = args.text
    else:
        text = sys.stdin.read()

    results = validate(text, mode=args.mode)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_report(results))


if __name__ == "__main__":
    main()
