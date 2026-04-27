from datetime import datetime

from shared.auth import get_youtube_data_client
from shared.utils import get_logger
from .models import YouTubeTrendItem

logger = get_logger(__name__)

REGION_CODES = {
    "US": "미국",
    "GB": "영국",
    "JP": "일본",
    "AU": "호주",
    "CA": "캐나다",
    "FR": "프랑스",
    "DE": "독일",
    "TH": "태국",
    "KR": "한국",
}

TRAVEL_CATEGORY_ID = "19"


class YouTubeTrendAnalyzer:
    """
    YouTube Data API를 이용한 트렌드 분석기.
    M2의 YouTubeTrendCollector와 달리 조회수/좋아요/댓글 통계까지 수집합니다.
    """

    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = get_youtube_data_client()
        return self._client

    def fetch_region(
        self,
        region_code: str = "US",
        limit: int = 20,
        category_id: str = TRAVEL_CATEGORY_ID,
    ) -> list[YouTubeTrendItem]:
        try:
            resp = self.client.videos().list(
                part="snippet,statistics",
                chart="mostPopular",
                regionCode=region_code,
                videoCategoryId=category_id,
                maxResults=min(limit, 50),
            ).execute()

            items = [self._parse(item, region_code) for item in resp.get("items", [])]
            logger.info("YouTube 트렌드 분석 [%s] %d건", region_code, len(items))
            return items
        except Exception as e:
            logger.warning("YouTube 트렌드 분석 실패 [%s]: %s", region_code, e)
            return []

    def fetch_all_regions(self, limit_per_region: int = 10) -> list[YouTubeTrendItem]:
        results: list[YouTubeTrendItem] = []
        for code in REGION_CODES:
            results.extend(self.fetch_region(region_code=code, limit=limit_per_region))
        return results

    def _parse(self, item: dict, region_code: str) -> YouTubeTrendItem:
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        video_id = item.get("id", "")

        published_raw = snippet.get("publishedAt", "")
        try:
            published_at = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
        except Exception:
            published_at = datetime.utcnow()

        return YouTubeTrendItem(
            video_id=video_id,
            title=snippet.get("title", ""),
            channel=snippet.get("channelTitle", ""),
            region=region_code,
            view_count=int(stats.get("viewCount", 0)),
            like_count=int(stats.get("likeCount", 0)),
            comment_count=int(stats.get("commentCount", 0)),
            category_id=snippet.get("categoryId", category_id if False else TRAVEL_CATEGORY_ID),
            published_at=published_at,
            thumbnail=snippet.get("thumbnails", {}).get("medium", {}).get("url", ""),
            url=f"https://www.youtube.com/watch?v={video_id}",
            tags=snippet.get("tags", [])[:20],
            description=snippet.get("description", "")[:300],
        )

    def extract_keywords(self, items: list[YouTubeTrendItem], top_n: int = 20) -> list[tuple[str, float]]:
        """제목과 태그에서 키워드를 추출하고 조회수 기반 점수를 부여합니다."""
        keyword_scores: dict[str, float] = {}
        max_views = max((i.view_count for i in items), default=1)

        for item in items:
            score = item.view_count / max_views * 100
            tokens: list[str] = []

            for tag in item.tags:
                tokens.append(tag.lower().strip())

            words = item.title.lower().split()
            stop_words = {"the", "a", "an", "in", "on", "at", "to", "for", "of", "and", "or", "is", "are"}
            tokens.extend(w.strip(".,!?\"'") for w in words if w not in stop_words and len(w) > 3)

            for token in tokens:
                if not token:
                    continue
                keyword_scores[token] = max(keyword_scores.get(token, 0), score)

        sorted_kw = sorted(keyword_scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_kw[:top_n]
