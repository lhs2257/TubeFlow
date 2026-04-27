from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.core.content_sourcing import CollectConfig, ContentSourcingService

router = APIRouter(prefix="/sourcing", tags=["소재 수집"])
_service = ContentSourcingService()


class CollectRequest(BaseModel):
    subreddits: list[str] = Field(..., examples=[["r/AskReddit", "r/todayilearned"]])
    time_filter: str = Field(default="week")
    sort: str = Field(default="top")
    limit: int = Field(default=50, ge=1, le=200)
    min_score: int = Field(default=0, ge=0)
    exclude_keywords: list[str] = Field(default_factory=list)
    save_format: str = Field(default="json")


class CollectResponse(BaseModel):
    count: int
    saved_path: str
    posts: list[dict]


@router.post("/collect", response_model=CollectResponse)
async def collect_posts(req: CollectRequest):
    if not req.subreddits:
        raise HTTPException(status_code=400, detail="서브레딧을 하나 이상 입력해주세요.")
    config = CollectConfig(
        subreddits=req.subreddits,
        time_filter=req.time_filter,
        sort=req.sort,
        limit=req.limit,
        min_score=req.min_score,
        exclude_keywords=req.exclude_keywords,
    )
    result = _service.collect_and_save(config, fmt=req.save_format)
    return CollectResponse(**result)
