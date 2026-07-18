#!/usr/bin/env python3
"""Convert a WordPress XML export (WXR) into Hugo markdown content files."""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Iterable

try:
    from markdownify import markdownify as to_markdown
except ImportError:  # pragma: no cover - optional dependency fallback
    to_markdown = None


NS = {
    "content": "http://purl.org/rss/1.0/modules/content/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
    "wp": "http://wordpress.org/export/1.2/",
}


@dataclass
class Post:
    post_id: str
    post_type: str
    status: str
    title: str
    slug: str
    date: datetime
    content: str
    tags: list[str]
    categories: list[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert WordPress export XML to Hugo markdown files."
    )
    parser.add_argument("--xml", required=True, help="Path to WordPress export XML file.")
    parser.add_argument(
        "--output", default="content", help="Hugo content directory (default: content)."
    )
    parser.add_argument(
        "--include-pages",
        action="store_true",
        help="Include WordPress pages in addition to posts.",
    )
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="Include draft/private/future content and mark as draft in front matter.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing markdown files.",
    )
    return parser.parse_args()


def get_text(element: ET.Element, path: str, default: str = "") -> str:
    found = element.find(path, NS)
    if found is None or found.text is None:
        return default
    return found.text.strip()


def parse_date(item: ET.Element) -> datetime:
    wp_date = get_text(item, "wp:post_date_gmt") or get_text(item, "wp:post_date")
    if wp_date and wp_date != "0000-00-00 00:00:00":
        date_value = datetime.strptime(wp_date, "%Y-%m-%d %H:%M:%S")
        return date_value.replace(tzinfo=timezone.utc)

    pub_date = get_text(item, "pubDate")
    if pub_date:
        parsed = parsedate_to_datetime(pub_date)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)

    return datetime.now(tz=timezone.utc)


def slugify(value: str) -> str:
    lowered = value.lower().strip()
    lowered = re.sub(r"[^\w\s-]", "", lowered)
    lowered = re.sub(r"[\s_]+", "-", lowered)
    lowered = re.sub(r"-+", "-", lowered).strip("-")
    return lowered or "untitled"


def normalize_slug(item: ET.Element, title: str) -> str:
    raw = get_text(item, "wp:post_name")
    if raw:
        return slugify(raw)
    return slugify(title)


def html_to_markdown(content: str) -> str:
    normalized = rewrite_media_urls(content)
    if to_markdown is None:
        stripped = re.sub(r"<br\s*/?>", "\n", normalized, flags=re.IGNORECASE)
        stripped = re.sub(r"</p\s*>", "\n\n", stripped, flags=re.IGNORECASE)
        stripped = re.sub(r"<[^>]+>", "", stripped)
        return html.unescape(stripped).strip()

    markdown = to_markdown(
        normalized,
        heading_style="ATX",
        bullets="-",
        strip=["span", "div"],
    )
    return markdown.strip()


def rewrite_media_urls(content: str) -> str:
    pattern = re.compile(
        r"https?://[^/]+/wp-content/uploads/",
        flags=re.IGNORECASE,
    )
    return pattern.sub("/uploads/", content).replace("/wp-content/uploads/", "/uploads/")


def collect_terms(item: ET.Element, domain: str) -> list[str]:
    terms: list[str] = []
    for category in item.findall("category"):
        if category.attrib.get("domain") != domain:
            continue
        if not category.text:
            continue
        value = category.text.strip()
        if value:
            terms.append(value)
    return sorted(set(terms))


def read_posts(
    xml_path: Path,
    include_pages: bool,
    include_drafts: bool,
) -> Iterable[Post]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    for item in root.findall("./channel/item"):
        post_type = get_text(item, "wp:post_type")
        if post_type not in {"post", "page"}:
            continue
        if post_type == "page" and not include_pages:
            continue

        status = get_text(item, "wp:status")
        if status != "publish" and not include_drafts:
            continue

        title = get_text(item, "title", "Untitled")
        content = get_text(item, "content:encoded")

        yield Post(
            post_id=get_text(item, "wp:post_id", "0"),
            post_type=post_type,
            status=status,
            title=title,
            slug=normalize_slug(item, title),
            date=parse_date(item),
            content=html_to_markdown(content),
            tags=collect_terms(item, "post_tag"),
            categories=collect_terms(item, "category"),
        )


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_front_matter(post: Post, include_drafts: bool) -> str:
    lines = [
        "---",
        f"title: {yaml_quote(post.title)}",
        f"date: {post.date.isoformat().replace('+00:00', 'Z')}",
        f'draft: {"true" if post.status != "publish" and include_drafts else "false"}',
        f"slug: {yaml_quote(post.slug)}",
    ]

    if post.tags:
        lines.append("tags:")
        lines.extend(f"  - {yaml_quote(tag)}" for tag in post.tags)
    if post.categories:
        lines.append("categories:")
        lines.extend(f"  - {yaml_quote(category)}" for category in post.categories)

    lines.append("---")
    return "\n".join(lines)


def target_file_path(output_root: Path, post: Post) -> Path:
    if post.post_type == "page":
        filename = "index.md" if post.slug == "index" else f"{post.slug}.md"
        return output_root / filename
    return output_root / "posts" / f"{post.slug}.md"


def write_post(
    post: Post,
    output_root: Path,
    include_drafts: bool,
    overwrite: bool,
    used_paths: set[Path],
) -> Path:
    candidate = target_file_path(output_root, post)
    if candidate in used_paths:
        candidate = candidate.with_name(f"{candidate.stem}-{post.post_id}{candidate.suffix}")

    used_paths.add(candidate)
    candidate.parent.mkdir(parents=True, exist_ok=True)

    if candidate.exists() and not overwrite:
        raise FileExistsError(
            f"Refusing to overwrite existing file: {candidate}. Use --overwrite to replace."
        )

    front_matter = render_front_matter(post, include_drafts)
    body = post.content.strip()
    content = f"{front_matter}\n\n{body}\n"
    candidate.write_text(content, encoding="utf-8")
    return candidate


def main() -> int:
    args = parse_args()

    xml_path = Path(args.xml)
    output_root = Path(args.output)
    if not xml_path.exists():
        print(f"WordPress export file not found: {xml_path}", file=sys.stderr)
        return 1

    posts = list(
        read_posts(
            xml_path=xml_path,
            include_pages=args.include_pages,
            include_drafts=args.include_drafts,
        )
    )
    if not posts:
        print("No matching posts/pages found in the XML export.", file=sys.stderr)
        return 1

    written: list[Path] = []
    used_paths: set[Path] = set()
    for post in posts:
        path = write_post(
            post=post,
            output_root=output_root,
            include_drafts=args.include_drafts,
            overwrite=args.overwrite,
            used_paths=used_paths,
        )
        written.append(path)

    print(
        "Converted "
        f"{len(written)} entries from {xml_path} into {output_root}. "
        "Copy your media files into static/uploads/."
    )
    for path in written[:10]:
        print(f" - {path.as_posix()}")
    if len(written) > 10:
        print(f" - ... and {len(written) - 10} more files")

    return os.EX_OK


if __name__ == "__main__":
    raise SystemExit(main())
