# backend/ - FastAPI 백엔드

## 개요

모든 핵심 기능을 REST API로 제공하는 FastAPI 백엔드입니다.
로컬 실행 또는 서버 배포 모두 지원합니다.

## 구조

```
backend/
├── api/                     # API 라우터
│   ├── sourcing.py          # /api/v1/sourcing
│   ├── script.py            # /api/v1/script
│   ├── uploader.py          # /api/v1/uploader
│   └── trend.py             # /api/v1/trend
├── core/                    # 핵심 비즈니스 로직
│   ├── content_sourcing/
│   ├── script_writer/
│   ├── uploader/
│   └── trend_analyzer/
└── db/                      # 데이터베이스 모델 및 마이그레이션
```

## 실행 방법

```bash
uvicorn backend.main:app --reload --port 8000
```

## API 문서

서버 실행 후 `http://localhost:8000/docs` 에서 Swagger UI 확인 가능

## 상태

- [ ] 개발 예정 (M1~M5 단계)
