from pathlib import Path

from shared.utils import get_logger, save_json, save_csv, timestamped_filename
from .collector import RedditCollector
from .models import CollectConfig, RedditPost

logger = get_logger(__name__)
OUTPUT_DIR = Path("data/sourcing")


class ContentSourcingService:
    def __init__(self):
        self.collector = RedditCollector()

    def collect(self, config: CollectConfig) -> list[RedditPost]:
        logger.info("소재 수집 시작 - 서브레딧: %s", config.subreddits)
        posts = self.collector.fetch(config)
        logger.info("소재 수집 완료 - 총 %d건", len(posts))
        return posts

    def save(self, posts: list[RedditPost], fmt: str = "json") -> Path:
        data = [p.to_dict() for p in posts]
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if fmt == "csv":
            path = OUTPUT_DIR / timestamped_filename("posts", "csv")
            return save_csv(data, path)
        path = OUTPUT_DIR / timestamped_filename("posts", "json")
        return save_json(data, path)

    def collect_and_save(self, config: CollectConfig, fmt: str = "json") -> dict:
        posts = self.collect(config)
        path = self.save(posts, fmt)
        return {
            "count": len(posts),
            "saved_path": str(path),
            "posts": [p.to_dict() for p in posts],
        }
