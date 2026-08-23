---
name: content-pipeline
description: Peak Interval blog automation. "research" mode (weekly) fills a theme queue from Reddit, fitness creators, Search Console and keyword volume; "publish" mode (daily) ships one blog post. Use when asked to run the content pipeline or when invoked by the scheduled jobs.
---

# Peak Interval Content Pipeline

Modes, selected by the argument: `research` (weekly), `publish` (daily).
No argument = `publish`. **Blog only** — Peak Interval's social publishing runs
on its own separate pipeline, so this one never touches Planoly or carousels.

The site is **Eleventy**, not Next.js: posts are markdown files in
`blog/posts/<slug>.md` with YAML front matter, built with `npm run build`,
deployed to Vercel from `main`. Live URLs are
`https://peakintervalapp.com/blog/posts/<slug>/` — note the `/posts/` segment,
which the IndexNow and index-check steps both need.

The queue lives at `docs/marketing/content-queue.json`:
```json
{ "themes": [ { "slug": "...", "theme": "...", "hook": "...", "query": "...",
    "evidence": "one line citing the Reddit/creator signal", "pain_quotes": ["..."],
    "category": "one of the existing categories, exactly",
    "distinctFrom": "closest existing slug — and the different question this answers",
    "searchEvidence": "striking-distance query with impressions/position, or a keyword with its monthly volume",
    "imagePrompt": "what the featured image should show" } ],
  "retired": [ { "slug": "...", "reason": "duplicate of <slug>", "date": "2026-08-23" } ] }
```
Publish runs remove the FIRST theme after shipping its post. Research runs
append. Commit queue changes with the rest of the run.

`retired` is the memory of topics deliberately rejected. Never re-propose a
retired slug or its question — read the list every research run.

**Categories are a closed set.** Use one of these exactly, or the post falls out
of the category pages: `Workout Guides`, `Specialized HIIT Training`,
`HIIT Fundamentals`, `Fitness + Nutrition`, `Advanced HIIT Concepts`,
`App Features`, `HIIT Success Stories`, `Buying Guides`, `Comparisons`.

## Stay in the app lane — this is the whole strategy

On 2026-08-23, commit `5e9fc2b` deleted 89 of the 117 posts. The reason is the
single most important thing to understand before choosing any topic. Search
Console showed only 31 of 132 URLs indexed, split by intent like this:

| Lane | Posts | Indexed |
|---|---|---|
| App lane — timers, interval formats, named competitors, how-to-build-X | 24 | 71% |
| Generic fitness editorial — sleep, protein, carb cycling, mental health | 93 | 4% |

Google predicts a page's value from the rest of the domain before it spends a
crawl, so the generic library was not merely useless: at 79% of the site's URLs
returning almost nothing, it was capping crawl demand for the pages that do
work. All 89 pruned slugs are in the queue's `retired` list and the gate scores
against them.

**So: do not write generic fitness editorial.** A post about sleep, macros,
motivation, or the physiology of EPOC is off-strategy here no matter how strong
the Reddit signal behind it. Good topics for this blog answer a question
someone asks *while trying to run intervals* — which timer, which format, how
to set up a specific workout, how the Watch flow works, how Peak Interval
compares to a named competitor, how to build a specific protocol.

That constraint is what makes this pipeline different from QuestSpark's, where
any parenting pain point is fair game.

## Never publish the same topic twice

28 posts remain, and they are commercially dense: half a dozen legitimately
resemble each other because they are all about choosing an interval timer. The
gate is not optional:

```bash
python3 Scripts/marketing/topic_overlap.py index      # every published + queued topic
python3 Scripts/marketing/topic_overlap.py audit      # queue vs published, closest neighbours
python3 Scripts/marketing/topic_overlap.py calibrate  # live score distribution + worst existing pairs
python3 Scripts/marketing/topic_overlap.py check "<slug>" "<theme> <hook> <query>"
```

