"""Smoke checks for Hugo output, using only the Python standard library."""

import argparse
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET


class PageMetadata(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.alternates = {}
        self.canonical = None
        self.locale = None
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonical = attrs.get("href")
            if attrs.get("hreflang"):
                self.alternates[attrs["hreflang"]] = attrs.get("href")
        if tag == "meta" and attrs.get("property") == "og:locale":
            self.locale = attrs.get("content")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def feed_summaries(root):
    return {
        item.findtext("link"): item.findtext("description")
        for path in root.rglob("*.xml")
        for item in ET.parse(path).getroot().findall("./channel/item")
        if item.findtext("link")
    }


def check(root, previous=None):
    require(root.is_dir(), f"Missing output directory: {root}")
    html_files = list(root.rglob("*.html"))
    require(html_files, "No generated HTML")
    xml_files = list(root.rglob("*.xml"))
    require(xml_files, "No generated XML")
    for path in xml_files:
        ET.parse(path)
    for lang, prefix in [("it", ""), ("en", "en/")]:
        for relative in ["index.xml", "sitemap.xml", "posts/index.xml"]:
            require((root / prefix / relative).is_file(), f"Missing {prefix}{relative}")
        index = json.loads((root / prefix / "index.json").read_text(encoding="utf-8"))
        require(isinstance(index, list) and index, f"Empty search index: {lang}")
        require(all(entry.get("title") and entry.get("permalink") for entry in index),
                f"Invalid search entries: {lang}")
    pairs = [
        ("index.html", "en/index.html"),
        ("chi-sono/index.html", "en/about/index.html"),
        ("contatti/index.html", "en/contact/index.html"),
        ("progetti/index.html", "en/projects/index.html"),
        ("progetti/framework-proprietario/index.html", "en/projects/framework-proprietario/index.html"),
        ("walletmanager/index.html", "en/walletmanager/index.html"),
    ]
    for italian, english in pairs:
        pages = [PageMetadata(root / italian), PageMetadata(root / english)]
        for page, lang, other in [(pages[0], "it", pages[1]), (pages[1], "en", pages[0])]:
            require(page.canonical, f"Missing canonical: {italian}/{english}")
            require(page.locale == {"it": "it_it", "en": "en_us"}[lang],
                    f"Incorrect Open Graph locale: {italian}/{english}")
            require(page.alternates.get(lang) == page.canonical,
                    f"Missing self hreflang: {italian}/{english}")
            require(page.alternates.get("en" if lang == "it" else "it") == other.canonical,
                    f"Missing reciprocal hreflang: {italian}/{english}")
    # These content files are deliberately drafts and must stay unpublished.
    for draft in ["progetti/logicway-rfid", "en/projects/logicway-rfid",
                  "posts/perche-un-framework-proprietario", "en/posts/why-a-proprietary-framework"]:
        require(not (root / draft / "index.html").exists(), f"Published draft: {draft}")
    for path in xml_files:
        for item in ET.parse(path).getroot().findall("./channel/item"):
            require(item.findtext("link"), f"Empty RSS item URL: {path}")
            require(not urlsplit(item.findtext("link", "")).path.rstrip("/").endswith("/search"),
                    f"Search page in RSS: {path}")
    if previous:
        for extension in ["*.html", "*.xml", "*.json"]:
            before = {p.relative_to(previous) for p in previous.rglob(extension)}
            after = {p.relative_to(root) for p in root.rglob(extension)}
            require(before == after, f"Changed routes ({extension}): {before ^ after}")
        old, new = feed_summaries(previous), feed_summaries(root)
        changed = [url for url in old.keys() & new.keys() if old[url] != new[url]]
        require(old.keys() == new.keys(), "Changed RSS item URLs")
        require(not changed, f"Changed RSS summaries: {changed}")
        print("Routes and RSS summaries match the baseline.")
    print(f"Site checks passed: {len(html_files)} HTML pages, {len(xml_files)} XML files, 2 search indexes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--compare", type=Path, help="Previous build: compare routes and RSS summaries")
    args = parser.parse_args()
    check(args.output, args.compare)
