import hashlib
from datetime import datetime

from shared.auth import get_youtube_data_client
from shared.utils import get_logger
from .models import Article

logger = get_logger(__name__)

REGION_CODES = {
    "전세계 (미국)": "US",
    "영국":          "GB",
    "일본":          "JP",
    "호주":          "AU",
    "캐나다":        "CA",
    "프랑스":        "FR",
    "독일":          "DE",
    "태국":          "TH",
}

TRAVEL_CATEGORY_ID = "19"  # YouTube 카테고리: 여행 & 이벤트


class YouTubeTrendCollector:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = get_youtube_data_client()
        return self._client

    def fetch(self, region_code: str = "US", limit: int = 20) -> list[Article]:
        try:
            resp = self.client.videos().list(
                part="snippet",
                chart="mostPopular",
                regionCode=region_code,
                videoCategoryId=TRAVEL_CATEGORY_ID,
                maxResults=min(limit, 50),
            ).execute()

            articles = [self._to_article(item, region_code) for item in resp.get("items", [])]
            logger.info("YouTube 트렌드 [%s] 수집 완료: %d건", region_code, len(articles))
            return articles
        except Exception as e:
            logger.warning("YouTube 트렌드 수집 실패 [%s]: %s", region_code, e)
            return []

    def fetch_multi_region(self, limit_per_region: int = 10) -> list[Article]:
        articles: list[Article] = []
        for name, code in REGION_CODES.items():
            fetched = self.fetch(region_code=code, limit=limit_per_region)
            logger.info("YouTube [%s] %d건", name, len(fetched))
            articles.extend(fetched)
        return articles

    def _to_article(self, item: dict, region_code: str) -> Article:
        snippet = item.get("snippet", {})
        video_id = item.get("id", "")
        published = snippet.get("publishedAt", "")
        try:
            published_at = datetime.fromisoformat(published.replace("Z", "+00:00"))
        except Exception:
            published_at = datetime.utcnow()

        return Article(
            id=hashlib.md5(video_id.encode()).hexdigest(),
            title=snippet.get("title", ""),
            body=snippet.get("description", "")[:500],
            source="youtube",
            source_name="YouTube Trends",
            url=f"https://www.youtube.com/watch?v={video_id}",
            published_at=published_at,
            country=region_code,
            thumbnail=snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
        )