`check` refuses outright in three cases: the slug is already published, the
slug is in `retired`, or the closest neighbour scores 0.50+. At 0.22+ you must
**open the closest neighbour in `blog/posts/` and read it**, then write one
sentence in `distinctFrom` naming that slug and the different question your
post answers. If you cannot write that sentence honestly, drop the topic.

Thresholds were calibrated against the post-prune corpus on 2026-08-23 (28
posts, median pair 0.053, p99 0.486, max 0.619), not inherited. They sit higher
than QuestSpark's precisely because this corpus is dense. Re-run `calibrate`
once the corpus passes ~45 posts.

Two deliberate false positives, both commercial series: `peak-interval-vs-*`
posts score 0.35-0.49 against each other, and `best-<format>-timer` posts score
0.33-0.62. If the closest neighbour is a sibling in one of those series and the
competitor or format genuinely differs, ship it. One real duplicate survived
the prune — `best-emom-timer` and `best-tabata-timer` at 0.62 — and
consolidating that pair is worth more than a new post.

A fresh angle, a newer study, or a different exercise list is not a different
topic. A different *question someone typed into Google* is.

## Let search results steer the queue

Peak Interval's posts were written from an idea list with no feedback from
search, which is exactly how 89 of them ended up deleted. Both properties are
wired into the
globally-registered `app-analytics` MCP server, so that loop can close:

- `query_search_analytics` — Google clicks, impressions, CTR, position. Pass
  `siteUrl: "sc-domain:peakintervalapp.com"`; the default is QuestSpark's
  property, so **always pass it explicitly** or you will report the wrong site.
- `inspect_search_console_url` — live Google index status for one URL.
- `get_bing_url_info` — Bing crawl/index status. Pass
  `siteUrl: "https://peakintervalapp.com/"` (URL-prefix form, trailing slash).
- `get_bing_traffic_stats` — Bing impressions, clicks and InIndex page count.

Four things about this data that will mislead you if you forget them:

- **A missing row is not a zero.** Search Analytics returns a row only where
  there was at least one impression. A post absent from a `page` breakdown has
  never surfaced — that is NOT evidence it is unindexed. Only
  `inspect_search_console_url` answers indexing.
- **The last 2-3 days are partial.** Draw no conclusions from them.
- **Query rows are anonymised** for rare queries, so query-level numbers never
  sum to site totals. Page-level rows are complete.
- **New posts are slow.** Days to weeks before impressions accumulate, and
  position 40-90 means indexed but not competitive, not failed. Judge no post
  earlier than **21 days** after publishing.

## Mode: research (weekly — Monday)

1. Run `topic_overlap.py index` and read the `retired` list. New themes must
   duplicate no published post, no queued theme, and no retired slug. Also skim
   `blog-post-ideas.md` for anything still un-DONE worth reviving.
2. Research demand signals, scoped to the subreddits in
   `docs/marketing/reddit-communities.md` (broad fitness keyword searches come
   back full of supplement spam and gym selfies):
   - xpoz `getRedditPostsByKeywords` / `getRedditCommentsByKeywords` over
     r/hiit, r/fitness, r/xxfitness, r/bodyweightfitness, r/crossfit and the
     secondary list.
   - **Filter every signal through the app lane.** A thread about protein
     timing is real pain and a bad post for this blog. A thread about a timer
     that stopped mid-workout, a Watch app that drained the battery, or not
     being able to set up a 40/20 ladder quickly is the same pain in the lane
     Google indexes for us. **Product-friction threads are the strongest signal
     available** — they sit exactly where a search query meets a reason to
     install the app. Prioritise them, and discard on-topic-but-generic threads
     however well they perform socially.
   - xpoz `getTiktokPostsByUser` over fitness creators for phrasing and hooks.
     Find creators with `searchTiktokUsers` by name; never by hashtag or
     keyword, which returns unrelated results.
