TONE_DESCRIPTIONS = {
    "informative":   "사실 중심 해설, 명확하고 신뢰감 있는 어조",
    "storytelling":  "이야기 형식, 감성적이고 몰입감 있는 서술",
    "humor":         "유머와 위트를 곁들인 가볍고 친근한 어조",
    "dramatic":      "긴장감과 충격을 극대화하는 드라마틱한 어조",
}

SYSTEM_PROMPT = """당신은 유튜브 쇼츠 전문 대본 작가입니다.
중국, 일본, 동남아시아, 북한 등 아시아 정세와 국제 이슈를 다루는 채널을 위해 대본을 작성합니다.
주 시청자는 40~60대 한국인으로, 깊이 있는 정보를 원하되 짧고 임팩트 있는 영상을 선호합니다.

규칙:
- 반드시 [인트로], [본문], [아웃트로] 세 섹션으로 구성
- 각 섹션은 "## [인트로]", "## [본문]", "## [아웃트로]" 헤더로 구분
- 구어체로 작성 (실제 말하듯이, 입에 붙는 문장)
- 시청자를 "여러분"으로 호칭
- [인트로]는 2~3문장으로 짧고 강렬하게 (후킹 필수)
- [본문]은 핵심 사실을 압축해서 전달 (불필요한 설명 금지)
- [아웃트로]는 1~2문장으로 마무리 (구독 유도 포함)
- 목표 글자 수를 반드시 준수하여 지정된 시간 안에 읽힐 수 있도록 작성"""


def build_user_prompt(
    source_title: str,
    source_body: str,
    tone: str,
    language: str,
    target_duration_sec: int,
    channel_intro: str,
    channel_outro: str,
) -> str:
    tone_desc = TONE_DESCRIPTIONS.get(tone, TONE_DESCRIPTIONS["informative"])
    lang_desc = "한국어" if language == "ko" else "영어"
    # 한국어 구어체 분당 약 250자 기준
    target_chars = int(target_duration_sec / 60 * 250)

    intro_note = f"\n채널 고정 인트로: {channel_intro}" if channel_intro else ""
    outro_note = f"\n채널 고정 아웃트로: {channel_outro}" if channel_outro else ""

    return f"""다음 소재로 유튜브 쇼츠 대본을 작성해주세요.

[소재 제목]
{source_title}

[소재 내용]
{source_body}

[작성 조건]
- 언어: {lang_desc}
- 어조: {tone_desc}
- 목표 길이: {target_duration_sec}초 이내 ({target_chars}자 내외){intro_note}{outro_note}

[인트로]에서는 첫 문장부터 시청자가 멈춰서 볼 만한 충격적이거나 흥미로운 후킹 문장으로 시작하세요.
[본문]에서는 소재의 핵심 내용만 압축하여 군더더기 없이 전달하세요.
[아웃트로]에서는 한 줄로 마무리하고 구독/좋아요를 자연스럽게 유도하세요."""
