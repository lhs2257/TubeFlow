from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Article:
    id: str
    title: str
    body: str
    source: str          # guardian | newsapi | rss | youtube
    source_name: str     # 매체명 (예: The Guardian, BBC Travel)
    url: str
    published_at: datetime
    country: str = ""
    category: str = "travel"
    thumbnail: str = ""
    is_selected: bool = False
    title_ko: str = ""   # 한국어 번역 제목 (번역 후 채워짐)
    body_ko: str = ""    # 한국어 번역 본문 (번역 후 채워짐)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "source": self.source,
            "source_name": self.source_name,
            "url": self.url,
            "published_at": self.published_at.isoformat(),
            "country": self.country,
            "category": self.category,
            "thumbnail": self.thumbnail,
            "is_selected": self.is_selected,
            "title_ko": self.title_ko,
            "body_ko": self.body_ko,
        }


@dataclass
class CollectConfig:
    keywords: list[str] = field(default_factory=lambda: [
        "China", "Japan", "Southeast Asia", "ASEAN",
        "geopolitics", "Asia Pacific", "Taiwan", "North Korea",
    ])
    countries: list[str] = field(default_factory=list)   # 빈 리스트 = 전세계
    language: str = "en"
    limit: int = 20
    sources: list[str] = field(default_factory=lambda: [
        "guardian", "newsapi",
        "scmp", "rfa",
        "nhk", "nikkei",
        "cna", "diplomat",
        "koreaherald", "reuters_asia", "bbc_asia",
        "youtube",
    ])
    rss_feeds: list[str] = field(default_factory=list)  # 선택된 RSS 피드 ID 목록
