"""
수집된 소재 한국어 번역 모듈.

OpenAI GPT-4o-mini를 사용하여 자연스러운 한국어로 번역합니다.
배치 처리(15건/호출)로 API 비용을 최소화합니다.
번역 실패 시 원문을 그대로 반환합니다 (폴백).
"""
import json

from shared.utils import get_logger

logger = get_logger(__name__)

_BATCH_SIZE = 15    # 한 번의 API 호출에 처리할 기사 수
_BODY_LIMIT  = 250  # 번역할 본문 최대 길이 (미리보기용)

_SYSTEM_PROMPT = (
    "당신은 전문 한국어 번역가입니다. "
    "영문 뉴스 기사를 40~60대 한국인이 읽기 편한 자연스러운 문어체 한국어로 번역합니다. "
    "직역보다는 의역을 사용하여 자연스러운 문장을 만들어 주세요."
)


def translate_articles(articles: list[dict]) -> list[dict]:
    """
    article 딕셔너리 리스트의 title / body 를 한국어로 번역합니다.
    각 article 에 title_ko / body_ko 키를 추가하여 반환합니다.
    """
    try:
        from openai import OpenAI
        from shared.config.settings import get_settings
        settings = get_settings()
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY 미설정")
        client = OpenAI(api_key=settings.openai_api_key)
    except Exception as e:
        logger.warning("OpenAI 초기화 실패 — 번역 생략: %s", e)
        for art in articles:
            art["title_ko"] = art.get("title", "")
            art["body_ko"]  = art.get("body",  "")
        return articles

    # 이미 한국어인 항목은 건너뜀
    to_translate: list[int] = []
    for i, art in enumerate(articles):
        title = art.get("title", "").strip()
        body  = art.get("body",  "").strip()
        if _is_korean(title) and _is_korean(body):
            art["title_ko"] = title
            art["body_ko"]  = body
        else:
            to_translate.append(i)

    if not to_translate:
        logger.info("번역 생략: 전체 기사가 이미 한국어입니다.")
        return articles

    logger.info("번역 대상: %d건 (배치 크기: %d)", len(to_translate), _BATCH_SIZE)

    # 배치 단위 처리
    for batch_start in range(0, len(to_translate), _BATCH_SIZE):
        batch_indices = to_translate[batch_start:batch_start + _BATCH_SIZE]
        batch_data    = [articles[i] for i in batch_indices]
        translated    = _translate_batch(client, batch_data)
        for idx, result in zip(batch_indices, translated):
            articles[idx]["title_ko"] = result.get("title_ko") or articles[idx].get("title", "")
            articles[idx]["body_ko"]  = result.get("body_ko")  or articles[idx].get("body",  "")

    # 누락 항목 보완
    for art in articles:
        if "title_ko" not in art:
            art["title_ko"] = art.get("title", "")
        if "body_ko" not in art:
            art["body_ko"] = art.get("body", "")

    logger.info("번역 완료: %d건", len(articles))
    return articles


def _translate_batch(client, batch: list[dict]) -> list[dict]:
    """배치 단위로 OpenAI API를 호출하여 번역합니다."""
    items = []
    for i, art in enumerate(batch):
        items.append({
            "idx":   i,
            "title": art.get("title", "").strip(),
            "body":  art.get("body",  "").strip()[:_BODY_LIMIT],
        })

    user_prompt = (
        "아래 뉴스 기사 목록의 title과 body를 한국어로 번역하세요.\n"
        "반드시 다음 형식의 JSON으로만 응답하세요:\n"
        '{"translations": [{"title_ko": "번역된 제목", "body_ko": "번역된 본문"}, ...]}\n\n'
        f"기사 목록 (JSON):\n{json.dumps(items, ensure_ascii=False, indent=2)}"
    )

    fallback = [
        {"title_ko": art.get("title", ""), "body_ko": art.get("body", "")}
        for art in batch
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.2,
            response_format={"type": "json_object"},
        )
        raw = response.choices[0].message.content.strip()
        parsed = json.loads(raw)

        translations = parsed.get("translations", [])
        if len(translations) != len(batch):
            logger.warning("번역 결과 수 불일치: 요청 %d건, 응답 %d건", len(batch), len(translations))
            # 개수가 맞지 않으면 인덱스 범위 내에서만 사용
            result = fallback[:]
            for i, t in enumerate(translations):
                if i < len(result):
                    result[i] = t
            return result

        return translations

    except Exception as e:
        logger.warning("배치 번역 실패 (%d건): %s", len(batch), e)
        return fallback


def _is_korean(text: str) -> bool:
    """텍스트의 30% 이상이 한글이면 이미 한국어로 판단합니다."""
    if not text:
        return True  # 빈 텍스트는 번역 불필요
    korean = sum(1 for c in text if "가" <= c <= "힣")
    return korean / len(text) > 0.3
