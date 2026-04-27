import hashlib
from datetime import datetime

import requests

from shared.config import get_settings
from shared.utils import get_logger
from .models import Article

logger = get_logger(__name__)
BASE_URL = "https://newsapi.org/v2/everything"


class NewsAPICollector:
    def __init__(self):
        self.api_key = get_settings().news_api_key

    def fetch(self, keywords: list[str], language: str = "en", limit: int = 20) -> list[Article]:
        query = " OR ".join(keywords)
        params = {
            "q": query,
            "language": language,
            "sortBy": "publishedAt",
            "pageSize": min(limit, 100),
            "apiKey": self.api_key,
        }
        try:
            resp = requests.get(BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            articles = resp.json().get("articles", [])
            result = [self._to_article(a) for a in articles if a.get("title") != "[Removed]"]
            logger.info("NewsAPI 수집 완료: %d건", len(result))
            return result
        except Exception as e:
            logger.warning("NewsAPI 수집 실패: %s", e)
            return []

    def _to_article(self, raw: dict) -> Article:
        source = raw.get("source", {})
        pub = raw.get("publishedAt", "")
        try:
            published_at = datetime.fromisoformat(pub.replace("Z", "+00:00"))
        except Exception:
            published_at = datetime.utcnow()

        uid = hashlib.md5((raw.get("url", "") + pub).encode()).hexdigest()
        return Article(
            id=uid,
            title=raw.get("title", ""),
            body=raw.get("description", "") or raw.get("content", "")[:500],
            source="newsapi",
            source_name=source.get("name", "NewsAPI"),
            url=raw.get("url", ""),
            published_at=published_at,
            thumbnail=raw.get("urlToImage", ""),
        )
