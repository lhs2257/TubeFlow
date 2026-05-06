"""
트렌드 기반 검색 키워드 자동 제안 모듈.

Google Trends (pytrends) 로 최근 7일 트렌딩 연관 키워드를 수집하고
6시간 단위로 캐시하여 불필요한 API 호출을 방지합니다.
pytrends 오류 시 정적 기본값으로 폴백합니다.
"""
import json
import time
from pathlib import Path

from shared.utils import get_logger

logger = get_logger(__name__)

CACHE_FILE = Path("data/keyword_cache.json")
CACHE_TTL  = 6 * 3600  # 6시간 (초)

# Google Trends 조회 시드 키워드 (최대 5개씩)
_SEED_BATCH_1 = ["China", "Taiwan", "South China Sea", "Xi Jinping", "ASEAN"]
_SEED_BATCH_2 = ["Myanmar", "Vietnam", "North Korea", "Japan military", "Indo-Pacific"]

# 항상 포함할 고정 키워드 (안정적 결과 보장)
_STABLE_KEYWORDS = [
    "Taiwan strait",
    "South China Sea",
    "North Korea missile",
    "Indo-Pacific",
    "ASEAN summit",
    "China economy",
    "Myanmar coup",
    "US China rivalry",
]

# pytrends 실패 시 사용할 정적 폴백 목록
FALLBACK_KEYWORDS = [
    "Taiwan strait", "South China Sea", "Xi Jinping", "China economy",
    "Myanmar coup", "Cambodia China", "Vietnam politics",
    "North Korea missile", "Korea China relations", "Korea Japan",
    "Indo-Pacific", "US China rivalry", "ASEAN summit",
    "Japan military", "Asia geopolitics", "China sanctions",
]


def get_trending_keywords(force_refresh: bool = False) -> dict:
    """
    최신 트렌딩 키워드를 반환합니다.

    Returns:
        {
            "keywords": [...],
            "timestamp": float,
            "updated_at": "YYYY-MM-DD HH:MM",
            "source": "google_trends" | "cache" | "fallback"
        }
    """
    # 캐시 유효성 확인
    if not force_refresh and CACHE_FILE.exists():
        try:
            cached = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
            age = time.time() - cached.get("timestamp", 0)
            if age < CACHE_TTL:
                cached["source"] = "cache"
                return cached
        except Exception:
            pass

    try:
        from pytrends.request import TrendReq
        pytrends = TrendReq(hl="en-US", tz=540, timeout=(10, 30))

        trending_kws: set[str] = set()

        for seed_batch in [_SEED_BATCH_1, _SEED_BATCH_2]:
            try:
                pytrends.build_payload(seed_batch, timeframe="now 7-d", geo="KR")
                time.sleep(1.5)  # 쿼터 보호
                related = pytrends.related_queries()

                for data in related.values():
                    if not data:
                        continue
                    for kind in ("rising", "top"):
                        df = data.get(kind)
                        if df is not None and not df.empty:
                            for kw in df["query"].head(3).tolist():
                                kw = kw.strip()
                                # 너무 짧거나 숫자만인 키워드 제외
                                if len(kw) >= 4 and not kw.isdigit():
                                    trending_kws.add(kw)
            except Exception as e:
                logger.warning("pytrends 배치 조회 실패: %s", e)
                continue

        # 안정적 키워드 + 트렌딩 키워드 합산 (최대 16개)
        stable = list(_STABLE_KEYWORDS)
        dynamic = [k for k in list(trending_kws) if k not in stable]
        final = stable + dynamic
        final = final[:16]

        result = {
            "keywords": final,
            "timestamp": time.time(),
            "updated_at": _now_str(),
            "source": "google_trends",
        }
        _save_cache(result)
        logger.info("트렌딩 키워드 갱신 완료: %d개 (source=google_trends)", len(final))
        return result

    except Exception as e:
        logger.warning("트렌드 키워드 조회 실패, 폴백 사용: %s", e)
        result = {
            "keywords": FALLBACK_KEYWORDS,
            "timestamp": time.time(),
            "updated_at": _now_str(),
            "source": "fallback",
        }
        _save_cache(result)
        return result


def _save_cache(data: dict) -> None:
    try:
        CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CACHE_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    except Exception as e:
        logger.warning("키워드 캐시 저장 실패: %s", e)


def _now_str() -> str:
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M")
