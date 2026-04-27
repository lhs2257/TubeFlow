# 작업 현황 (PROGRESS.md)

> 최종 업데이트: 2026-04-27 (.env.example Guardian/NewsAPI 항목 반영)

## 현재 단계

**[M5] 트렌드 분석 (trend_analyzer)** - 대기중

---

## 전체 작업 트리

```
유튜브 채널 운영 자동화 스위트
├── [v] 프로젝트 초기화 (2026-04-27 완료)
├── [v] [D0] UI/UX 디자인
│   ├── [v] D0-1. 전체 화면 구성 및 네비게이션 구조 설계
│   ├── [v] D0-2. 각 탭별 와이어프레임 작성
│   └── [v] D0-3. 디자인 시안 확정 및 references/01-design/ 저장
├── [v] [M1] 공통 기반 (shared/)
│   ├── [v] M1-1. 프로젝트 환경 설정 (.env.example, requirements.txt)
│   ├── [v] M1-2. 설정 관리 모듈 (shared/config/settings.py)
│   ├── [v] M1-3. API 인증 모듈 (shared/auth/ - Reddit, YouTube, OpenAI)
│   ├── [v] M1-4. 공통 유틸리티 (shared/utils/ - 로거, 파일 처리)
│   └── [v] M1-5. 백엔드 진입점 (backend/main.py)
├── [v] [M2] 소재 수집 (content_sourcing) - 여행 특화 멀티소스
│   ├── [v] M2-1. The Guardian Travel API (guardian.py)
│   ├── [v] M2-2. NewsAPI 여행 카테고리 (newsapi.py)
│   ├── [v] M2-3. RSS 피드 수집 - 6개 매체 (rss_reader.py)
│   ├── [v] M2-4. YouTube 트렌드 - 8개 국가 (youtube_trend.py)
│   ├── [v] M2-5. 통합 서비스 (service.py)
│   └── [v] M2-6. FastAPI 라우터 (api/sourcing.py)
├── [v] [M3] 대본 작성 (script_writer)
│   ├── [v] M3-1. 데이터 모델 (models.py)
│   ├── [v] M3-2. OpenAI 대본 생성기 (generator.py)
│   ├── [v] M3-3. 프롬프트 템플릿 - 4가지 어조 (templates.py)
│   ├── [v] M3-4. 서비스 레이어 (service.py)
│   └── [v] M3-5. FastAPI 라우터 (api/script.py)
├── [v] [M4] 업로드 예약 (uploader)
│   ├── [v] M4-1. 데이터 모델 (models.py)
│   ├── [v] M4-2. YouTube 업로더 - 즉시/예약 (uploader.py)
│   ├── [v] M4-3. 업로드 큐 스케줄러 (scheduler.py)
│   └── [v] M4-4. FastAPI 라우터 (api/uploader.py)
├── [ ] [M5] 트렌드 분석 (trend_analyzer)
│   ├── [ ] M5-1. YouTube 트렌드 수집
│   ├── [ ] M5-2. Google Trends 연동
│   └── [ ] M5-3. 트렌드 리포트 생성
├── [ ] [M6] 데스크톱 UI 통합 (desktop/)
│   ├── [ ] M6-1. 메인 윈도우 및 네비게이션
│   ├── [ ] M6-2. 각 탭별 UI 구현
│   └── [ ] M6-3. 백엔드 연동 테스트
└── [ ] [M7] 패키징 및 배포 (deploy/)
    ├── [ ] M7-1. PyInstaller .exe 빌드
    ├── [ ] M7-2. Docker 컨테이너화
    └── [ ] M7-3. 서버 배포 가이드 작성
```

## 마커 설명

| 마커 | 의미 |
|------|------|
| `[v]` | 완료 |
| `[>]` | 진행중 |
| `[ ]` | 대기 |
| `[!]` | 문제 발생 |

---

## 작업 로그

### 2026-04-27
- [v] 프로젝트 초기화 완료
  - 폴더 구조 생성
  - PROJECT.md, PROGRESS.md 생성
  - 각 모듈 README.md 생성
  - CLAUDE.md 업데이트
  - .gitignore 생성
  - git 초기화 및 초기 커밋
- [v] D0 UI/UX 디자인 완료
  - 앱명: TubeFlow
  - 다크 테마, 좌측 사이드바 + 4탭 구조
  - references/01-design/ 에 전체 파일 저장 (HTML + 7개 JSX)
- [v] M4 업로드 예약 완료
  - models.py (UploadJob, VideoMetadata, PrivacyStatus, UploadStatus)
  - uploader.py (YouTube Data API 업로드, 썸네일 설정)
  - scheduler.py (업로드 큐 관리, 예약 실행, 큐 영속화)
  - api/uploader.py (POST /add, POST /run, GET /queue, DELETE /cancel)
- [v] M3 대본 작성 완료
  - models.py (Script, ScriptRequest 데이터 모델)
  - templates.py (4가지 어조 프롬프트 - 정보/스토리/유머/드라마)
  - generator.py (OpenAI gpt-4o 대본 생성, 섹션 파싱)
  - service.py (생성 + JSON 저장)
  - api/script.py (POST /api/v1/script/generate)
- [v] M2 소재 수집 완료 (여행 특화 멀티소스로 전면 교체)
  - Reddit API 접근 불가로 인해 4개 소스로 교체
  - guardian.py (The Guardian Travel API - 5,000건/일)
  - newsapi.py (NewsAPI 여행 카테고리 - 100건/일)
  - rss_reader.py (Lonely Planet, NatGeo, BBC Travel 등 6개 매체)
  - youtube_trend.py (8개 국가 여행 인기 급상승 영상)
  - api/sourcing.py (POST /api/v1/sourcing/collect)
- [v] M1 공통 기반 완료
  - requirements.txt, .env.example (OpenAI 키 항목으로 업데이트)
  - shared/config/settings.py (pydantic-settings)
  - shared/auth/ (Reddit, YouTube, OpenAI 인증) - Anthropic -> OpenAI 교체
  - shared/utils/ (로거, 파일 유틸)
  - backend/main.py (FastAPI 진입점)
  - [>] .env 실제 API 키 입력 중 (Reddit, OpenAI, YouTube)

---

## 다음 할 일

**[M5-1] YouTube 트렌드 수집** (backend/core/trend_analyzer/)
