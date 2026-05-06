"""
기사 URL 본문 추출 모듈.

trafilatura를 사용하여 뉴스 기사의 전체 본문을 추출합니다.
추출 실패 시 빈 문자열을 반환합니다 (폴백은 호출부에서 처리).
"""
from shared.utils import get_logger

logger = get_logger(__name__)

_MAX_CHARS = 3000  # GPT 프롬프트 비용 절감용 최대 길이


def fetch_article_text(url: str) -> str:
    """
    주어진 URL에서 기사 본문을 추출하여 반환합니다.
    실패 시 빈 문자열을 반환합니다.
    """
    if not url or not url.startswith("http"):
        return ""

    try:
        import trafilatura

        downloaded = trafilatura.fetch_url(url)
        if not downloaded:
            logger.warning("URL 다운로드 실패: %s", url)
            return ""

        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=False,
            no_fallback=False,
        )
        if not text:
            logger.warning("본문 추출 실패 (빈 결과): %s", url)
            return ""

        text = text.strip()
        if len(text) > _MAX_CHARS:
            text = text[:_MAX_CHARS] + "..."

        logger.info("기사 본문 추출 완료: %d자 (%s...)", len(text), url[:50])
        return text

    except Exception as e:
        logger.warning("기사 본문 추출 오류: %s — %s", url, e)
        return ""
