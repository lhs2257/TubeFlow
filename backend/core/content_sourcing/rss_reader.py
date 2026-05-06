import hashlib
from datetime import datetime
from email.utils import parsedate_to_datetime

import requests
import xml.etree.ElementTree as ET

from shared.utils import get_logger
from .models import Article

logger = get_logger(__name__)

# 카테고리별 RSS 피드 목록
# 소스 ID → (매체명, URL, 카테고리)
RSS_FEEDS: dict[str, tuple[str, str, str]] = {
    # ── 중국 이슈 ────────────────────────────────────────────────
    "scmp":         ("South China Morning Post", "https://www.scmp.com/rss/91/feed",                      "china"),
    "rfa":          ("Radio Free Asia",           "https://www.rfa.org/english/rss2.xml",                 "china"),
    # ── 일본 이슈 ────────────────────────────────────────────────
    "nhk":          ("NHK World",                 "https://www3.nhk.or.jp/rss/news/cat6.xml",             "japan"),
    "nikkei":       ("Nikkei Asia",               "https://asia.nikkei.com/rss/feed/nar",                 "japan"),
    # ── 동남아 이슈 ──────────────────────────────────────────────
    "cna":          ("Channel NewsAsia",          "https://www.channelnewsasia.com/api/v1/rss-outbound-feed?_format=xml&category=10416", "sea"),
    "diplomat":     ("The Diplomat",              "https://thediplomat.com/feed/",                        "sea"),
    # ── 국제/한국 시각 ───────────────────────────────────────────
    "koreaherald":  ("Korea Herald",              "https://www.koreaherald.com/rss/01.xml",               "korea"),
    "reuters_asia": ("Reuters Asia",              "https://feeds.reuters.com/reuters/asian-news",         "world"),
    "bbc_asia":     ("BBC News Asia",             "https://feeds.bbci.co.uk/news/world/asia/rss.xml",     "world"),
}


RSS_SOURCE_IDS: set[str] = set(RSS_FEEDS.keys())


class RSSCollector:
    def fetch(
        self,
        limit_per_feed: int = 5,
        feed_ids: list[str] | None = None,
    ) -> list[Article]:
        """
        feed_ids: 수집할 피드 ID 목록 (None 이면 전체 수집)
        """
        target = feed_ids if feed_ids else list(RSS_FEEDS.keys())
        articles: list[Article] = []
        for fid in target:
            if fid not in RSS_FEEDS:
                continue
            name, url, category = RSS_FEEDS[fid]
            try:
                fetched = self._fetch_feed(name, url, category, limit_per_feed)
                articles.extend(fetched)
                logger.info("RSS [%s] 수집 완료: %d건", name, len(fetched))
            except Exception as e:
                logger.warning("RSS [%s] 수집 실패: %s", name, e)
        return articles

    def _fetch_feed(self, source_name: str, url: str, category: str, limit: int) -> list[Article]:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "TubeFlow/1.0"})
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        items = root.findall(".//item") or root.findall(".//atom:entry", ns)
        articles = []
        for item in items[:limit]:
            article = self._parse_item(item, source_name, category, ns)
            if article:
                articles.append(article)
        return articles

    def _parse_item(self, item, source_name: str, category: str, ns: dict) -> Article | None:
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
            category=category,
        )

    def _text(self, element, tags: list[str], ns: dict) -> str:
        for tag in tags:
            el = element.find(tag, ns) if ":" in tag else element.find(tag)
            if el is not None:
                if tag == "atom:link":
                    return el.get("href", "") or (el.text or "")
                return (el.text or "").strip()
        return ""
