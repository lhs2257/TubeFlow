"""
수집된 소재 한국어 번역 모듈.

deep-translator (GoogleTranslator 무료 백엔드) 를 사용합니다.
이미 한국어인 텍스트는 번역을 건너뜁니다.
번역 실패 시 원문을 그대로 반환합니다 (폴백).
"""
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from shared.utils import get_logger

logger = get_logger(__name__)

_MAX_WORKERS  = 5    # 병렬 번역 스레드 수
_CHAR_LIMIT   = 500  # 번역 텍스트 최대 길이 (Google 제한)
_DELAY        = 0.08  # 요청 간 딜레이 (초) — 과도한 호출 방지


def translate_articles(articles: list[dict]) -> list[dict]:
    """
    article 딕셔너리 리스트의 title / body 를 한국어로 번역합니다.
    각 article 에 title_ko / body_ko 키를 추가하여 반환합니다.
    """
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        logger.warning("deep-translator 미설치 — 번역 생략")
        for art in articles:
            art["title_ko"] = art.get("title", "")
            art["body_ko"]  = art.get("body", "")
        return articles

    texts_to_translate: list[tuple[int, str, str]] = []  # (idx, field, text)

    for i, art in enumerate(articles):
        title = art.get("title", "").strip()
        body  = art.get("body",  "").strip()
        if title and not _is_korean(title):
            texts_to_translate.append((i, "title", title[:_CHAR_LIMIT]))
        else:
            art["title_ko"] = title
        if body and not _is_korean(body):
            texts_to_translate.append((i, "body", body[:_CHAR_LIMIT]))
        else:
            art["body_ko"] = body

    if not texts_to_translate:
        return articles

    def _translate_one(item: tuple[int, str, str]) -> tuple[int, str, str]:
        idx, field, text = item
        try:
            translator = GoogleTranslator(source="auto", target="ko")
            result = translator.translate(text) or text
            time.sleep(_DELAY)
            return idx, field, result
        except Exception as e:
            logger.debug("번역 실패 [%d/%s]: %s", idx, field, e)
            return idx, field, text  # 폴백: 원문 반환

    with ThreadPoolExecutor(max_workers=_MAX_WORKERS) as pool:
        futures = {pool.submit(_translate_one, item): item for item in texts_to_translate}
        for future in as_completed(futures):
            try:
                idx, field, translated = future.result()
                articles[idx][f"{field}_ko"] = translated
            except Exception as e:
                logger.warning("번역 결과 처리 오류: %s", e)

    # 번역이 설정되지 않은 항목 보완
    for art in articles:
        if "title_ko" not in art:
            art["title_ko"] = art.get("title", "")
        if "body_ko" not in art:
            art["body_ko"] = art.get("body", "")

    logger.info("번역 완료: %d건", len(articles))
    return articles


def _is_korean(text: str) -> bool:
    """텍스트의 30% 이상이 한글이면 이미 한국어로 판단합니다."""
    if not text:
        return False
    korean = sum(1 for c in text if "가" <= c <= "힣")
    return korean / len(text) > 0.3
