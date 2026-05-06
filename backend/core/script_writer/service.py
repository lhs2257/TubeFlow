from pathlib import Path

from shared.utils import get_logger, save_json, timestamped_filename
from .generator import ScriptGenerator
from .models import Script, ScriptRequest
from .scraper import fetch_article_text

logger = get_logger(__name__)
OUTPUT_DIR = Path("data/scripts")


class ScriptWriterService:
    def __init__(self):
        self.generator = ScriptGenerator()

    def generate(self, req: ScriptRequest) -> Script:
        return self.generator.generate(req)

    def save(self, script: Script) -> Path:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        path = OUTPUT_DIR / timestamped_filename("script", "json")
        return save_json(script.to_dict(), path)

    def generate_and_save(self, req: ScriptRequest) -> dict:
        # URL이 있으면 전체 기사 본문 추출 후 source_body 교체
        if req.source_url:
            full_body = fetch_article_text(req.source_url)
            if full_body:
                logger.info("URL 본문 추출 성공 — source_body 교체 (%d자)", len(full_body))
                req = ScriptRequest(
                    source_title=req.source_title,
                    source_body=full_body,
                    source_url=req.source_url,
                    tone=req.tone,
                    language=req.language,
                    target_duration_sec=req.target_duration_sec,
                    channel_intro=req.channel_intro,
                    channel_outro=req.channel_outro,
                )
            else:
                logger.info("URL 본문 추출 실패 — 기존 source_body 사용")

        script = self.generate(req)
        path = self.save(script)
        return {
            "saved_path": str(path),
            **script.to_dict(),
        }
