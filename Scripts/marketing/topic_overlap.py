#!/usr/bin/env python3
"""Guard against the content pipeline republishing a topic it already covered.

Peak Interval is down to 28 posts after commit 5e9fc2b pruned 89 generic
fitness posts that Google indexed at 4%. What survived is the app lane —
timers, interval formats, named competitors, how-to-build-X — which indexes at
71%. That makes the surviving corpus small but DENSE: half a dozen posts about
choosing an interval timer legitimately resemble each other, so scores here run
higher than in a broad corpus and the thresholds are set accordingly.

This scores a candidate against every published post and queued theme so the
near-misses surface before they ship. It also scores against `retired`, which
now holds all 89 pruned slugs — rewriting one of those would recreate exactly
the content Google already refused.

Modes:

  index                     Print every published post and queued theme as
                            slug + search intent, newest last. Read this before
                            choosing any new topic.

  audit                     Score every queued theme against every published
                            post and against the other queued themes, and print
                            each one's closest existing coverage.

  check "<slug>" "<text>"   Score one candidate against the corpus. `text`
                            should be the theme + hook + target query. Exits
                            non-zero on a blatant repeat.

Similarity is IDF-weighted cosine over unigrams and bigrams drawn from the
slug, title and description — the fields that encode search intent. Words that
appear in nearly every Peak Interval post ("hiit", "workout") lose weight
automatically, so two posts do not look alike merely for being about intervals.

The score is triage, not truth. It compares words, so a duplicate phrased in
unfamiliar vocabulary slips through; `review` means read the neighbour and
judge it yourself. The hard failure only catches near-identical phrasings.

Two known false positives, both deliberate commercial series:
`peak-interval-vs-<competitor>` posts score 0.35-0.49 against each other
because only the competitor's name differs, and the `best-<format>-timer` posts
score 0.33-0.62 for the same reason. If the closest neighbour is a sibling in
one of those series and the format or competitor genuinely differs, it is not a
duplicate — ship it.

One real duplicate survived the prune: best-emom-timer and best-tabata-timer at
0.62. Consolidating that pair is worth more than a new post.
"""

from __future__ import annotations

import json
import math
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
POSTS_DIR = ROOT / "blog/posts"
QUEUE = ROOT / "docs/marketing/content-queue.json"

# Calibrated 2026-08-23 against the post-prune corpus (28 posts, 378 pairs):
# median 0.053, p90 0.143, p99 0.486, max 0.619. The survivors are commercially
# clustered — best-*-timer and peak-interval-vs-* posts sit at 0.33-0.62 by
# design — so BLOCK sits ABOVE p99 to avoid rejecting legitimate members of
# those series, and REVIEW sits near p95 to force a human read instead.
# Re-run `calibrate` once the corpus passes ~45 posts; a broad corpus will pull
# these down again.
BLOCK = 0.50     # near-identical topic — refuse outright
REVIEW = 0.22    # close enough that you must read it and justify the difference

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "best", "but", "by", "can", "do",
    "does", "for", "from", "get", "getting", "go", "guide", "has", "have", "how",
    "i", "in", "is", "it", "its", "my", "no", "not", "of", "off", "on", "one",
    "or", "our", "out", "over", "so", "that", "the", "their", "them", "then",
    "they", "this", "to", "up", "want", "was", "what", "when", "where", "which",
    "who", "why", "will", "with", "without", "you", "your",
}

# Fitness writing says the same thing many ways, and without this map two posts
# on the same subject share almost no vocabulary and score as unrelated — which
# is exactly the duplicate this exists to catch. Each group collapses to its
# first member. Deliberately NOT merged: run and cycle (modality-specific posts
# are genuinely different), and beginner and advanced (audience is the topic).
SYNONYM_GROUPS = [
    ("hiit", "interval", "intervals", "tabata", "sit", "hiis", "emom", "amrap",
     "circuit", "circuits"),
    ("workout", "workouts", "training", "train", "session", "sessions",
     "exercise", "exercises", "routine", "routines"),
    ("timer", "timers", "stopwatch", "clock", "app", "apps", "application"),
    ("fat", "weight", "loss", "burn", "burning", "lose", "losing", "cut",
     "cutting", "lean", "slim"),
    ("recovery", "recover", "recovering", "rest", "resting", "cooldown",
     "deload", "soreness", "sore"),
    ("heart", "hr", "cardio", "aerobic", "anaerobic", "vo", "vomax", "zone",
     "zones", "bpm"),
    ("strength", "strengthening", "weights", "dumbbell", "dumbbells",
     "kettlebell", "kettlebells", "barbell", "resistance", "lifting"),
    ("muscle", "muscles", "hypertrophy", "gains", "mass"),
    ("nutrition", "diet", "food", "eating", "meal", "meals", "protein", "carbs",
     "carbohydrate", "fuel", "fueling", "supplement", "supplements"),
    ("endurance", "stamina", "conditioning", "fitness", "capacity", "performance"),
    ("plan", "plans", "program", "programs", "programming", "challenge",
     "schedule", "periodization", "progression", "progressive"),
    ("quick", "short", "fast", "busy", "minute", "minutes", "brief"),
    ("home", "apartment", "indoor", "indoors", "small", "space", "bodyweight",
     "equipmentfree", "minimal"),
    ("gym", "outdoor", "outdoors", "outside", "park"),
    ("watch", "apple", "wearable", "tracker", "wearables"),
    ("injury", "injuries", "pain", "safe", "safety", "form", "technique",
     "prevention", "prevent"),
    ("beginner", "beginners", "starting", "start", "starter", "new", "novice"),
    ("advanced", "elite", "athlete", "athletes", "pro", "expert", "experienced"),
    ("women", "woman", "female", "females"),
    ("men", "man", "male", "males"),
    ("senior", "seniors", "older", "aging", "age", "elderly"),
    ("science", "research", "study", "studies", "evidence", "physiology",
     "metabolic", "metabolism", "epoc", "afterburn"),
    ("motivation", "motivated", "consistency", "consistent", "habit", "habits",
     "discipline", "adherence"),
    ("alternative", "alternatives", "versus", "vs", "compared", "comparison",
     "switch", "switching"),
]
SYNONYMS = {word: group[0] for group in SYNONYM_GROUPS for word in group}

