# trend_analyzer/ - 트렌드 분석 모듈

## 개요

YouTube Trends 및 Google Trends 데이터를 수집하여 트렌드 리포트를 생성합니다.

## 주요 기능

- YouTube 인기 동영상 트렌드 수집
- Google Trends 키워드 분석
- 트렌드 리포트 생성 (JSON/CSV)

## 인터페이스

```python
fetch_youtube_trends(region: str, category: str) -> list[TrendItem]
fetch_google_trends(keywords: list[str], period: str) -> TrendReport
generate_report(trends: list[TrendItem]) -> str
```

## 필요 환경변수

```
YOUTUBE_API_KEY=
```

## 상태

- [ ] 개발 예정 (M5 단계)
