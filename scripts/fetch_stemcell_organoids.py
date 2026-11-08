#!/usr/bin/env python3
"""Fetch the organoid pages of the STEMCELL Technologies website.

The pages have no API or data download, so this script crawls them. It
starts from the Organoid Research hub page and the organoid product list,
and follows links on www.stemcell.com whose paths name an organoid, an organ,
or an organoid product line (IntestiCult, HepatiCult, PneumaCult, STEMdiff,
and so on). Pages in other languages, account pages, search results and
media files are skipped, and so is any URL the site's robots.txt disallows;
a Crawl-delay there, if longer than --pause, is used instead.

Writes, into the output directory:

- ``html/``: each page as fetched, named by a hash of its URL.
- ``text/``: each page as plain text, named after its canonical URL, with
  the URL on the first line. Pages with the same canonical URL are written
  once.
- ``manifest.json``: the fetch time, and for each URL fetched its file, its
  canonical URL and title, or the error; the URLs skipped because
  robots.txt disallows them; and the links still queued when the page limit
  was reached.

Requests are made one at a time with a pause between them. The 2026-11-06
run read 400 pages from the crawl and about 30 more queued organoid pages,
412 unique pages in all.

    uv run python scripts/fetch_stemcell_organoids.py
    uv run python scripts/fetch_stemcell_organoids.py --max-pages 600 --pause 1.5
"""

import argparse
import datetime
import hashlib
import html.parser
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from pathlib import Path

SITE = "www.stemcell.com"
SEEDS = [
    "https://www.stemcell.com/technical-resources/area-of-interest/organoid-research.html",
    "https://www.stemcell.com/product-portfolios/organoids/view-all.html",
]
USER_AGENT = "nams-registry (https://github.com/monarch-initiative/nams-registry)"

# A link is followed when its path matches FOLLOW and not SKIP.
FOLLOW = re.compile(
    r"organoid|assembloid|intesticult|hepaticult|pneumacult|mammocult|pancreacult"
    r"|gynecult|stemdiff|kidney|cerebral|choroid|retina|tumor|colon|gastric|lung"
    r"|airway|alveol|pulmonary|hepatic|liver|intestin|mammary|prostat|pancrea"
    r"|endometr|vascul",
    re.I,
)
SKIP = re.compile(
    r"\.(pdf|jpe?g|png|gif|svg|zip|mp4)$|/customer/|/checkout/|/wishlist|/catalogsearch"
    r"|/forms/|/media/|/static/|/(fr|de|jp|cn|kr|es|it)/",
    re.I,
)
DROP_TAGS = {"script", "style", "noscript", "nav", "header", "footer", "svg"}
BOILERPLATE = re.compile(
    r"cookies are disabled|^Copyright ©|^Privacy$|Cookie Preferences|Terms & Conditions"
    r"|Current Country|^Loading|^Load More|^Learn More|^Home$",
    re.I,
)


class TextExtractor(html.parser.HTMLParser):
    """Collect the visible text of a page, one block element per line."""

    def __init__(self):
        super().__init__()
        self.parts = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in DROP_TAGS:
            self.skip += 1
        if tag in {"p", "br", "li", "h1", "h2", "h3", "h4", "h5", "tr", "div", "section"}:
            self.parts.append("\n")
        if tag in {"h1", "h2", "h3", "h4"}:
            self.parts.append("#" * int(tag[1]) + " ")
        if tag == "li":
            self.parts.append("- ")

    def handle_endtag(self, tag):
        if tag in DROP_TAGS:
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data):
        if not self.skip:
            self.parts.append(data)


def to_text(page):
    parser = TextExtractor()
    parser.feed(page)
    text = re.sub(r"[ \t\xa0]+", " ", "".join(parser.parts))
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(
        line for line in lines if len(line) > 3 and line != "-" and not BOILERPLATE.search(line)
    )


def links(base, page):
    for href in re.findall(r'href="([^"]+)"', page):
        url = urllib.parse.urljoin(base, href).split("#")[0]
        url = re.sub(r"(?<!:)//+", "/", url)
        parsed = urllib.parse.urlparse(url)
        if parsed.netloc != SITE or parsed.query or SKIP.search(url):
            continue
        if FOLLOW.search(parsed.path):
            yield url


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", "ignore")


def robots():
    """Read the site's robots.txt, fetched with this script's user agent."""
    parser = urllib.robotparser.RobotFileParser()
    parser.parse(fetch(f"https://{SITE}/robots.txt").splitlines())
    return parser


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--output", type=Path, default=Path("tmp/stemcell_organoids"))
    parser.add_argument("--max-pages", type=int, default=600)
    parser.add_argument("--pause", type=float, default=1.0, help="seconds between requests")
    args = parser.parse_args()

    html_dir, text_dir = args.output / "html", args.output / "text"
    html_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    rules = robots()
    pause = max(args.pause, rules.crawl_delay(USER_AGENT) or 0)
    queue, seen, pages, canonical_seen, disallowed = list(SEEDS), set(), {}, set(), []
    while queue and len(seen) < args.max_pages:
        url = queue.pop(0)
        if url in seen:
            continue
        seen.add(url)
        if not rules.can_fetch(USER_AGENT, url):
            disallowed.append(url)
            continue
        try:
            page = fetch(url)
        except (urllib.error.URLError, TimeoutError) as err:
            pages[url] = {"error": str(err)}
            time.sleep(pause)
            continue
        name = hashlib.md5(url.encode()).hexdigest()[:12] + ".html"
        (html_dir / name).write_text(page)
        match = re.search(r'<link rel="canonical" href="([^"]+)"', page)
        canonical = match.group(1) if match else url
        title = re.search(r"<title>(.*?)</title>", page, re.S)
        pages[url] = {
            "file": name,
            "canonical": canonical,
            "title": title.group(1).strip() if title else "",
        }
        if canonical not in canonical_seen:
            canonical_seen.add(canonical)
            stem = canonical.replace(f"https://{SITE}/", "").removesuffix(".html").lower()
            stem = re.sub(r"[^a-z0-9]+", "_", stem).strip("_")[:150]
            (text_dir / f"{stem}.txt").write_text(f"URL: {canonical}\n{to_text(page)}\n")
        for link in links(url, page):
            if link not in seen and link not in queue:
                queue.append(link)
        print(f"{len(seen)}\t{url}", file=sys.stderr)
        time.sleep(pause)

    manifest = {
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "seeds": SEEDS,
        "pages_fetched": len(seen),
        "unique_pages": len(canonical_seen),
        "pages": pages,
        "disallowed_by_robots_txt": disallowed,
        "queued_not_fetched": queue,
    }
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=1))
    print(f"{len(seen)} fetched, {len(canonical_seen)} unique, {len(queue)} left in queue")


if __name__ == "__main__":
    main()
