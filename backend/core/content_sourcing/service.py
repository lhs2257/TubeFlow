from pathlib import Path

from shared.utils import get_logger, save_json, save_csv, timestamped_filename
from .models import CollectConfig, Article
from .guardian import GuardianCollector
from .newsapi import NewsAPICollector
from .rss_reader import RSSCollector
from .youtube_trend import YouTubeTrendCollector

logger = get_logger(__name__)
OUTPUT_DIR = Path("data/sourcing")


class ContentSourcingService:
    def __init__(self):
        self._collectors = {
            "guardian": GuardianCollector(),
            "newsapi":  NewsAPICollector(),
            "rss":      RSSCollector(),
            "youtube":  YouTubeTrendCollector(),
        }

    def collect(self, config: CollectConfig) -> list[Article]:
        logger.info("소재 수집 시작 - 소스: %s", config.sources)
        articles: list[Article] = []

        for source in config.sources:
            collector = self._collectors.get(source)
            if not collector:
                continue
            try:
                if source == "guardian":
                    fetched = collector.fetch(config.keywords, config.limit)
                elif source == "newsapi":
                    fetched = collector.fetch(config.keywords, config.language, config.limit)
                elif source == "rss":
                    fetched = collector.fetch(limit_per_feed=max(1, config.limit // 6))
                elif source == "youtube":
                    fetched = collector.fetch_multi_region(limit_per_region=max(1, config.limit // 8))
                else:
                    fetched = []
                articles.extend(fetched)
            except Exception as e:
                logger.warning("[%s] 수집 중 오류: %s", source, e)

        logger.info("소재 수집 완료 - 총 %d건", len(articles))
        return articles

    def save(self, articles: list[Article], fmt: str = "json") -> Path:
        data = [a.to_dict() for a in articles]
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        if fmt == "csv":
            path = OUTPUT_DIR / timestamped_filename("articles", "csv")
            return save_csv(data, path)
        path = OUTPUT_DIR / timestamped_filename("articles", "json")
        return save_json(data, path)

    def collect_and_save(self, config: CollectConfig, fmt: str = "json") -> dict:
        articles = self.collect(config)
        path = self.save(articles, fmt)
        return {
            "count": len(articles),
            "saved_path": str(path),
            "articles": [a.to_dict() for a in articles],
        }
