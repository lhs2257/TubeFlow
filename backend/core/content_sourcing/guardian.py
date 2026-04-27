import hashlib
from datetime import datetime

import requests

from shared.config import get_settings
from shared.utils import get_logger
from .models import Article

logger = get_logger(__name__)
BASE_URL = "https://content.guardianapis.com/search"


class GuardianCollector:
    def __init__(self):
        self.api_key = get_settings().guardian_api_key

    def fetch(self, keywords: list[str], limit: int = 20) -> list[Article]:
        query = " OR ".join(keywords)
        params = {
            "q": query,
            "section": "travel",
            "show-fields": "bodyText,thumbnail",
            "page-size": min(limit, 50),
            "order-by": "newest",
            "api-key": self.api_key,
        }
        try:
            resp = requests.get(BASE_URL, params=params, timeout=10)
            resp.raise_for_status()
            results = resp.json().get("response", {}).get("results", [])
            articles = [self._to_article(r) for r in results]
            logger.info("Guardian 수집 완료: %d건", len(articles))
            return articles
        except Exception as e:
            logger.warning("Guardian 수집 실패: %s", e)
            return []

    def _to_article(self, raw: dict) -> Article:
        fields = raw.get("fields", {})
        return Article(
            id=hashlib.md5(raw["id"].encode()).hexdigest(),
            title=raw.get("webTitle", ""),
            body=fields.get("bodyText", "")[:500],
            source="guardian",
            source_name="The Guardian",
            url=raw.get("webUrl", ""),
            published_at=datetime.fromisoformat(raw["webPublicationDate"].replace("Z", "+00:00")),
            thumbnail=fields.get("thumbnail", ""),
        )
