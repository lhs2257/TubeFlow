from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TrendKeyword:
    keyword: str
    score: float          # 0~100 (Google Trends 기준, YouTube는 조회수 정규화)
    source: str           # "google" | "youtube" | "combined"
    region: str = "WW"   # ISO 국가 코드 또는 WW(전세계)
    related: list[str] = field(default_factory=list)


@dataclass
class YouTubeTrendItem:
    video_id: str
    title: str
    channel: str
    region: str
    view_count: int
    like_count: int
    comment_count: int
    category_id: str
    published_at: datetime
    thumbnail: str
    url: str
    tags: list[str] = field(default_factory=list)
    description: str = ""


@dataclass
class GoogleTrendItem:
    keyword: str
    interest_score: int   # 0~100
    region: str
    timeframe: str        # "now 7-d" 등
    related_rising: list[str] = field(default_factory=list)
    related_top: list[str] = field(default_factory=list)


@dataclass
class TrendReport:
    id: str
    generated_at: datetime
    keywords: list[TrendKeyword]
    youtube_trends: list[YouTubeTrendItem]
    google_trends: list[GoogleTrendItem]
    top_keywords: list[str]      # 상위 10개 통합 키워드
    regions: list[str]           # 분석에 포함된 국가 코드 목록
    summary: str = ""            # 리포트 한 줄 요약

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "generated_at": self.generated_at.isoformat(),
            "top_keywords": self.top_keywords,
            "regions": self.regions,
            "summary": self.summary,
            "keywords": [
                {
                    "keyword": k.keyword,
                    "score": k.score,
                    "source": k.source,
                    "region": k.region,
                    "related": k.related,
                }
                for k in self.keywords
            ],
            "youtube_trends": [
                {
                    "video_id": v.video_id,
                    "title": v.title,
                    "channel": v.channel,
                    "region": v.region,
                    "view_count": v.view_count,
                    "like_count": v.like_count,
                    "comment_count": v.comment_count,
                    "published_at": v.published_at.isoformat(),
                    "thumbnail": v.thumbnail,
                    "url": v.url,
                    "tags": v.tags,
                }
                for v in self.youtube_trends
            ],
            "google_trends": [
                {
                    "keyword": g.keyword,
                    "interest_score": g.interest_score,
                    "region": g.region,
                    "timeframe": g.timeframe,
                    "related_rising": g.related_rising,
                    "related_top": g.related_top,
                }
                for g in self.google_trends
            ],
        }
