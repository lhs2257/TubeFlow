from pathlib import Path

from shared.utils import get_logger, save_json, timestamped_filename
from .generator import ScriptGenerator
from .models import Script, ScriptRequest

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
        script = self.generate(req)
        path = self.save(script)
        return {
            "saved_path": str(path),
            **script.to_dict(),
        }
