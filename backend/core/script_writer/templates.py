TONE_DESCRIPTIONS = {
    "informative":   "정보 전달 중심, 명확하고 신뢰감 있는 어조",
    "storytelling":  "이야기 형식, 감성적이고 몰입감 있는 서술",
    "humor":         "유머와 위트를 곁들인 가볍고 친근한 어조",
    "dramatic":      "긴장감과 감동을 극대화하는 드라마틱한 어조",
}

SYSTEM_PROMPT = """당신은 유튜브 여행 채널 전문 대본 작가입니다.
주어진 소재를 바탕으로 시청자가 끝까지 보고 싶은 대본을 작성합니다.

규칙:
- 반드시 [인트로], [본문], [아웃트로] 세 섹션으로 구성
- 각 섹션은 "## [인트로]", "## [본문]", "## [아웃트로]" 헤더로 구분
- 구어체로 작성 (실제 말하듯이)
- 시청자를 "여러분"으로 호칭
- 숫자와 통계는 구체적으로 언급
- 섹션 사이 전환이 자연스럽게 연결"""


def build_user_prompt(
    source_title: str,
    source_body: str,
    tone: str,
    language: str,
    target_duration_min: int,
    channel_intro: str,
    channel_outro: str,
) -> str:
    tone_desc = TONE_DESCRIPTIONS.get(tone, TONE_DESCRIPTIONS["informative"])
    lang_desc = "한국어" if language == "ko" else "영어"
    word_count = target_duration_min * 130  # 분당 약 130단어 기준

    intro_note = f"\n채널 고정 인트로: {channel_intro}" if channel_intro else ""
    outro_note = f"\n채널 고정 아웃트로: {channel_outro}" if channel_outro else ""

    return f"""다음 소재로 유튜브 여행 대본을 작성해주세요.

[소재 제목]
{source_title}

[소재 내용]
{source_body}

[작성 조건]
- 언어: {lang_desc}
- 어조: {tone_desc}
- 목표 길이: 약 {target_duration_min}분 ({word_count}자 내외){intro_note}{outro_note}

[인트로]에서는 시청자의 호기심을 자극하는 후킹 문장으로 시작하세요.
[본문]에서는 소재의 핵심 내용을 흥미롭게 전달하세요.
[아웃트로]에서는 구독/좋아요 요청과 함께 다음 영상 예고로 마무리하세요."""
