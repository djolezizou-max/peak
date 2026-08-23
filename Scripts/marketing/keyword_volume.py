#!/usr/bin/env python3
"""Google Keyword Planner volume, for steering the content queue by demand.

The pipeline's themes come from pain signals — Reddit threads and fitness
creators. That finds what people struggle with, which is good inspiration,
but says nothing about how many of them type it into Google. Peak Interval
already has 118 posts written from an idea list rather than from demand data,
so this is the other half of the input: what actually gets searched.

It is a DISCOVERY tool, not a gate. Reddit-sourced themes are not required to
have measurable volume, and `volume` mode is far too unreliable to reject
anything on (see below).

Modes:

  ideas --seeds "chores" "screen time"      Expanded keyword ideas with monthly
        [--urls <blog url> ...]             volume. Seeds MUST be short head
        [--min-volume 100] [--limit 40]     terms; see the warning below.

  volume "<exact phrase>" ["<phrase>" ...]  Monthly volume for exact phrases,
                                            no expansion. Use to sanity-check
                                            a query before committing to it.

IMPORTANT — seeds must be SHORT. A conversational seed like "how long should
a hiit workout be" returns zero ideas, while "hiit" returns a full set, and a
blog-post URL seed works well too. Feed it head terms (1-2 words) or our own
post URLs, and let the expansion surface the long-tail phrasing.

Reading the numbers honestly:

- **`volume`'s coverage is spotty and the pattern is unexplained** (probed
  2026-08-22). It reports "kids" at 823,000/mo, "kids toys" at 74,000 and
  "chore chart for teens" at 1,600 — but returns nothing at all for
  "children", "toddler", "kids chores" or "screen time for kids". So the gaps
  are not about phrase length, long-tail-ness, or the word "kids", and they
  are not explained by the keyword being absent from `ideas` output either
  ("chore chart" reports 14,800 while never appearing as an idea for seed
  "chores"). Switching keyword_plan_network changes nothing. Whatever the
  cause, a blank here means NOT REPORTED and proves nothing about a phrase:
  never use it to reject a topic. `ideas` is the trustworthy mode — the
  volumes it returns alongside its expansions are consistent.
- Volume is US English unless --geo/--language say otherwise, and is a rounded
  12-month average, so it is a magnitude, not a precise count.
- High volume with HIGH competition is usually commercial intent other people
  pay for; our wins are the informational middle.
- Fitness seeds drag in adjacent commercial intent — supplement, gym
  membership and equipment queries that a blog post cannot serve and that ad
  budgets already own. Read the intent behind each idea, do not just sort by
  volume.

Credentials come from the google-ads skill's config (developer token + refresh
token), so this works only on this machine.
"""
import argparse
import re
import sys

GOOGLE_ADS_SKILL = "/Users/djordjejankovicmacmini/.claude/skills/google-ads"
sys.path.insert(0, GOOGLE_ADS_SKILL)

US = "geoTargetConstants/2840"
ENGLISH = "languageConstants/1000"

# Expansion drags in generic fragments that are not topics anyone can write a
# post for ("make it make", "a chores"). Cheap prefilter; the human still judges.
JUNK = re.compile(
    r"^(a|the|an|to|of|in|is|it)\s|\s(a|the|an)$|^\W*$|^.{1,3}$",
    re.IGNORECASE,
)


def client_and_customer():
    try:
        from google_ads_helper import get_client
    except ImportError as exc:  # pragma: no cover - environment problem
        sys.exit(
            f"Could not import the google-ads helper from {GOOGLE_ADS_SKILL}: {exc}\n"
            "That skill holds the developer token and refresh token this script needs."
        )
    return get_client()


def fmt(rows, min_volume, limit):
    """Sorted, filtered table. Returns the number dropped for the caller."""
    kept = [r for r in rows if r[1] >= min_volume and not JUNK.search(r[0])]
    dropped = len(rows) - len(kept)
    kept.sort(key=lambda r: -r[1])
    for text, volume, competition in kept[:limit]:
        print(f"{volume:>8}/mo  {competition:<8}  {text}")
    return len(kept), dropped