FRONT_MATTER = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)


def tokenize(text: str) -> list[str]:
    words = [
        SYNONYMS.get(w, w)
        for w in re.findall(r"[a-z]+", text.lower())
        if w not in STOPWORDS
    ]
    # Collapse runs the synonym map created ("interval training" -> "hiit hiit").
    deduped = [w for i, w in enumerate(words) if i == 0 or w != words[i - 1]]
    bigrams = [f"{a}_{b}" for a, b in zip(deduped, deduped[1:])]
    return deduped + bigrams


def front_matter_field(block: str, field: str) -> str:
    """Reads one scalar YAML field without a YAML dependency."""
    match = re.search(rf"^{field}:\s*(.*)$", block, re.M)
    if not match:
        return ""
    return match.group(1).strip().strip('"').strip("'")


def load_posts() -> list[tuple[str, str]]:
    """Published posts as (slug, intent text): slug words + title + description."""
    entries = []
    for path in sorted(POSTS_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8", errors="replace")
        match = FRONT_MATTER.match(text)
        block = match.group(1) if match else ""
        slug = path.stem
        title = front_matter_field(block, "title")
        description = front_matter_field(block, "description")
        entries.append((slug, " ".join([slug.replace("-", " "), title, description])))
    if not entries:
        sys.exit(f"error: parsed zero posts out of {POSTS_DIR} — is the path right?")
    return entries


def load_queue() -> tuple[dict, list[tuple[str, str]]]:
    if not QUEUE.exists():
        return {"themes": [], "retired": []}, []
    data = json.loads(QUEUE.read_text())
    entries = []
    for theme in data.get("themes", []):
        text = " ".join(
            [
                theme.get("slug", "").replace("-", " "),
                theme.get("theme", ""),
                theme.get("query", ""),
            ]
        )
        entries.append((theme.get("slug", "?"), text))
    return data, entries


def load_retired() -> list[tuple[str, str]]:
    """Deliberately rejected topics, scored like published ones.

    Without this the 89 posts pruned in 5e9fc2b would look like FREE topics to
    the pipeline rather than forbidden ones, and it would cheerfully rewrite
    the exact content Google declined to index. A retired slug only carries its
    own words, which is enough to catch a rewrite under the same name or a
    close paraphrase.
    """
    if not QUEUE.exists():
        return []
    data = json.loads(QUEUE.read_text())
    return [
        (item.get("slug", "?"), item.get("slug", "").replace("-", " "))
        for item in data.get("retired", [])
        if item.get("slug")
    ]


def idf(corpus: list[list[str]]) -> dict[str, float]:
    n = len(corpus)
    seen = Counter()
    for tokens in corpus:
        seen.update(set(tokens))
    return {term: math.log((n + 1) / (count + 1)) + 1 for term, count in seen.items()}


def vector(tokens: list[str], weights: dict[str, float]) -> dict[str, float]:
    counts = Counter(tokens)
    vec = {t: c * weights.get(t, 1.0) for t, c in counts.items()}
    norm = math.sqrt(sum(v * v for v in vec.values())) or 1.0
    return {t: v / norm for t, v in vec.items()}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    smaller, larger = (a, b) if len(a) < len(b) else (b, a)
    return sum(v * larger.get(t, 0.0) for t, v in smaller.items())


def build(extra: list[tuple[str, str]] | None = None):
    published = load_posts()
    _, queued = load_queue()
    retired = load_retired()
    labelled = (
        [("published", s, t) for s, t in published]
        + [("queued", s, t) for s, t in queued]
        + [("retired", s, t) for s, t in retired]
        + [("candidate", s, t) for s, t in (extra or [])]
    )
    tokenized = [(kind, slug, tokenize(text)) for kind, slug, text in labelled]
    weights = idf([tokens for _, _, tokens in tokenized])
    return [(kind, slug, vector(tokens, weights)) for kind, slug, tokens in tokenized]


def neighbours(target: dict[str, float], corpus, skip_slug: str, limit: int = 3):
    scored = [
        (cosine(target, vec), kind, slug)
        for kind, slug, vec in corpus
        if slug != skip_slug and kind != "candidate"
    ]
    return sorted(scored, reverse=True)[:limit]


def show_index() -> int:
    for slug, text in load_posts():
        rest = text.split(slug.replace("-", " "), 1)[-1].strip()
        print(f"published  {slug}\n           {rest[:150]}")
    _, queued = load_queue()
    for slug, text in queued:
        print(f"queued     {slug}\n           {text[:150]}")
    return 0


def calibrate() -> int:
    """Prints the live pairwise score distribution, so the thresholds above
    can be justified against the corpus rather than inherited from another
    repo with a quarter as many posts."""
    corpus = [(k, s, v) for k, s, v in build() if k in ("published", "queued")]
    scores = sorted(
        cosine(a[2], b[2])
        for i, a in enumerate(corpus)
        for b in corpus[i + 1:]
    )
    if not scores:
        sys.exit("no pairs to score")
    def pct(p: float) -> float:
        return scores[min(len(scores) - 1, int(len(scores) * p))]
    print(f"{len(corpus)} items, {len(scores)} pairs")
    for label, p in [("median", 0.5), ("p90", 0.9), ("p99", 0.99), ("p999", 0.999)]:
        print(f"  {label:6} {pct(p):.3f}")
    print(f"  max    {scores[-1]:.3f}")
    print(f"\nthresholds in use: REVIEW {REVIEW}, BLOCK {BLOCK}")
    print("Top 10 closest existing pairs (these are the real duplicates, if any):")
    ranked = sorted(
        ((cosine(a[2], b[2]), a[1], b[1]) for i, a in enumerate(corpus) for b in corpus[i + 1:]),
        reverse=True,
    )[:10]
    for score, one, two in ranked:
        print(f"  {score:.2f}  {one}  <->  {two}")
    return 0


def audit() -> int:
    corpus = build()
    blocked = 0
    queued_count = 0
    for kind, slug, vec in corpus:
        if kind != "queued":
            continue
        queued_count += 1
        top = neighbours(vec, corpus, slug)
        worst = top[0][0] if top else 0.0
        marker = "BLOCK" if worst >= BLOCK else ("review" if worst >= REVIEW else "ok")
        blocked += worst >= BLOCK
        print(f"[{marker:6}] {slug}")
        for score, other_kind, other_slug in top:
            print(f"           {score:.2f}  {other_kind}: {other_slug}")
    if not queued_count:
        print("queue is empty — nothing to audit")
        return 0
    print(
        f"\nReview anything at {REVIEW:.2f}+: read that neighbour and be able to say "
        f"what different question this post answers. Rewrite or drop it if you can't."
    )
    return 1 if blocked else 0


def check(slug: str, text: str) -> int:
    # Exact-slug collisions are checked before scoring, because neighbours()
    # skips same-slug pairs as "itself" — which would silently wave through a
    # rewrite of a pruned post under its original name, the likeliest mistake
    # of all now that 89 slugs sit in `retired`.
    data, _ = load_queue()
    for item in data.get("retired", []):
        if item.get("slug") == slug:
            print(f"candidate: {slug}\n\nREJECT: this slug is retired.\n  {item.get('reason', '')}")
            return 1
    for path in POSTS_DIR.glob("*.md"):
        if path.stem == slug:
            print(f"candidate: {slug}\n\nREJECT: {slug} is already published at blog/posts/{slug}.md.")
            return 1

    corpus = build(extra=[(slug, f"{slug.replace('-', ' ')} {text}")])
    target = next(vec for kind, s, vec in corpus if kind == "candidate" and s == slug)
    top = neighbours(target, corpus, slug, limit=5)
    print(f"candidate: {slug}")
    for score, kind, other in top:
        flag = " <-- BLOCK" if score >= BLOCK else (" <-- review" if score >= REVIEW else "")
        print(f"    {score:.2f}  {kind}: {other}{flag}")
    if top and top[0][0] >= BLOCK:
        print(f"\nREJECT: {top[0][2]} already covers this ({top[0][0]:.2f}). Pick another topic.")
        return 1
    if top and top[0][0] >= REVIEW:
        print(
            f"\nREVIEW: closest is {top[0][2]} ({top[0][0]:.2f}). Read it. State in the queue "
            f"entry's `distinctFrom` what different question this post answers."
        )
    return 0


def main() -> int:
    args = sys.argv[1:]
    if args and args[0] == "index":
        return show_index()
    if args and args[0] == "audit":
        return audit()
    if args and args[0] == "calibrate":
        return calibrate()
    if len(args) == 3 and args[0] == "check":
        return check(args[1], args[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
