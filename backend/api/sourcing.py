from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.core.content_sourcing import CollectConfig, ContentSourcingService

router = APIRouter(prefix="/sourcing", tags=["소재 수집"])
_service = ContentSourcingService()


class CollectRequest(BaseModel):
    keywords: list[str] = Field(default=["travel", "tourism"], examples=[["travel", "tourism", "destination"]])
    countries: list[str] = Field(default_factory=list)
    language: str = Field(default="en")
    limit: int = Field(default=20, ge=1, le=100)
    sources: list[str] = Field(default=["guardian", "newsapi", "rss", "youtube"])
    save_format: str = Field(default="json")


class CollectResponse(BaseModel):
    count: int
    saved_path: str
    articles: list[dict]


@router.post("/collect", response_model=CollectResponse)
async def collect_articles(req: CollectRequest):
    valid_sources = {"guardian", "newsapi", "rss", "youtube"}
    invalid = set(req.sources) - valid_sources
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


@router.get("/sources")
async def get_available_sources():
    return {
        "sources": [
            {"id": "guardian", "name": "The Guardian", "category": "뉴스", "limit": "5,000건/일"},
            {"id": "newsapi",  "name": "NewsAPI",       "category": "뉴스", "limit": "100건/일"},
            {"id": "rss",      "name": "RSS 피드",       "category": "미디어", "limit": "무제한"},
            {"id": "youtube",  "name": "YouTube Trends", "category": "동영상", "limit": "10,000유닛/일"},
        ]
    }
