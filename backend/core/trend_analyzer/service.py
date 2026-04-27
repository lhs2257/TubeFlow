import hashlib
from datetime import datetime
from pathlib import Path

from shared.utils import get_logger, save_json, load_json, timestamped_filename
from .models import TrendReport, TrendKeyword
from .youtube_trend import YouTubeTrendAnalyzer
from .google_trend import GoogleTrendAnalyzer

logger = get_logger(__name__)
REPORT_DIR = Path("data/trend_reports")


class TrendAnalyzerService:
    def __init__(self):
        self._yt = YouTubeTrendAnalyzer()
        self._gt = GoogleTrendAnalyzer()

    def analyze(
        self,
        regions: list[str] | None = None,
        google_keywords: list[str] | None = None,
        timeframe: str = "now 7-d",
        yt_limit_per_region: int = 10,
    ) -> TrendReport:
        regions = regions or ["US", "GB", "JP", "AU", "KR"]

        # YouTube 트렌드 수집
        yt_items = []
        for region in regions:
            yt_items.extend(self._yt.fetch_region(region_code=region, limit=yt_limit_per_region))

        # YouTube 키워드 추출
        yt_keywords_raw = self._yt.extract_keywords(yt_items, top_n=30)
        yt_top_words = [kw for kw, _ in yt_keywords_raw]

        # Google Trends 수집 (추출된 YouTube 키워드를 시드로 활용)
        seed_kw = google_keywords or yt_top_words[:10]
        gt_items = self._gt.fetch_interest(keywords=seed_kw, timeframe=timeframe)

        # 통합 키워드 점수 산출
        combined: dict[str, float] = {}
        for kw, score in yt_keywords_raw:
            combined[kw] = combined.get(kw, 0) + score * 0.4

        for gt in gt_items:
            combined[gt.keyword] = combined.get(gt.keyword, 0) + gt.interest_score * 0.6

        sorted_combined = sorted(combined.items(), key=lambda x: x[1], reverse=True)
        top_keywords = [kw for kw, _ in sorted_combined[:10]]

        keywords = []
        for kw, score in sorted_combined[:30]:
            source = "combined"
            if kw in [g.keyword for g in gt_items] and kw in yt_top_words:
                source = "combined"
            elif kw in [g.keyword for g in gt_items]:
                source = "google"
            else:
                source = "youtube"
            keywords.append(TrendKeyword(keyword=kw, score=round(score, 2), source=source))

        summary = f"상위 트렌드 키워드: {', '.join(top_keywords[:5])}" if top_keywords else "수집된 트렌드 없음"

        report_id = hashlib.md5(f"{datetime.utcnow().isoformat()}".encode()).hexdigest()[:12]
        report = TrendReport(
            id=report_id,
            generated_at=datetime.utcnow(),
            keywords=keywords,
            youtube_trends=yt_items,
            google_trends=gt_items,
            top_keywords=top_keywords,
            regions=regions,
            summary=summary,
        )

        self._save_report(report)
        logger.info("트렌드 리포트 생성 완료: %s (%s)", report_id, summary)
        return report

    def _save_report(self, report: TrendReport) -> None:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        filename = timestamped_filename("trend_report", "json")
        save_json(report.to_dict(), REPORT_DIR / filename)

    def load_latest_report(self) -> dict | None:
        if not REPORT_DIR.exists():
            return None
        files = sorted(REPORT_DIR.glob("*.json"), reverse=True)
        if not files:
            return None
        try:
            return load_json(files[0])
        except Exception as e:
            logger.warning("최신 트렌드 리포트 로드 실패: %s", e)
            return None

    def list_reports(self) -> list[dict]:
        if not REPORT_DIR.exists():
            return []
        files = sorted(REPORT_DIR.glob("*.json"), reverse=True)
        summaries = []
        for f in files[:20]:
            try:
                data = load_json(f)
                summaries.append({
                    "id": data.get("id", ""),
                    "generated_at": data.get("generated_at", ""),
                    "top_keywords": data.get("top_keywords", []),
                    "summary": data.get("summary", ""),
                    "regions": data.get("regions", []),
                    "file": f.name,
                })
            except Exception:
                continue
        return summaries
