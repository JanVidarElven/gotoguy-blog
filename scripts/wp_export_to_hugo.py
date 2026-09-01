#!/usr/bin/env python3
"""Convert a WordPress XML export (WXR) into Hugo markdown content files."""

from __future__ import annotations

import argparse
import html
import os
import re
import sys
import xml.etree.ElementTree as ET
import zipfile
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
    parser.add_argument(
        "--media-zip",
        default=None,
        help="Optional WordPress media archive (.zip) to extract into static/uploads/.",
    )
    parser.add_argument(
        "--media-output",
        default="static/uploads",
        help="Directory to receive extracted media files (default: static/uploads).",
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
    if to_markdown is not None:
        markdown = to_markdown(
            normalized,
            heading_style="ATX",
            bullets="-",
            strip=["span", "div"],
        )
        markdown = markdown.strip()
        if markdown:
            return annotate_fenced_code_languages(wrap_code_blocks(markdown))

    # Fallback conversion for environments without markdownify installed.
    text = normalized
    text = re.sub(r"(?is)<br\s*/?>", "\n", text)
    text = re.sub(r"(?is)<(/?)h([1-6])\b([^>]*)>", lambda m: f"\n\n{'#' * int(m.group(2))} ", text)
    text = re.sub(r"(?is)<p\b[^>]*>", "\n\n", text)
    text = re.sub(r"(?is)</p>", "\n\n", text)
    text = re.sub(r"(?is)<li\b[^>]*>", "\n- ", text)
    text = re.sub(r"(?is)</li>", "\n", text)
    text = re.sub(r"(?is)<ol\b[^>]*>|<ul\b[^>]*>", "\n", text)
    text = re.sub(r"(?is)</ol>|</ul>", "\n", text)
    text = re.sub(r"(?is)<pre\b[^>]*>(.*?)</pre>", lambda m: f"\n\n```\n{html.unescape(strip_html(m.group(1))).strip()}\n```\n\n", text, flags=re.DOTALL)
    text = re.sub(r"(?is)<code\b[^>]*>(.*?)</code>", lambda m: f"`{html.unescape(strip_html(m.group(1))).strip()}`", text, flags=re.DOTALL)
    text = re.sub(r"(?is)<a\s+[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", lambda m: f"[{strip_html(m.group(2)).strip()}]({m.group(1)})", text)
    text = re.sub(r"(?is)<img\s+[^>]*src=[\"']([^\"']+)[\"'][^>]*?(?:alt=[\"']([^\"']*)[\"'])?[^>]*>", lambda m: f"![{m.group(2) or 'image'}]({rewrite_media_urls(m.group(1))})", text)
    text = re.sub(r"(?is)<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"\\_", "_", text)
    text = wrap_code_blocks(text)
    text = annotate_fenced_code_languages(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def wrap_code_blocks(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    buffer: list[str] = []
    blank_lines = 0
    in_fence = False

    def codeish(line: str) -> bool:
        stripped = line.strip()
        if not stripped:
            return False
        if re.match(r"^#{2,6}\s", stripped):
            return False
        if stripped.startswith("http://") or stripped.startswith("https://"):
            return False
        if stripped.startswith("!") or stripped.startswith("["):
            return False
        if stripped.startswith("@{"):
            return True
        if stripped.startswith("#") or stripped.startswith("$"):
            return True
        if re.match(
            r"^(?:Add|Get|Set|New|Remove|Import|Export|Start|Stop|Register|ForEach|Where|Write|Test|Select|Convert|Invoke|Connect|Install|Enable|Disable|Show|Disconnect)-[A-Za-z0-9_.-]+",
            stripped,
        ):
            return True
        if re.match(r"^[A-Za-z0-9_.-]+\s*=\s*.*", stripped):
            return True
        return False

    def normalize_code_line(line: str) -> str:
        return line.replace(r"\_", "_")

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("```"):
            if buffer:
                output.append("```powershell")
                output.extend(buffer)
                output.append("```")
                buffer = []
                blank_lines = 0
            in_fence = not in_fence
            output.append(line)
            continue

        if in_fence:
            output.append(line)
            continue

        if not stripped:
            if buffer:
                blank_lines += 1
                continue
            output.append("")
            continue

        if codeish(stripped):
            if not buffer:
                buffer = []
            if blank_lines:
                buffer.extend([""] * blank_lines)
                blank_lines = 0
            buffer.append(normalize_code_line(stripped))
            continue

        if buffer:
            output.append("```powershell")
            output.extend(buffer)
            output.append("```")
            buffer = []
            blank_lines = 0

        output.append(line)

    if buffer:
        output.append("```powershell")
        output.extend(buffer)
        output.append("```")

    return "\n".join(output)


def infer_code_language(code_lines: list[str]) -> str:
    snippet = "\n".join(code_lines).strip()
    lowered = snippet.lower()
    non_empty_lines = [line.strip() for line in code_lines if line.strip()]
    if not snippet:
        return ""
    if snippet.startswith("{") or snippet.startswith("["):
        if re.search(r'"\w+"\s*:', snippet):
            return "json"
    if re.search(r'(^|\n)\s*"\w[^"]*"\s*:\s*[\{\["0-9tfn-]', snippet):
        return "json"
    if snippet.startswith("<!--"):
        return "html"
    if snippet.startswith("<") and re.search(r"</?[a-zA-Z][^>]*>", snippet):
        return "html"
    if re.search(
        r"(^|\n)\s*(const|let|var)\s+[A-Za-z_$][\w$]*\s*=|(^|\n)\s*function\s+[A-Za-z_$][\w$]*\s*\(|document\.getElementById\(",
        snippet,
        re.MULTILINE,
    ):
        return "javascript"
    if re.search(r"(^|\n)\s*(Set|ClearCollect|Collect|Patch|Reset|Navigate|UpdateContext|If)\(", snippet):
        return "powerfx"
    if re.search(
        r"(^|\n)\s*(split|replace|mod|length|if|equals|concat|json|base64ToString|contains|outputs|triggerBody)\(",
        lowered,
    ):
        return "text"
    if non_empty_lines and (
        non_empty_lines[0] == "---"
        or all(
            re.match(r"^[A-Za-z0-9_.-]+\s*:\s*.+$", line) for line in non_empty_lines[: min(len(non_empty_lines), 8)]
        )
    ):
        return "yaml"
    if non_empty_lines and re.match(
        r"^(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\s+\S+.*(?:\s+HTTP/\d\.\d)?$",
        non_empty_lines[0],
        re.IGNORECASE,
    ):
        return "http"
    if re.search(
        r"(^|\n)\s*(targetScope\s*=|param\s+\w+\s+\w+|resource\s+\w+\s+'[^']+'|provider\s+\w+|module\s+\w+)",
        snippet,
        re.MULTILINE,
    ):
        return "bicep"
    if re.search(
        r"(^|\n)\s*(let\s+\w+\s*=|datatable\s*\(|print\s+|[A-Za-z_][\w]*\s*\|\s*(where|project|extend|summarize|join|order by)\b)",
        lowered,
        re.MULTILINE,
    ):
        return "kusto"
    if re.search(
        r"(^|\n)\s*(Add|Get|Set|New|Remove|Import|Export|Start|Stop|Register|ForEach|Where|Write|Test|Select|Convert|Invoke|Connect|Install|Enable|Disable|Show|Disconnect)-[A-Za-z0-9_.-]+",
        snippet,
        re.MULTILINE,
    ) or "$_" in snippet or re.search(r"(^|\n)\s*\$", snippet, re.MULTILINE) or snippet.startswith("@{"):
        return "powershell"
    if re.search(r"(^|\n)\s*(az|git|curl|wget|npm|npx|hugo)\s+", lowered, re.MULTILINE):
        return "bash"
    return ""


def annotate_fenced_code_languages(text: str) -> str:
    lines = text.splitlines()
    output: list[str] = []
    in_fence = False
    fence_line = ""
    code_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if not in_fence:
                in_fence = True
                fence_line = line
                code_lines = []
                continue
            fence_tag = fence_line.strip()[3:].strip()
            if fence_tag:
                open_fence = f"```{fence_tag}"
            else:
                language = infer_code_language(code_lines)
                open_fence = f"```{language}" if language else "```"
            output.append(open_fence)
            output.extend(code_lines)
            output.append("```")
            in_fence = False
            fence_line = ""
            code_lines = []
            continue
        if in_fence:
            code_lines.append(line)
            continue
        output.append(line)
    if in_fence:
        output.append(fence_line or "```")
        output.extend(code_lines)
    return "\n".join(output)


def strip_html(value: str) -> str:
    return re.sub(r"(?is)<[^>]+>", "", value)


def rewrite_media_urls(content: str) -> str:
    rewritten = content
    patterns = [
        (re.compile(r"https?://[^/]+/wp-content/uploads/", flags=re.IGNORECASE), "/uploads/"),
        (re.compile(r"(?:https?://[^/]+)?/wp-content/uploads/", flags=re.IGNORECASE), "/uploads/"),
        (re.compile(r"(?:https?://[^/]+)?wp-content/uploads/", flags=re.IGNORECASE), "/uploads/"),
    ]
    for pattern, replacement in patterns:
        rewritten = pattern.sub(replacement, rewritten)
    rewritten = re.sub(r":\[[^\]]+\]", "", rewritten)
    return rewritten


def extract_media_archive(zip_path: Path, output_root: Path) -> list[Path]:
    if not zip_path.exists():
        raise FileNotFoundError(f"Media archive not found: {zip_path}")

    output_root.mkdir(parents=True, exist_ok=True)
    extracted: list[Path] = []
    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            if name.endswith("/"):
                continue
            cleaned = name.replace('\\', '/')
            if cleaned.startswith("wp-content/uploads/"):
                cleaned = cleaned[len("wp-content/uploads/") :]
            elif cleaned.startswith("uploads/"):
                cleaned = cleaned[len("uploads/") :]
            if cleaned.startswith("/"):
                cleaned = cleaned.lstrip("/")
            if not cleaned or cleaned.startswith("../"):
                continue

            destination = output_root / cleaned
            destination.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(name) as src, destination.open("wb") as dst:
                dst.write(src.read())
            extracted.append(destination)

    return extracted


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

    if args.media_zip:
        media_zip = Path(args.media_zip)
        media_root = Path(args.media_output)
        try:
            extracted = extract_media_archive(media_zip, media_root)
            print(f"Extracted {len(extracted)} media files into {media_root}.")
        except FileNotFoundError:
            print(f"Media archive not found: {media_zip}", file=sys.stderr)
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