def cmd_ideas(args):
    client, customer_id = client_and_customer()
    service = client.get_service("KeywordPlanIdeaService")

    request = client.get_type("GenerateKeywordIdeasRequest")
    request.customer_id = customer_id
    request.language = args.language
    request.geo_target_constants.append(args.geo)
    request.include_adult_keywords = False

    long_seeds = [s for s in (args.seeds or []) if len(s.split()) > 3]
    if long_seeds:
        print(
            f"WARNING: {len(long_seeds)} seed(s) are conversational phrases; those "
            "reliably return nothing. Use 1-2 word head terms.\n",
            file=sys.stderr,
        )

    # The API takes keyword seeds OR url seeds OR both-as-one; both-as-one is
    # the useful shape here (our own post + the head term it targets).
    if args.seeds and args.urls:
        request.keyword_and_url_seed.url = args.urls[0]
        request.keyword_and_url_seed.keywords.extend(args.seeds)
        if len(args.urls) > 1:
            print("NOTE: only the first --url is used when seeds are also given.", file=sys.stderr)
    elif args.urls:
        request.url_seed.url = args.urls[0]
    elif args.seeds:
        request.keyword_seed.keywords.extend(args.seeds)
    else:
        sys.exit("Give --seeds and/or --urls.")

    try:
        response = service.generate_keyword_ideas(request=request)
        rows = [
            (r.text, r.keyword_idea_metrics.avg_monthly_searches or 0,
             r.keyword_idea_metrics.competition.name if r.keyword_idea_metrics.competition else "-")
            for r in response
        ]
    except Exception as exc:
        sys.exit(f"Keyword Planner request failed: {type(exc).__name__}: {exc}")

    if not rows:
        sys.exit(
            "No ideas returned. Almost always the seeds were too long — retry with "
            "head terms like 'chores' or 'screen time', or seed with a blog post URL."
        )

    kept, dropped = fmt(rows, args.min_volume, args.limit)
    print(
        f"\n{kept} ideas at >= {args.min_volume}/mo "
        f"({dropped} dropped as junk or below threshold, {len(rows)} returned).",
        file=sys.stderr,
    )


def cmd_volume(args):
    client, customer_id = client_and_customer()
    service = client.get_service("KeywordPlanIdeaService")

    request = client.get_type("GenerateKeywordHistoricalMetricsRequest")
    request.customer_id = customer_id
    request.language = args.language
    request.geo_target_constants.append(args.geo)
    request.keywords.extend(args.keywords)

    try:
        response = service.generate_keyword_historical_metrics(request=request)
    except Exception as exc:
        sys.exit(f"Keyword Planner request failed: {type(exc).__name__}: {exc}")

    measured = {}
    for result in response.results:
        metrics = result.keyword_metrics
        measured[result.text.lower()] = (
            metrics.avg_monthly_searches or 0,
            metrics.competition.name if metrics.competition else "-",
        )

    unreported = 0
    for keyword in args.keywords:
        hit = measured.get(keyword.lower())
        if hit is None or hit[0] == 0:
            unreported += 1
            print(f"{'not reported':>12}  {'-':<8}  {keyword}")
        else:
            print(f"{str(hit[0]) + '/mo':>12}  {hit[1]:<8}  {keyword}")
    if unreported:
        print(
            f"\n{unreported} of {len(args.keywords)} not reported. That is NOT evidence of "
            "low demand — this endpoint returns 0 for plainly-popular phrases on this "
            "account (see the module docstring). Do not reject a topic on it.",
            file=sys.stderr,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--geo", default=US, help="geo target constant (default US)")
    parser.add_argument("--language", default=ENGLISH, help="language constant (default English)")
    sub = parser.add_subparsers(dest="mode", required=True)

    ideas = sub.add_parser("ideas", help="expanded keyword ideas with volume")
    ideas.add_argument("--seeds", nargs="*", help="SHORT head terms, 1-2 words")
    ideas.add_argument("--urls", nargs="*", help="seed from page content, e.g. one of our blog posts")
    ideas.add_argument("--min-volume", type=int, default=100)
    ideas.add_argument("--limit", type=int, default=40)
    ideas.set_defaults(func=cmd_ideas)

    volume = sub.add_parser("volume", help="exact-phrase monthly volume, no expansion")
    volume.add_argument("keywords", nargs="+")
    volume.set_defaults(func=cmd_volume)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
