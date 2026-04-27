import time

from shared.utils import get_logger
from .models import GoogleTrendItem

logger = get_logger(__name__)

TRAVEL_SEED_KEYWORDS = [
    "travel", "tourism", "vacation", "trip", "destination",
    "adventure", "backpacking", "solo travel", "travel tips",
]

try:
    from pytrends.request import TrendReq
    _PYTRENDS_AVAILABLE = True
except ImportError:
    _PYTRENDS_AVAILABLE = False
    logger.warning("pytrends 미설치 — Google Trends 기능 비활성화. `pip install pytrends`로 설치하세요.")


class GoogleTrendAnalyzer:
    """
    pytrends를 이용한 Google Trends 분석기.
    pytrends가 설치되지 않은 경우 빈 결과를 반환합니다.
    """

    def __init__(self, hl: str = "en-US", tz: int = 360):
        self._pytrends = None
        self._hl = hl
        self._tz = tz

    @property
    def pytrends(self):
        if self._pytrends is None:
            if not _PYTRENDS_AVAILABLE:
                raise RuntimeError("pytrends가 설치되지 않았습니다.")
            self._pytrends = TrendReq(hl=self._hl, tz=self._tz)
        return self._pytrends

    def fetch_interest(
        self,
        keywords: list[str] | None = None,
        timeframe: str = "now 7-d",
        geo: str = "",
    ) -> list[GoogleTrendItem]:
        if not _PYTRENDS_AVAILABLE:
            return []

        keywords = keywords or TRAVEL_SEED_KEYWORDS
        results: list[GoogleTrendItem] = []

        # Google Trends는 한 번에 최대 5개 키워드
        for i in range(0, len(keywords), 5):
            batch = keywords[i : i + 5]
            try:
                self.pytrends.build_payload(batch, timeframe=timeframe, geo=geo)
                df = self.pytrends.interest_over_time()

                if df.empty:
                    continue

                for kw in batch:
                    if kw not in df.columns:
                        continue
                    score = int(df[kw].mean())
                    related = self._get_related(kw)
                    results.append(
                        GoogleTrendItem(
                            keyword=kw,
                            interest_score=score,
                            region=geo or "WW",
                            timeframe=timeframe,
                            related_rising=related["rising"],
                            related_top=related["top"],
                        )
                    )
                time.sleep(1)  # API 쿼터 초과 방지
            except Exception as e:
                logger.warning("Google Trends 수집 실패 [%s]: %s", batch, e)

        logger.info("Google Trends 수집 완료: %d개 키워드", len(results))
        return results

    def fetch_related_queries(self, keyword: str) -> dict[str, list[str]]:
        if not _PYTRENDS_AVAILABLE:
            return {"rising": [], "top": []}
        return self._get_related(keyword)

    def _get_related(self, keyword: str) -> dict[str, list[str]]:
        try:
            related_data = self.pytrends.related_queries()
            kw_data = related_data.get(keyword, {})

            rising_df = kw_data.get("rising")
            top_df = kw_data.get("top")

            rising = rising_df["query"].tolist()[:10] if rising_df is not None and not rising_df.empty else []
            top = top_df["query"].tolist()[:10] if top_df is not None and not top_df.empty else []
            return {"rising": rising, "top": top}
        except Exception:
            return {"rising": [], "top": []}
