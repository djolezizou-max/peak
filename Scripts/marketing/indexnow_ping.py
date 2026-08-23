#!/usr/bin/env python3
"""Tell Bing (and other IndexNow engines) about a URL the moment it ships.

Bing coverage matters beyond Bing's own traffic because ChatGPT's search
grounds on Bing's index, so a post Bing has not crawled is invisible to that
assistant however well it ranks on Google. Waiting for a sitemap re-crawl is
the slow path; IndexNow is a push.

Usage:
    python3 Scripts/marketing/indexnow_ping.py <url> [<url> ...]
    python3 Scripts/marketing/indexnow_ping.py --check      # verify the key file only

The key lives in two places that must agree, or every ping is rejected:
the KEY constant here, and <key>.txt in the repo root, passed through by
.eleventy.js and served at https://peakintervalapp.com/<key>.txt. To rotate,
change all three.

This pings AFTER the deploy is live, not at push time: a URL that 404s when
the crawler arrives is worse than one it finds a day later via the sitemap,
so each URL is polled until it returns 200 before being submitted.
"""
import argparse
import json
import sys
import time
import urllib.error
import urllib.request

KEY = "bc78c3ae8d93a7d9bcb54ddaa9c837bd"
HOST = "peakintervalapp.com"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/IndexNow"

# A Vercel deploy of this Eleventy site takes well under a minute; 10 tries
# at 15s covers a slow one without hanging the publish run for long.
LIVE_TRIES = 10
LIVE_DELAY = 15


def http_status(url, timeout=10):
    request = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "questspark-indexnow/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status
    except urllib.error.HTTPError as error:
        return error.code
    except Exception as error:  # DNS, TLS, timeout
        print(f"  ! {url}: {type(error).__name__}: {error}", file=sys.stderr)
        return None


def check_key_file():
    """The key file must be live and match, or IndexNow rejects everything."""
    try:
        with urllib.request.urlopen(KEY_LOCATION, timeout=10) as response:
            body = response.read().decode("utf-8").strip()
    except Exception as error:
        print(f"FAIL: {KEY_LOCATION} is not reachable ({type(error).__name__}: {error}).")
        print("The key file ships from the repo root via .eleventy.js passthrough — has the site deployed since it was added?")
        return False
    if body != KEY:
        print(f"FAIL: {KEY_LOCATION} serves {body!r} but this script uses {KEY!r}.")
        return False
    print(f"OK: {KEY_LOCATION} serves the matching key.")
    return True


def wait_until_live(url):
    for attempt in range(1, LIVE_TRIES + 1):
        status = http_status(url)
        if status == 200:
            return True
        print(f"  {url} -> {status} (attempt {attempt}/{LIVE_TRIES})", file=sys.stderr)
        if attempt < LIVE_TRIES:
            time.sleep(LIVE_DELAY)
    return False


def submit(urls):
    payload = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }).encode("utf-8")
    request = urllib.request.Request(
        ENDPOINT,
        data=payload,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            # 200 accepted, 202 accepted but key validation pending.
            print(f"IndexNow accepted {len(urls)} URL(s): HTTP {response.status}")
            return True
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")[:300]
        # 422 is the one worth calling out: it means the URLs do not match the
        # host, or the key file does not validate.
        print(f"IndexNow rejected the submission: HTTP {error.code} {detail}", file=sys.stderr)
        return False
    except Exception as error:
        print(f"IndexNow request failed: {type(error).__name__}: {error}", file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("urls", nargs="*", help="full URLs to submit")
    parser.add_argument("--check", action="store_true", help="verify the key file and exit")
    parser.add_argument("--no-wait", action="store_true", help="skip the live check (use only for already-live URLs)")
    args = parser.parse_args()

    if args.check:
        sys.exit(0 if check_key_file() else 1)
    if not args.urls:
        parser.error("give at least one URL, or --check")

    bad_host = [u for u in args.urls if f"//{HOST}/" not in u]
    if bad_host:
        sys.exit(f"These URLs are not on {HOST}, which IndexNow rejects: {bad_host}")

    if not check_key_file():
        sys.exit(1)

    live = args.urls
    if not args.no_wait:
        live = []
        for url in args.urls:
            if wait_until_live(url):
                live.append(url)
            else:
                print(f"SKIPPING {url}: never returned 200, so submitting it would point Bing at a 404.")
        if not live:
            sys.exit("No URLs were live; nothing submitted.")

    sys.exit(0 if submit(live) else 1)


if __name__ == "__main__":
    main()
