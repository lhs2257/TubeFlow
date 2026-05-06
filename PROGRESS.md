# 작업 현황 (PROGRESS.md)

> 최종 업데이트: 2026-05-06 (RSS 수집 개수 버그 수정 / 원문 버튼 위치 개선)

## 현재 단계

**[M7] 패키징 및 배포 (deploy/)** - 대기중

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
├── [v] [M5] 트렌드 분석 (trend_analyzer)
│   ├── [v] M5-1. YouTube 트렌드 수집 (youtube_trend.py)
│   ├── [v] M5-2. Google Trends 연동 (google_trend.py)
│   └── [v] M5-3. 트렌드 리포트 생성 (service.py + api/trend.py)
├── [v] [M6] 데스크톱 UI 통합 (desktop/)
│   ├── [v] M6-1. 메인 윈도우 및 네비게이션 (main_window.py)
│   ├── [v] M6-2. 각 탭별 UI 구현 (tab_sourcing / tab_script / tab_uploader / tab_trend)
│   └── [v] M6-3. 백엔드 연동 API 클라이언트 (client/api_client.py)
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
- [v] M6 데스크톱 UI 통합 완료
  - client/api_client.py (APIClient - 모든 백엔드 API 비동기 래핑)
  - ui/main_window.py (TubeFlowApp - 사이드바 + 4탭 + 서버 모드 전환)
  - ui/tab_sourcing.py (소재 수집 탭 - 멀티소스 수집 + 결과 목록)
  - ui/tab_script.py (대본 작성 탭 - 어조/길이 선택 + 에디터)
  - ui/tab_uploader.py (업로드 예약 탭 - 폼 + 큐 패널)
  - ui/tab_trend.py (트렌드 분석 탭 - 키워드 순위 + 통계 카드)
  - run_app.py (앱 진입점)
- [v] M5 트렌드 분석 완료
  - models.py (TrendReport, TrendKeyword, YouTubeTrendItem, GoogleTrendItem)
  - youtube_trend.py (조회수/좋아요/태그 포함 멀티 리전 수집 + 키워드 추출)
  - google_trend.py (pytrends 기반 관심도 + 연관 키워드)
  - service.py (YouTube 40% + Google 60% 가중 통합 점수, 리포트 JSON 저장)
  - api/trend.py (POST /analyze, GET /report/latest, GET /keywords 등 5개 엔드포인트)
  - backend/main.py에 trend 라우터 등록
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

**[M7-1] PyInstaller .exe 빌드** (deploy/)

---

## 작업 로그 (계속)

### 2026-05-06
- [v] 소재 수집 — RSS 수집 개수 버그 수정 및 UI 개선
  - service.py: RSS limit_per_feed를 피드 수로 나누던 버그 수정 (소스당 limit 각각 적용)
  - tab_sourcing.py: 원문 보기 버튼 위치 좌하단 → 우하단으로 변경
- [v] 소재 수집 — 번역 엔진 OpenAI GPT-4o-mini로 교체
  - translator.py: deep-translator → OpenAI GPT-4o-mini (의역 기반 자연스러운 문어체)
  - 배치 처리 15건/호출로 API 비용 최소화 (20건 기준 약 $0.002)
  - json_object 응답 포맷으로 파싱 안정성 향상
  - 번역 실패 시 원문 폴백 유지
- [v] 소재 수집 — 수집 소재 한국어 자동 번역
  - translator.py: deep-translator GoogleTranslator 기반, ThreadPoolExecutor 병렬 처리
  - 이미 한국어인 텍스트 자동 감지 (한글 비율 30% 이상 시 번역 생략)
  - models.py: Article에 title_ko / body_ko 필드 추가
  - service.py: collect() 완료 후 translate_articles() 자동 호출
  - tab_sourcing.py: 제목/본문 미리보기 번역본 우선 표시
  - requirements.txt: deep-translator==1.11.4 추가
- [v] 소재 수집 — 키워드 자동 갱신 / 체크박스 기본값 / 날짜순 정렬
  - keyword_suggester.py: pytrends 기반 트렌딩 키워드 수집, 6시간 캐시, 폴백 16개
  - GET /api/v1/sourcing/keywords/trending 엔드포인트 추가
  - service.py: 수집 결과 published_at 내림차순 정렬
  - tab_sourcing.py: 앱 시작 시 키워드 자동 로드, 갱신 버튼, 소스/시각 표시
  - 체크박스 기본값: 중국(SCMP, RFA) + 동남아(CNA, The Diplomat)만 ON
- [v] 소재 수집 탭 — 결과 카드 UI 개선
  - 본문 요약 120자 미리보기 추가
  - 원문 보기 버튼 추가 (클릭 시 기본 브라우저로 링크 오픈, webbrowser 모듈)
  - 소스명 + 날짜 한 줄 정렬 개선
- [v] M2 소재 수집 — 한국 40대+ 중장년층 대상 아시아/정치 특화 개편
  - rss_reader.py: 여행 RSS 전체 제거 → 중국/일본/동남아/국제 9개 피드로 교체
    - 중국: South China Morning Post, Radio Free Asia
    - 일본: NHK World, Nikkei Asia
    - 동남아: Channel NewsAsia, The Diplomat
    - 국제/한국: Korea Herald, Reuters Asia, BBC News Asia
  - guardian.py: travel 섹션 고정 제거 → world/politics/travel/international 복수 섹션
  - models.py: 기본 키워드 아시아 정세 중심으로 변경 (영어)
  - service.py + api/sourcing.py: 새 RSS 소스 ID 처리 로직 추가
  - tab_sourcing.py: 카테고리별 그룹 체크박스 + 소스 설명 한 줄 UI 전면 개편

### 2026-04-29
- [v] M6 코드 리뷰 및 버그 수정 완료
  - [!] 버그: 탭 간 데이터 전달 미동작 수정
    - Windows에서 `event_generate(data=)` 인자 전달 불가 문제 해결
    - `_pending_transfer` / `_pending_title` 인스턴스 변수로 우회
    - `main_window.py`에 `<<SendToScript>>` / `<<SendToUpload>>` 이벤트 바인딩 추가
    - `UploaderTab.prefill_title()` 메서드 추가
  - [v] `backend/api/uploader.py` 미사용 import 제거 (UploadFile, File, Form)
  - [v] `backend/main.py` import 순서 PEP8 정리 (상단으로 이동)
