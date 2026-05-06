from pathlib import Path

from shared.utils import get_logger, save_json, save_csv, timestamped_filename
from .models import CollectConfig, Article
from .guardian import GuardianCollector
from .newsapi import NewsAPICollector
from .rss_reader import RSSCollector, RSS_FEEDS, RSS_SOURCE_IDS
from .youtube_trend import YouTubeTrendCollector
from .translator import translate_articles

logger = get_logger(__name__)
OUTPUT_DIR = Path("data/sourcing")


class ContentSourcingService:
    def __init__(self):
        self._guardian  = GuardianCollector()
        self._newsapi   = NewsAPICollector()
        self._rss       = RSSCollector()
        self._youtube   = YouTubeTrendCollector()

    def collect(self, config: CollectConfig) -> list[Article]:
        logger.info("소재 수집 시작 - 소스: %s", config.sources)
        articles: list[Article] = []

        # 선택된 소스 중 RSS 피드 ID만 추려 한 번에 수집
        selected_rss = [s for s in config.sources if s in RSS_SOURCE_IDS]

        for source in config.sources:
            try:
                if source == "guardian":
                    fetched = self._guardian.fetch(config.keywords, config.limit)
                elif source == "newsapi":
                    fetched = self._newsapi.fetch(config.keywords, config.language, config.limit)
                elif source == "youtube":
                    fetched = self._youtube.fetch_multi_region(limit_per_region=max(1, config.limit // 8))
                elif source in RSS_SOURCE_IDS:
                    # RSS는 선택된 피드 목록 전체를 한 번만 수집 (중복 방지)
                    if source == selected_rss[0]:
                        fetched = self._rss.fetch(
                            limit_per_feed=max(1, config.limit // max(len(selected_rss), 1)),
                            feed_ids=selected_rss,
                        )
                    else:
                        continue  # 첫 번째 RSS 소스에서 이미 전체 수집함
                else:
                    fetched = []
                articles.extend(fetched)
            except Exception as e:
                logger.warning("[%s] 수집 중 오류: %s", source, e)

        # 최근 날짜순 정렬
        articles.sort(key=lambda a: a.published_at, reverse=True)

        # 한국어 번역 (title_ko / body_ko 채우기)
        article_dicts = [a.to_dict() for a in articles]
        article_dicts = translate_articles(article_dicts)
        for art, d in zip(articles, article_dicts):
            art.title_ko = d.get("title_ko", "")
            art.body_ko  = d.get("body_ko",  "")

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
