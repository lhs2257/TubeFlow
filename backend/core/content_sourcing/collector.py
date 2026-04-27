from datetime import datetime

import praw

from shared.auth import get_reddit_client
from shared.utils import get_logger
from .models import RedditPost, CollectConfig

logger = get_logger(__name__)


class RedditCollector:
    def __init__(self):
        self._client: praw.Reddit | None = None

    @property
    def client(self) -> praw.Reddit:
        if self._client is None:
            self._client = get_reddit_client()
        return self._client

    def fetch(self, config: CollectConfig) -> list[RedditPost]:
        posts: list[RedditPost] = []
        for subreddit_name in config.subreddits:
            try:
                fetched = self._fetch_subreddit(subreddit_name, config)
                posts.extend(fetched)
                logger.info("r/%s 수집 완료: %d건", subreddit_name, len(fetched))
            except Exception as e:
                logger.warning("r/%s 수집 실패: %s", subreddit_name, e)
        return posts

    def _fetch_subreddit(self, name: str, config: CollectConfig) -> list[RedditPost]:
        sub = self.client.subreddit(name.lstrip("r/"))
        raw_posts = self._get_sorted_posts(sub, config)
        return [self._to_post(p) for p in raw_posts if self._passes_filter(p, config)]

    def _get_sorted_posts(self, sub, config: CollectConfig):
        kwargs = {"limit": config.limit}
        match config.sort:
            case "top":
                return sub.top(time_filter=config.time_filter, **kwargs)
            case "hot":
                return sub.hot(**kwargs)
            case "new":
                return sub.new(**kwargs)
            case "rising":
                return sub.rising(**kwargs)
            case _:
                return sub.top(time_filter=config.time_filter, **kwargs)

    def _passes_filter(self, post, config: CollectConfig) -> bool:
        if post.score < config.min_score:
            return False
        if config.exclude_keywords:
            title_lower = post.title.lower()
            if any(kw.lower() in title_lower for kw in config.exclude_keywords):
                return False
        return True

    def _to_post(self, post) -> RedditPost:
        return RedditPost(
            id=post.id,
            title=post.title,
            body=post.selftext[:500] if post.selftext else "",
            subreddit=f"r/{post.subreddit.display_name}",
            score=post.score,
            num_comments=post.num_comments,
            url=post.url,
            permalink=post.permalink,
            created_at=datetime.utcfromtimestamp(post.created_utc),
            flair=post.link_flair_text or "",
        )
