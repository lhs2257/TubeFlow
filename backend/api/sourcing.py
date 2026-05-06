from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.core.content_sourcing import CollectConfig, ContentSourcingService
from backend.core.content_sourcing.rss_reader import RSS_FEEDS, RSS_SOURCE_IDS

router = APIRouter(prefix="/sourcing", tags=["소재 수집"])
_service = ContentSourcingService()

# 전체 허용 소스 ID
_ALL_SOURCES = {"guardian", "newsapi", "youtube"} | RSS_SOURCE_IDS

_DEFAULT_SOURCES = [
    "guardian", "newsapi",
    "scmp", "rfa",
    "nhk", "nikkei",
    "cna", "diplomat",
    "koreaherald", "reuters_asia", "bbc_asia",
    "youtube",
]

_DEFAULT_KEYWORDS = [
    "China", "Japan", "Southeast Asia", "ASEAN",
    "geopolitics", "Asia Pacific", "Taiwan", "North Korea",
]


class CollectRequest(BaseModel):
    keywords: list[str] = Field(default=_DEFAULT_KEYWORDS)
    countries: list[str] = Field(default_factory=list)
    language: str = Field(default="en")
    limit: int = Field(default=20, ge=1, le=100)
    sources: list[str] = Field(default=_DEFAULT_SOURCES)
    save_format: str = Field(default="json")


class CollectResponse(BaseModel):
    count: int
    saved_path: str
    articles: list[dict]


@router.post("/collect", response_model=CollectResponse)
async def collect_articles(req: CollectRequest):
    invalid = set(req.sources) - _ALL_SOURCES
    if invalid:
        raise HTTPException(status_code=400, detail=f"유효하지 않은 소스: {invalid}")

    config = CollectConfig(
        keywords=req.keywords,
        countries=req.countries,
        language=req.language,
        limit=req.limit,
        sources=req.sources,
    )
    result = _service.collect_and_save(config, fmt=req.save_format)
    return CollectResponse(**result)


@router.get("/keywords/trending")
async def get_trending_keywords(refresh: bool = False):
    """Google Trends 기반 최신 트렌딩 키워드를 반환합니다 (6시간 캐시)."""
    from backend.core.content_sourcing.keyword_suggester import get_trending_keywords
    return get_trending_keywords(force_refresh=refresh)


@router.get("/sources")
async def get_available_sources():
    rss_list = [
        {
            "id": fid,
            "name": name,
            "category": cat,
            "type": "rss",
            "limit": "무제한",
        }
        for fid, (name, _, cat) in RSS_FEEDS.items()
    ]
    return {
        "sources": [
            {"id": "guardian",  "name": "The Guardian",  "category": "world", "type": "api",     "limit": "5,000건/일"},
            {"id": "newsapi",   "name": "NewsAPI",        "category": "world", "type": "api",     "limit": "100건/일"},
            {"id": "youtube",   "name": "YouTube Trends", "category": "video", "type": "api",     "limit": "10,000유닛/일"},
            *rss_list,
        ]
    }
