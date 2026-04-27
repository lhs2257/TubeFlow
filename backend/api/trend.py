from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.core.trend_analyzer import TrendAnalyzerService

router = APIRouter(prefix="/trend", tags=["트렌드 분석"])
_service = TrendAnalyzerService()


class AnalyzeRequest(BaseModel):
    regions: list[str] = Field(
        default=["US", "GB", "JP", "AU", "KR"],
        examples=[["US", "GB", "JP"]],
    )
    google_keywords: list[str] = Field(
        default=[],
        description="Google Trends에 조회할 시드 키워드 (비어있으면 YouTube 추출 키워드 자동 사용)",
    )
    timeframe: str = Field(
        default="now 7-d",
        description="Google Trends 기간 (now 1-d / now 7-d / today 1-m / today 3-m)",
    )
    yt_limit_per_region: int = Field(default=10, ge=1, le=50)


class AnalyzeResponse(BaseModel):
    id: str
    generated_at: str
    top_keywords: list[str]
    summary: str
    regions: list[str]
    keyword_count: int
    youtube_trend_count: int
    google_trend_count: int


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_trends(req: AnalyzeRequest):
    """트렌드 분석을 실행하고 리포트를 생성합니다."""
    try:
        report = _service.analyze(
            regions=req.regions,
            google_keywords=req.google_keywords or None,
            timeframe=req.timeframe,
            yt_limit_per_region=req.yt_limit_per_region,
        )
        return AnalyzeResponse(
            id=report.id,
            generated_at=report.generated_at.isoformat(),
            top_keywords=report.top_keywords,
            summary=report.summary,
            regions=report.regions,
            keyword_count=len(report.keywords),
            youtube_trend_count=len(report.youtube_trends),
            google_trend_count=len(report.google_trends),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"트렌드 분석 실패: {e}")


@router.get("/report/latest")
async def get_latest_report():
    """가장 최근 트렌드 리포트 전체를 반환합니다."""
    data = _service.load_latest_report()
    if not data:
        raise HTTPException(status_code=404, detail="저장된 트렌드 리포트가 없습니다.")
    return data


@router.get("/report/list")
async def list_reports():
    """저장된 트렌드 리포트 목록을 반환합니다 (최근 20개)."""
    return {"reports": _service.list_reports()}


@router.get("/keywords")
async def get_keywords(top: int = Query(default=20, ge=1, le=100)):
    """최신 리포트의 상위 키워드를 반환합니다."""
    data = _service.load_latest_report()
    if not data:
        raise HTTPException(status_code=404, detail="저장된 트렌드 리포트가 없습니다.")
    keywords = data.get("keywords", [])[:top]
    return {
        "generated_at": data.get("generated_at"),
        "top_keywords": data.get("top_keywords", []),
        "keywords": keywords,
    }


@router.get("/regions")
async def get_supported_regions():
    """지원하는 YouTube 트렌드 수집 국가 목록을 반환합니다."""
    from backend.core.trend_analyzer.youtube_trend import REGION_CODES
    return {"regions": [{"code": code, "name": name} for code, name in REGION_CODES.items()]}