3. **Read what search already says about our own posts.** Two queries, both
   `dataState: "final"`, both with `siteUrl: "sc-domain:peakintervalapp.com"`:
   - Last 90 days, `dimensions: ["query"]`, `rowLimit: 500`. Pull out
     **striking-distance queries**: average position 8-40 with at least 2
     impressions. Google already associates us with these and we lose on the
     last stretch — worth more than a fresh topic from zero. **At least 2 of
     the themes must target one**, recorded in `searchEvidence`.
   - Last 28 days, `dimensions: ["page"]`, `rowLimit: 1000`. This is the most
     valuable read in the pipeline: the surviving 28 posts are the ones Google
     actually indexed, so the ones earning impressions show which app-lane
     angles work. Write more like the winners. Note any post 21+ days old with
     no row at all.
4. **Keyword research, for volume the pain signals never surface.**
   ```bash
   python3 Scripts/marketing/keyword_volume.py ideas --seeds "hiit" "interval timer" --min-volume 100
   python3 Scripts/marketing/keyword_volume.py ideas --urls https://peakintervalapp.com/blog/posts/<a-strong-post>/ --min-volume 100
   ```
   Vary seeds run to run — short head terms only (`hiit`, `tabata`,
   `interval timer`, `cardio`, `fat loss`, `treadmill`, `kettlebell`). **At
   least 2 themes must come from this list**, with the keyword and volume in
   `searchEvidence`. Judge intent: high volume with HIGH competition is usually
   commercial intent that ad budgets own, and fitness seeds drag in supplement
   and equipment queries a blog post cannot serve. `volume` mode must never
   reject a theme — it returns 0 for phrases that plainly have traffic.
5. Draft **7 themes**, each with: kebab-case `slug` matching search phrasing,
   `theme`, one-line `hook`, target `query`, one-line `evidence`, 2-3
   paraphrased `pain_quotes` (never verbatim user text), a `category` from the
   closed set above, and an `imagePrompt`.
6. **Gate each one before it enters the queue.** Run `check` on every candidate
   and follow the rules above. Candidates must be distinct from each other, not
   just from what exists. No more than **2 themes per category** in a batch of
   7 — the corpus is already 23 posts deep in Workout Guides.
7. Append the survivors, then run `audit` and confirm no BLOCK rows.
8. Commit + push `main`. Report the themes in one short paragraph, say which
   candidates you rejected and what they collided with, and give the search
   summary (see Report).

## Mode: publish (daily — blog only)

Take the FIRST theme off the queue. If the queue is empty, do a 10-minute
mini-research (step 2 above) to pick one theme, then proceed — and note the
empty queue in the report.

**Gate it before writing a word**, since a theme queued days ago can be
overtaken by a post published since:

```bash
python3 Scripts/marketing/topic_overlap.py check "<slug>" "<theme> <hook> <query>"
```

- Non-zero exit: do **not** publish it. Move the theme to `retired` with the
  colliding slug as the reason, take the next theme, and gate that one too.
- 0.18+: open the closest published post and read it. Either write the
  `distinctFrom` sentence and make the post genuinely answer that different
  question, or retire the theme and move on.

If you retire every remaining theme, publish nothing and say so in the report
and the iMessage. A skipped day is cheaper than a duplicate post.

### Write the post

Create `blog/posts/<slug>.md`. Front matter must carry every field or the post
breaks the index and category pages:

```yaml
---
title: "Title In Title Case"
description: "~155 chars, the search-result snippet. Mentions Peak Interval naturally where it fits."
date: "YYYY-MM-DD"
featured_image: "/assets/blog/<filename>.png"
image_alt: "Describes what the generated image actually shows"
layout: "post.liquid"
tags: "posts"
category: "<one of the closed set>"
---
```

Generate the cover first, so `featured_image` points at something real:

```bash
python3 Scripts/marketing/generate_blog_image.py "<imagePrompt from the queue>" "<slug>.png"
```

It prints the exact `featured_image:` line to paste. If it reports no API key,
**publish nothing and say so in the report and the iMessage** — a post without
a cover breaks every existing layout, and silently shipping one is worse than
skipping a day.

