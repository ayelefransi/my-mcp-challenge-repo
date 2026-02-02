#!/usr/bin/env python3
"""Simple news headline scraper.

Usage:
  python news_scraper.py https://example.com -o headlines.csv -n 20

This script is intentionally generic: provide a URL and an optional CSS selector
to extract headline elements. Results are saved to CSV with columns
`title,url,source,fetched_at`.
"""
from __future__ import annotations

import argparse
import csv
import datetime
import time
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def fetch_html(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 10, retries: int = 2) -> str:
    """Fetch page HTML with simple retry/backoff.

    Raises the underlying exception on final failure.
    """
    session = requests.Session()
    headers = headers or {"User-Agent": "news-scraper/1.0 (+https://example.com)"}
    backoff = 1.0
    for attempt in range(retries + 1):
        try:
            resp = session.get(url, headers=headers, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception:
            if attempt == retries:
                raise
            time.sleep(backoff)
            backoff *= 2


def parse_headlines(html: str, base_url: str, selector: str = "h1,h2,h3 a, .headline a, .title a", limit: Optional[int] = None) -> List[Dict[str, str]]:
    """Return a list of headline dicts extracted from `html`.

    Each dict contains: `title`, `url`, `source`, `fetched_at`.
    """
    soup = BeautifulSoup(html, "html.parser")
    elements = soup.select(selector)
    seen = set()
    results: List[Dict[str, str]] = []
    now = datetime.datetime.utcnow().isoformat()

    for el in elements:
        title = el.get_text(strip=True)
        if not title:
            continue
        # avoid duplicates
        if title in seen:
            continue
        seen.add(title)

        link = ""
        if el.name == "a" and el.get("href"):
            link = urljoin(base_url, el["href"])
        else:
            a = el.find("a", href=True)
            if a:
                link = urljoin(base_url, a["href"])

        results.append({"title": title, "url": link, "source": base_url, "fetched_at": now})
        if limit is not None and len(results) >= limit:
            break

    return results


def save_to_csv(rows: List[Dict[str, str]], path: str) -> None:
    fieldnames = ["title", "url", "source", "fetched_at"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main() -> None:
    p = argparse.ArgumentParser(description="Scrape a page for news headlines and save to CSV")
    p.add_argument("url", help="Page URL to scrape")
    p.add_argument("-s", "--selector", default="h1,h2,h3 a, .headline a, .title a", help="CSS selector to find headline elements")
    p.add_argument("-o", "--output", default="headlines.csv", help="CSV output path")
    p.add_argument("-n", "--limit", type=int, default=50, help="Maximum number of headlines to save (0 for no limit)")
    p.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds")
    p.add_argument("--user-agent", default="news-scraper/1.0 (+https://example.com)", help="User-Agent header for requests")
    args = p.parse_args()

    limit = None if args.limit == 0 else args.limit
    headers = {"User-Agent": args.user_agent}

    try:
        html = fetch_html(args.url, headers=headers, timeout=args.timeout)
    except Exception as e:
        print(f"Failed to fetch {args.url}: {e}")
        raise SystemExit(1)

    rows = parse_headlines(html, args.url, selector=args.selector, limit=limit)
    if not rows:
        print("No headlines found with the given selector.")
    else:
        save_to_csv(rows, args.output)
        print(f"Saved {len(rows)} headlines to {args.output}")


if __name__ == "__main__":
    main()
