# trend_analyzer/ - 트렌드 분석 모듈

## 개요

YouTube Data API와 Google Trends(pytrends)를 결합하여 여행 관련 트렌드를 분석하고
통합 리포트를 생성합니다. YouTube 인기 급상승 영상에서 키워드를 추출하고,
해당 키워드의 Google 검색 관심도를 교차 분석하여 점수를 산출합니다.

## 파일 구조

```
trend_analyzer/
  models.py        TrendReport, TrendKeyword, YouTubeTrendItem, GoogleTrendItem
  youtube_trend.py YouTubeTrendAnalyzer - 조회수/좋아요/태그 포함 수집
  google_trend.py  GoogleTrendAnalyzer - pytrends 기반 관심도 및 연관 키워드
  service.py       TrendAnalyzerService - 통합 분석 + 리포트 저장/조회
  __init__.py
```

## 주요 인터페이스

```python
from backend.core.trend_analyzer import TrendAnalyzerService

service = TrendAnalyzerService()

# 트렌드 분석 실행 (YouTube + Google Trends 통합)
report = service.analyze(
    regions=["US", "GB", "JP", "KR"],
    google_keywords=["travel", "vacation"],  # None이면 YouTube에서 자동 추출
    timeframe="now 7-d",
    yt_limit_per_region=10,
)

# 리포트는 data/trend_reports/*.json 에 자동 저장됨
latest = service.load_latest_report()   # dict
reports = service.list_reports()         # list[dict]
```

## API 엔드포인트

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | /api/v1/trend/analyze | 트렌드 분석 실행 |
| GET  | /api/v1/trend/report/latest | 최신 리포트 전체 조회 |
| GET  | /api/v1/trend/report/list | 저장된 리포트 목록 |
| GET  | /api/v1/trend/keywords | 최신 리포트 상위 키워드 |
| GET  | /api/v1/trend/regions | 지원 국가 목록 |

## 키워드 점수 산출 방식

- YouTube 점수 (40%): 조회수를 정규화한 0~100 점수
- Google 점수 (60%): Google Trends interest_over_time 평균값 (0~100)
- 두 소스 모두 있는 키워드: combined (가중 합산)

## 필요 환경변수

```
YOUTUBE_API_KEY=   # YouTube Data API 키 (필수)
```

pytrends는 별도 인증 불필요 (공개 Google Trends 크롤링).
단, `pip install pytrends` 설치가 필요합니다.

## 상태

- [v] 개발 완료 (M5 단계, 2026-04-27)