Body style, matched to the surviving posts: open with two short paragraphs that
name the reader's actual situation, then 3-5 `##` sections of 2-3 short
paragraphs each, second person, concrete numbers over adjectives. Mention Peak
Interval's mechanics (interval setup, Apple Watch flow, rest/prep phases, audio
cues) only where they genuinely answer the question — the existing posts that
rank are the ones that help first and sell second. Close with a short practical
takeaway, not a hard pitch.

Verify `npm run build 2>&1 | tail -5` succeeds and the post appears in `_site`.
Commit + push `main` (house workflow, no PRs). Remove the theme from the queue
and commit.

### Tell Bing immediately (after the push)

ChatGPT's search grounds on Bing's index, so a post Bing has not crawled is
invisible to that assistant however well it ranks on Google.

```bash
python3 Scripts/marketing/indexnow_ping.py https://peakintervalapp.com/blog/posts/<slug>/
```

The script waits for the Vercel deploy to serve the URL before submitting —
pointing a crawler at a 404 is worse than being found a day later by the
sitemap — so expect it to take a couple of minutes. `HTTP 200` or `202` is
success. If it reports the key file unreachable, the deploy has not landed or
`bc78c3ae8d93a7d9bcb54ddaa9c837bd.txt` fell out of the Eleventy passthrough in
`.eleventy.js`; say so in the report rather than retrying blindly.

### Index check (after the push, before the notify)

Cheap regression test on the one thing that would silently kill every post at
once. Do **not** inspect the post you just shipped; Google has not seen it yet.
Inspect the post published **3 days ago**:

```
inspect_search_console_url  https://peakintervalapp.com/blog/posts/<slug-from-3-days-ago>/
  with siteUrl: "sc-domain:peakintervalapp.com"
```

`indexStatusResult.verdict` should be `PASS`. Anything else — `NEUTRAL`,
"Discovered - currently not indexed", "Crawled - currently not indexed" — means
new posts are not reaching the index. Say so in the report **and the iMessage**.
One post lagging is normal variance; two consecutive days failing is a real
breakage worth stopping for.

### Notify (after the push succeeds)

All iMessage sends go through the QSNotify shim app, which permanently holds
the Automation + Full Disk Access grants (direct osascript/imsg calls break
every time a claude CLI or homebrew update replaces the calling binary — do not
use them):

```bash
printf 'send|New Peak Interval blog post is live: https://peakintervalapp.com/blog/posts/<slug>/' > /Users/djordjejankovicmacmini/QuestSpark/logs/qsnotify.cmd
open -W -a /Users/djordjejankovicmacmini/Applications/QSNotify.app
tail -1 /Users/djordjejankovicmacmini/QuestSpark/logs/qsnotify.log
```

The shim lives in the QuestSpark repo and is shared by both pipelines — that
path is correct, not a copy-paste error. The tail line is the delivery
verification: success looks like `... send ok | <chat.db timestamp> sent=1
err=0`. If it reports `send FAILED` or `chat.db unreadable`, say so in the run
report — do not fall back to raw osascript or imsg.

If any phase of any mode failed, still send an iMessage saying which phase
failed and what state was left, so a silent broken run never goes unnoticed.

### Report

Short plain-prose summary: theme + evidence line, blog slug, the closest
existing post and why this one is different, anything retired as a duplicate,
and queue depth remaining. If any phase failed, say which and what state was
left.

Publish runs add one line for the index check: the post inspected and its
verdict. Research runs add a short search-performance paragraph — impressions
and clicks for the last 28 days against the 28 before, which striking-distance
queries were found and which themes were aimed at them, which existing posts
are actually earning impressions, and which themes came from keyword research
with the volume behind them. Say plainly how the 7 split across the three
sources (pain signals, striking distance, keyword volume). If the Search
Console sample was too thin to steer on, say that instead of inventing a trend.
