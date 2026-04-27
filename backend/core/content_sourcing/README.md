# content_sourcing/ - 소재 수집 모듈

## 개요

Reddit API(PRAW) 등 외부 플랫폼에서 유튜브 콘텐츠 소재를 자동 수집하고 정리합니다.

## 주요 기능

- Reddit 서브레딧별 인기 게시물 수집
- 키워드 기반 필터링
- 소재 JSON/CSV 저장

## 인터페이스

```python
fetch_reddit_posts(subreddit: str, limit: int) -> list[Post]
filter_posts(posts: list[Post], keywords: list[str]) -> list[Post]
save_posts(posts: list[Post], format: str) -> str
```

## 필요 환경변수

```
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=
```

## 상태

- [ ] 개발 예정 (M2 단계)
