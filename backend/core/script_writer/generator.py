import hashlib
import re
from datetime import datetime

from shared.auth import get_openai_client
from shared.config import get_settings
from shared.utils import get_logger
from .models import Script, ScriptRequest, ScriptSection
from .templates import SYSTEM_PROMPT, build_user_prompt

logger = get_logger(__name__)

WORDS_PER_SECOND = 130 / 60  # 분당 130자 -> 초당


class ScriptGenerator:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = get_openai_client()
        return self._client

    def generate(self, req: ScriptRequest) -> Script:
        logger.info("대본 생성 시작 - 소재: %s", req.source_title[:40])

        user_prompt = build_user_prompt(
            source_title=req.source_title,
            source_body=req.source_body,
            tone=req.tone,
            language=req.language,
            target_duration_min=req.target_duration_min,
            channel_intro=req.channel_intro,
            channel_outro=req.channel_outro,
        )

        response = self.client.chat.completions.create(
            model=get_settings().openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=0.8,
        )

        raw_text = response.choices[0].message.content
        sections = self._parse_sections(raw_text)
        script_id = hashlib.md5(f"{req.source_title}{datetime.utcnow()}".encode()).hexdigest()

        script = Script(
            id=script_id,
            title=f"[{req.tone.upper()}] {req.source_title}",
            source_title=req.source_title,
            source_url=req.source_url,
            tone=req.tone,
            sections=sections,
        )
        logger.info("대본 생성 완료 - 총 %d자, 예상 %d분", len(script.full_text), script.total_duration_sec // 60)
        return script

    def _parse_sections(self, text: str) -> list[ScriptSection]:
        patterns = {
            "intro": r"##\s*\[인트로\](.*?)(?=##\s*\[|$)",
            "main":  r"##\s*\[본문\](.*?)(?=##\s*\[|$)",
            "outro": r"##\s*\[아웃트로\](.*?)(?=##\s*\[|$)",
        }
        sections = []
        for section_type, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL)
            content = match.group(1).strip() if match else ""
            duration = int(len(content) / WORDS_PER_SECOND)
            sections.append(ScriptSection(type=section_type, content=content, duration_sec=duration))

        if not any(s.content for s in sections):
            sections = [ScriptSection(type="main", content=text.strip(), duration_sec=int(len(text) / WORDS_PER_SECOND))]

        return sections
