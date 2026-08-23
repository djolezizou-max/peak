#!/usr/bin/env python3
"""Generate a featured image for a blog post, using Gemini.

Every one of the 118 existing posts has a `featured_image`, so a post shipped
without one breaks the visual consistency of the index page, the category
pages and every social/link preview. This is the automated replacement for
generate_blog_image.sh, which called OpenAI and depended on an OPENAI_API_KEY
that is not set anywhere on this machine.

Usage:
    python3 Scripts/marketing/generate_blog_image.py "<prompt>" <filename.png>
    python3 Scripts/marketing/generate_blog_image.py --check

Writes to assets/blog/<filename> and prints the path to put in front matter.

The key is read from GEMINI_API_KEY, or from Scripts/marketing/gemini.json
({"apiKey": "..."}), which is gitignored — launchd jobs do not inherit an
interactive shell's environment, so the file is the reliable path for the
scheduled publish run.

House style for these covers, inferred from the existing assets: photoreal
fitness photography, real people mid-effort, natural or gym lighting, no text
overlays, no logos, landscape. Prompts are wrapped with that so every post
does not need to restate it.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "assets/blog"
KEY_FILE = pathlib.Path(__file__).resolve().parent / "gemini.json"

MODEL = "gemini-2.5-flash-image"
ASPECT = "16:9"

# Wrapped around every prompt so covers stay consistent with the existing 118.
STYLE = (
    "Photorealistic fitness photography, landscape orientation. "
    "Natural lighting, authentic gym or outdoor setting, real athletic people mid-effort. "
    "No text, no words, no letters, no logos, no watermarks, no UI overlays. "
    "Editorial magazine quality, shallow depth of field. Subject: "
)


def resolve_key() -> str:
    from_env = os.environ.get("GEMINI_API_KEY")
    if from_env:
        return from_env
    if KEY_FILE.exists():
        key = json.loads(KEY_FILE.read_text()).get("apiKey")
        if key:
            return key
    sys.exit(
        f"No Gemini API key. Set GEMINI_API_KEY, or write {KEY_FILE} as "
        '{"apiKey": "..."}. Get one at https://aistudio.google.com/apikey.\n'
        "The scheduled publish run cannot generate cover images until this exists."
    )


def generate(prompt: str, filename: str) -> int:
    try:
        from google import genai
        from google.genai import types
    except ImportError:
        sys.exit("google-genai is not installed. Run: pip3 install google-genai Pillow")

    client = genai.Client(api_key=resolve_key())
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    destination = OUTPUT_DIR / filename

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=STYLE + prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=ASPECT),
            ),
        )
    except Exception as error:
        sys.exit(f"Gemini image generation failed: {type(error).__name__}: {error}")

    # The response carries the image as inline bytes on a part; a text-only
    # response means the model refused or the prompt tripped a safety filter,
    # which is worth reporting rather than writing a zero-byte file.
    for candidate in response.candidates or []:
        for part in candidate.content.parts or []:
            data = getattr(getattr(part, "inline_data", None), "data", None)
            if data:
                destination.write_bytes(data)
                print(f"Wrote {destination} ({len(data)} bytes)")
                print(f'featured_image: "/assets/blog/{filename}"')
                return 0

    text = " ".join(
        part.text for c in (response.candidates or []) for part in (c.content.parts or []) if getattr(part, "text", None)
    )
    sys.exit(f"Gemini returned no image. Model said: {text[:300] or '(nothing)'}")


def check() -> int:
    key = resolve_key()
    print(f"Gemini key found ({len(key)} chars), model {MODEL}, output {OUTPUT_DIR}.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prompt", nargs="?", help="what the image should show")
    parser.add_argument("filename", nargs="?", help="output filename, e.g. hiit-treadmill.png")
    parser.add_argument("--check", action="store_true", help="verify the key is available and exit")
    args = parser.parse_args()

    if args.check:
        return check()
    if not args.prompt or not args.filename:
        parser.error("give a prompt and a filename, or --check")
    return generate(args.prompt, args.filename)


if __name__ == "__main__":
    raise SystemExit(main())
