#!/usr/bin/env python3
"""Grade one unslop eval output.

    tells.py EVALS_JSON EVAL_ID OUTPUT_FILE [INPUT_FILE] > grading.json

The mechanical rules a regex can find (13, 17, 18, 19, 1, 4, 7, 8, 9, 16,
20, 22, 23, 26, 31), the facts the prompt said to keep, the quoted text
that must survive as written, a length band, and a fragment count as the
over-compression proxy from the Guards section. The judgment half of the
skill (soul, rhythm, opinions) is for the creator in the viewer.
"""
import json
import re
import sys

EM_DASH = "—"
CURLY = re.compile("[‘’“”]")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐⬆✅❌✨⭕\U0001F000-\U0001F2FF]")
VOCAB = (
    # rule 1
    "pivotal moment", "testament to", "evolving landscape", "setting the stage", "indelible mark", "deeply rooted",
    "game-changer", "game changer",
    # rule 4
    "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit", "seamless", "seamlessly", "robust",
    # rule 7
    "additionally", "crucial", "delve", "delves", "delving", "enduring", "enhance", "enhances", "enhanced", "fostering", "foster", "fostered",
    "garner", "interplay", "intricate", "landscape", "pivotal", "showcase", "showcases", "showcasing", "tapestry", "testament", "underscore", "underscores",
    # rule 8
    "serves as", "stands as", "boasts",
    # rule 26
    "substrate", "wedge", "vector", "locus", "vantage", "nexus", "bedrock", "scaffolding", "modality", "paradigm", "gold-plating",
    "north star", "flywheel", "endgame",
    # rule 31
    "utilize", "utilizes", "utilizing", "leverage", "leverages", "leveraging", "facilitate", "facilitates", "numerous",
)
FILLER = (
    "in order to", "due to the fact that", "it is important to note", "it's worth noting", "it is worth noting",
    "in the event that", "at the end of the day",
)
NOT_JUST = re.compile(r"\bnot (just|only|merely)\b[^.!?\n]{0,80}\bbut\b", re.I)
CHATBOT = (
    "hope this helps", "let me know", "let us know", "feel free", "certainly", "great question", "absolutely right",
    "of course!", "thrilled", "excited to announce", "excited to share", "stay tuned", "happy to help", "we'd love to hear",
    "we would love to hear", "we're excited", "we are excited",
)
ASIDES = (
    "honestly", "the credit goes to", "not going to pretend", "the kind of thing that", "easy to feel", "made it easy",
    "rather than silently", "rather than quietly", "worth it", "we'll take it", "we read all of it", "i'll be straight",
    "to be fair", "if we're honest", "shouldn't be able to", "bigger than the version number", "i'd be lying",
    "the part that bugs me", "what bugs me", "the honest answer", "no small thing", "in a good way",
)
BOLD_LABEL = re.compile(r"^\s*(?:(?:[-*]|\d+\.)\s+)?\*\*[^*\n]+:\*\*", re.M)
SPACED_EN_DASH = re.compile(r"\s\u2013\s")
HEADING = re.compile(r"^(#{1,6})\s+(.*)$", re.M)
CODE_BLOCK = re.compile(r"```.*?```", re.S)
CODE_SPAN = re.compile(r"`[^`\n]*`")
URL = re.compile(r"https?://\S+")


HEADING_WORDS = set("""new started getting matters summary changes testing tests test notes overview details steps
guide usage next why what how it the and of for with to plan results background motivation context impact risk rollback
timeline status update fix fixes performance security stability upgrade install started""".split())


def squash(s):
    """Whitespace, blockquote markers, line breaks and quote style do not count as a change to quoted text."""
    s = re.sub(r"(?m)^\s*>\s?", "", s)
    s = s.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
    return re.sub(r"\s+", " ", s).strip()


def prose_of(text):
    """Text minus code blocks, code spans, and URLs; the rules are about prose."""
    return URL.sub("", CODE_SPAN.sub("", CODE_BLOCK.sub("", text)))


QUOTE_CLASS = {"'": "['\u2018\u2019]", '"': '["\u201c\u201d]'}


def without_verbatim(text, verbatim):
    """Cut each quoted passage out however it was wrapped or re-quoted, so its own tells are not counted."""
    out = text
    for v in verbatim:
        pat = "".join("[\\s>]+" if ch == " " else QUOTE_CLASS.get(ch, re.escape(ch)) for ch in squash(v))
        # the quotation marks that wrap the passage belong to it too
        out = re.sub('["\u201c]?' + pat + '["\u201d]?', " ", out)
    return out


def sentences(prose):
    body = "\n".join(l for l in prose.splitlines() if not l.lstrip().startswith(("#", ">", "-", "*", "|")))
    parts = re.split(r"(?<=[.!?])\s+", body)
    return [p.strip() for p in parts if p.strip()]


