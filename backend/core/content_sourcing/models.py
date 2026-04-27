from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class RedditPost:
    id: str
    title: str
    body: str
    subreddit: str
    score: int
    num_comments: int
    url: str
    permalink: str
    created_at: datetime
    flair: str = ""
    is_selected: bool = False

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "subreddit": self.subreddit,
            "score": self.score,
            "num_comments": self.num_comments,
            "url": self.url,
            "permalink": f"https://reddit.com{self.permalink}",
            "created_at": self.created_at.isoformat(),
            "flair": self.flair,
            "is_selected": self.is_selected,
        }


@dataclass
class CollectConfig:
    subreddits: list[str]
    time_filter: str = "week"       # hour | day | week | month | year | all
    sort: str = "top"               # top | hot | new | rising
    limit: int = 50
    min_score: int = 0
    exclude_keywords: list[str] = field(default_factory=list)
