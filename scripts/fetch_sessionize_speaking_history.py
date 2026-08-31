#!/usr/bin/env python3
"""Fetch public Sessionize speaker sessions into a Hugo data file."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_PROFILE_URL = "https://sessionize.com/jan-vidar-elven/"
DEFAULT_OUTPUT = "data/sessionize/speaking_history.json"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a public Sessionize speaker profile into Hugo data."
    )
    parser.add_argument(
        "--profile-url",
        default=DEFAULT_PROFILE_URL,
        help="Public Sessionize speaker profile URL.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Path to output JSON data file.",
    )
    return parser.parse_args()


def fetch_html(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; gotoguy-blog-sessionize-fetcher/1.0)"
        },
    )
    with urlopen(request) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def clean_html_fragment(value: str) -> str:
    without_tags = re.sub(r"<[^>]+>", "", value)
    normalized = re.sub(r"\s+", " ", unescape(without_tags)).strip()
    return normalized


def parse_profile_name(html: str) -> str:
    match = re.search(r'<h1 class="c-s-speaker-info__name">(.*?)</h1>', html, re.S)
    if not match:
        return "Speaker"
    return clean_html_fragment(match.group(1))


def parse_sessions(html: str, profile_url: str) -> list[dict[str, str]]:
    session_pattern = re.compile(
        r'<div class="c-s-session">\s*'
        r'<h3 class="c-s-session__title">\s*'
        r'<a href="(?P<href>/s/[^"]+)">(?P<title>.*?)</a>.*?'
        r'<p class="c-s-session__summary">(?P<summary>.*?)</p>',
        re.S,
    )

    seen_urls: set[str] = set()
    sessions: list[dict[str, str]] = []
    for match in session_pattern.finditer(html):
        relative_url = clean_html_fragment(match.group("href"))
        title = clean_html_fragment(match.group("title"))
        summary = clean_html_fragment(match.group("summary"))
        url = f"https://sessionize.com{relative_url}"
        if not title or url in seen_urls:
            continue
        seen_urls.add(url)
        sessions.append(
            {
                "title": title,
                "url": url,
                "summary": summary,
            }
        )

    if not sessions:
        raise ValueError(f"No sessions found at {profile_url}")

    return sessions


def write_output(output_path: Path, payload: dict[str, object]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    args = parse_args()

    try:
        html = fetch_html(args.profile_url)
        payload = {
            "profile": {
                "name": parse_profile_name(html),
                "source_url": args.profile_url,
                "fetched_at": datetime.now(timezone.utc)
                .replace(microsecond=0)
                .isoformat()
                .replace("+00:00", "Z"),
            },
            "sessions": parse_sessions(html, args.profile_url),
        }
        write_output(Path(args.output), payload)
    except (HTTPError, URLError, ValueError) as exc:
        print(f"Failed to refresh Sessionize data: {exc}", file=sys.stderr)
        return 1

    print(
        f"Refreshed {len(payload['sessions'])} sessions from {args.profile_url} "
        f"into {args.output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