def main():
    evals_path, eval_id, out_path = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    in_path = sys.argv[4] if len(sys.argv) > 4 else None
    ev = next(e for e in json.load(open(evals_path))["evals"] if e["id"] == eval_id)
    try:
        text = open(out_path).read()
    except FileNotFoundError:
        exp = [{"text": f"The output file {ev['output']} exists", "passed": False, "evidence": "not written"}]
        print(json.dumps({"expectations": exp, "summary": {"passed": 0, "failed": 1, "total": 1, "pass_rate": 0.0}}, indent=2))
        return
    verbatim = ev.get("verbatim", [])
    # the harness appends its own attribution footer to a PR body; not the model's prose
    text = re.sub(r"\n+\U0001F916 Generated with \[Claude Code\][^\n]*\n?(Co-Authored-By:[^\n]*\n?)*$", "\n", text)
    stripped = without_verbatim(text, verbatim)
    prose = prose_of(stripped)
    low = prose.lower()
    exp = []

    def add(text_, passed, evidence):
        exp.append({"text": text_, "passed": bool(passed), "evidence": evidence})

    n = stripped.count(EM_DASH)
    en = len(SPACED_EN_DASH.findall(stripped))
    add("No em dashes or spaced en dashes outside quoted text (rule 13)", n == 0 and en == 0, f"{n} em dash(es), {en} spaced en dash(es)")
    n = len(CURLY.findall(stripped))
    add("No curly quotes outside quoted text (rule 19)", n == 0, f"{n} curly quote(s)")
    bad = []
    for _, title in HEADING.findall(stripped):
        words = [w for w in re.sub(r"[`*_]", "", title).split()[1:] if not w.isupper()]
        caps = [w for w in words if w[0].isupper()]
        if len(caps) >= 2 or any(w.lower().strip("'s") in HEADING_WORDS or w.lower() in HEADING_WORDS for w in caps):
            bad.append(title)
    add("Headings are sentence case (rule 17)", not bad, "title case: " + "; ".join(bad) if bad else f"{len(HEADING.findall(stripped))} heading(s), all sentence case")
    n = len(EMOJI.findall(stripped))
    add("No emoji (rule 18)", n == 0, f"{n} emoji")
    hits = {w: len(re.findall(rf"\b{re.escape(w)}\b", low)) for w in VOCAB}
    hits = {w: c for w, c in hits.items() if c}
    add("No AI vocabulary, puffery, or metaphor nouns (rules 1, 4, 7, 8, 26, 31)", not hits, ", ".join(f"{w} x{c}" for w, c in hits.items()) or "none")
    hits = {w: len(re.findall(rf"\b{re.escape(w)}\b", low)) for w in FILLER}
    hits = {w: c for w, c in hits.items() if c}
    nj = NOT_JUST.findall(prose)
    add("No filler phrases or 'not just X but Y' (rules 9, 23)", not hits and not nj,
        ", ".join(f'"{w}" x{c}' for w, c in hits.items()) + (f"; not-just x{len(nj)}" if nj else "") or "none")
    hits = {w: low.count(w) for w in CHATBOT}
    hits = {w: c for w, c in hits.items() if c}
    add("No chatbot or sycophantic phrases (rules 20, 22)", not hits, ", ".join(f'"{w}" x{c}' for w, c in hits.items()) or "none")
    n = len(BOLD_LABEL.findall(stripped))
    add("No bullet or paragraph opens with a bold label and a colon (rule 16)", n == 0, f"{n} bold-label line(s)")

    hits = {w: low.count(w) for w in ASIDES}
    hits = {w: c for w, c in hits.items() if c}
    add("No knowing asides (rule 34, proxy: a phrase list from iteration 1)", not hits, ", ".join(f'"{w}" x{c}' for w, c in hits.items()) or "none")

    missing = []
    for f in ev.get("facts", []):
        if f.startswith("re:"):
            ok = re.search(f[3:], text, re.I) is not None
        else:
            ok = f in text
        if not ok:
            missing.append(f)
    add(f"Every fact survives ({len(ev.get('facts', []))} checked)", not missing, "missing: " + ", ".join(missing) if missing else "all present")

    if verbatim:
        lost = [v for v in verbatim if squash(v) not in squash(text)]
        add("Quoted text survives as written (Guards)", not lost, "changed: " + " | ".join(squash(v)[:60] for v in lost) if lost else "intact, including its own tells")

    words = len(prose_of(text).split())
    band = ev.get("length", {})
    if "max_words" in band:
        add(f"Under {band['max_words']} words", words <= band["max_words"], f"{words} words")
    elif in_path and band:
        src = len(prose_of(open(in_path).read()).split())
        lo, hi = int(src * band.get("min_ratio", 0)), int(src * band.get("max_ratio", 99))
        add(f"Length between {int(band.get('min_ratio', 0)*100)}% and {int(band.get('max_ratio', 99)*100)}% of the input", lo <= words <= hi, f"{words} words against {src} in the input")

    sents = sentences(prose)
    frags = [s for s in sents if len(s.split()) < 4]
    notx = [s for s in sents if re.match(r"Not\b", s) and len(s.split()) <= 5]
    share = len(frags) / len(sents) if sents else 0
    add("Not over-corrected: under 15% fragments, no 'Not X.' closers (Guards)", share <= 0.15 and not notx,
        f"{len(frags)}/{len(sents)} sentences under 4 words" + ("; " + " | ".join(notx) if notx else ""))

    passed = sum(e["passed"] for e in exp)
    print(json.dumps({"expectations": exp, "summary": {"passed": passed, "failed": len(exp) - passed, "total": len(exp), "pass_rate": round(passed / len(exp), 3)}}, indent=2))


if __name__ == "__main__":
    main()
