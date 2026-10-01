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
        self.robots = []
        self.descriptions = []
        self.title = ""
        self.in_title = False
        self.is_redirect = False
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonical = attrs.get("href")
            if attrs.get("hreflang"):
                self.alternates[attrs["hreflang"]] = attrs.get("href")
        if tag == "meta" and attrs.get("property") == "og:locale":
            self.locale = attrs.get("content")
        if tag == "meta" and attrs.get("name") == "robots":
            self.robots.append(attrs.get("content", ""))
        if tag == "meta" and attrs.get("name") == "description":
            self.descriptions.append(attrs.get("content", ""))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.is_redirect = True

    def handle_data(self, data):
        if self.in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False


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


def check(root, previous=None, allow_summary_changes=False, environment="production"):
    require(root.is_dir(), f"Missing output directory: {root}")
    html_files = list(root.rglob("*.html"))
    require(html_files, "No generated HTML")
    xml_files = list(root.rglob("*.xml"))
    require(xml_files, "No generated XML")
    for path in xml_files:
        ET.parse(path)
    production = environment == "production"
    excluded = {prefix + name + "/index.html"
                for prefix in ["", "en/"]
                for name in ["search", "tags", "categories", "privacy-loadmap",
                             "privacy-mangiamo", "privacy-walletmanager"]}
    metadata = {p.relative_to(root).as_posix(): PageMetadata(p) for p in html_files}
    for relative in excluded:
        require(relative in metadata, f"Missing utility page: {relative}")
    for relative, page in metadata.items():
        # Alias redirects can carry a canonical, but have no regular page head.
        if not page.canonical or page.is_redirect:
            continue
        expected = ("noindex, follow" if relative in excluded else "index, follow") if production else "noindex, nofollow"
        require(page.robots == [expected], f"Wrong or duplicate robots meta: {relative}: {page.robots}")
        if relative not in excluded and not relative.endswith("404.html"):
            require(page.title.strip(), f"Missing title: {relative}")
            require(len(page.descriptions) == 1 and page.descriptions[0].strip(),
                    f"Missing or duplicate description: {relative}")
    for relative, title in [("index.html", "Claudio Bosticco | Responsabile sviluppo software .NET"),
                            ("en/index.html", "Claudio Bosticco | Software Development Manager .NET")]:
        require(metadata[relative].title == title, f"Incorrect homepage SEO title: {relative}")
    ns = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    sitemap_index = ET.parse(root / "sitemap.xml").getroot()
    require(sitemap_index.tag == "{" + ns["s"] + "}sitemapindex", "Missing multilingual sitemap index")
    sitemap_urls = {node.text for node in sitemap_index.findall("s:sitemap/s:loc", ns)}
    base_url = metadata["index.html"].canonical
    require(sitemap_urls == {base_url + "it/sitemap.xml", base_url + "en/sitemap.xml"},
            "Wrong language sitemap URLs")
    indexed_urls = set()
    for lang in ["it", "en"]:
        sitemap = ET.parse(root / lang / "sitemap.xml").getroot()
        indexed_urls.update(node.text for node in sitemap.findall("s:url/s:loc", ns))
        for url in sitemap.findall("s:url", ns):
            require((url.findtext("s:lastmod", namespaces=ns) or "").strip(),
                    f"Missing sitemap lastmod: {url.findtext('s:loc', namespaces=ns)}")
    for relative, page in metadata.items():
        if not page.canonical or page.is_redirect or relative.endswith("404.html"):
            continue
        require((page.canonical in indexed_urls) == (relative not in excluded),
                f"Sitemap inclusion does not match indexing policy: {relative}")
    robots = (root / "robots.txt").read_text(encoding="utf-8").splitlines()
    require("User-agent: *" in robots, "Missing robots user agent")
    require("Sitemap: " + base_url + "sitemap.xml" in robots, "Missing sitemap in robots.txt")
    require(("Disallow: /" in robots) == (not production), "Wrong robots.txt environment policy")
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
            require(not production or page.locale == {"it": "it_it", "en": "en_us"}[lang],
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
        require(allow_summary_changes or not changed, f"Changed RSS summaries: {changed}")
        for relative, page in metadata.items():
            baseline = PageMetadata(previous / relative)
            require(page.canonical == baseline.canonical, f"Changed canonical: {relative}")
            require(page.alternates == baseline.alternates, f"Changed hreflang: {relative}")
        print(f"Routes, canonical and hreflang match the baseline; {len(changed)} RSS summaries changed.")
    print(f"Site checks passed: {len(html_files)} HTML pages, {len(xml_files)} XML files, 2 search indexes.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--compare", type=Path, help="Previous build: compare routes and RSS summaries")
    parser.add_argument("--allow-summary-changes", action="store_true", help="Allow intentional RSS description edits during comparison")
    parser.add_argument("--environment", choices=["production", "development"], default="production")
    args = parser.parse_args()
    check(args.output, args.compare, args.allow_summary_changes, args.environment)
