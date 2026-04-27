import hashlib
from datetime import datetime
from email.utils import parsedate_to_datetime

import requests
import xml.etree.ElementTree as ET

from shared.utils import get_logger
from .models import Article

logger = get_logger(__name__)

TRAVEL_RSS_FEEDS = {
    "Lonely Planet":        "https://www.lonelyplanet.com/news/feed",
    "National Geographic":  "https://www.nationalgeographic.com/travel/rss",
    "BBC Travel":           "https://feeds.bbci.co.uk/travel/rss.xml",
    "Atlas Obscura":        "https://www.atlasobscura.com/feeds/latest",
    "Condé Nast Traveler":  "https://www.cntraveler.com/feed/rss",
    "Travel + Leisure":     "https://www.travelandleisure.com/rss",
}


class RSSCollector:
    def fetch(self, limit_per_feed: int = 5) -> list[Article]:
        articles: list[Article] = []
        for name, url in TRAVEL_RSS_FEEDS.items():
            try:
                fetched = self._fetch_feed(name, url, limit_per_feed)
                articles.extend(fetched)
                logger.info("RSS [%s] 수집 완료: %d건", name, len(fetched))
            except Exception as e:
                logger.warning("RSS [%s] 수집 실패: %s", name, e)
        return articles

    def _fetch_feed(self, source_name: str, url: str, limit: int) -> list[Article]:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "TubeFlow/1.0"})
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        items = root.findall(".//item") or root.findall(".//atom:entry", ns)
        articles = []
        for item in items[:limit]:
            article = self._parse_item(item, source_name, ns)
            if article:
                articles.append(article)
        return articles

    def _parse_item(self, item, source_name: str, ns: dict) -> Article | None:
        title = self._text(item, ["title", "atom:title"], ns)
        url = self._text(item, ["link", "atom:link"], ns) or ""
        description = self._text(item, ["description", "atom:summary", "atom:content"], ns) or ""
        pub_str = self._text(item, ["pubDate", "atom:published", "atom:updated"], ns) or ""

        if not title or not url:
            return None

        try:
            published_at = parsedate_to_datetime(pub_str) if pub_str else datetime.utcnow()
        except Exception:
            published_at = datetime.utcnow()

        return Article(
            id=hashlib.md5(url.encode()).hexdigest(),
            title=title,
            body=description[:500],
            source="rss",
            source_name=source_name,
            url=url,
            published_at=published_at,
        )

    def _text(self, element, tags: list[str], ns: dict) -> str:
        for tag in tags:
            el = element.find(tag, ns) if ":" in tag else element.find(tag)
            if el is not None:
                if tag == "atom:link":
                    return el.get("href", "") or (el.text or "")
                return (el.text or "").strip()
        return ""
