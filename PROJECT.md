# 유튜브 채널 운영 자동화 스위트

## 프로젝트 개요

유튜브 채널 운영에 필요한 모든 기능을 하나의 데스크톱 애플리케이션으로 통합한 자동화 도구입니다.
소재 수집, 대본 작성, 업로드 예약, 트렌드 분석 기능을 제공하며, 추후 팀원과의 공유를 위한
백엔드 서버 배포도 지원합니다.

## 핵심 기능

| 모듈 | 기능 |
|------|------|
| 소재 수집 | Reddit API 등을 통한 콘텐츠 소재 자동 수집 및 정리 |
| 대본 작성 | 수집된 소재를 바탕으로 AI 기반 대본 자동 생성 |
| 업로드 예약 | 유튜브 영상 업로드 및 예약 자동화 |
| 트렌드 분석 | YouTube/Google Trends 기반 트렌드 리포트 생성 |

## 기술 스택

| 영역 | 도구 |
|------|------|
| 데스크톱 UI | Python, CustomTkinter |
| 백엔드 API | FastAPI |
| 데이터베이스 | SQLite (로컬) / PostgreSQL (서버 배포 시) |
| 소재 수집 | PRAW (Reddit API), requests |
| 대본 작성 | Claude API (Anthropic) |
| 유튜브 연동 | YouTube Data API v3, google-api-python-client |
| 트렌드 분석 | pytrends (Google Trends), YouTube Data API |
| 패키징 | PyInstaller |
| 서버 배포 | Docker, Railway / AWS / GCP |

## 배포 방식

- **개인 사용**: 백엔드를 로컬(localhost)에서 실행 -> PyInstaller로 .exe 단일 패키지 배포
- **팀 공유**: 백엔드를 서버에 배포 -> 데스크톱 앱 설정에서 서버 주소 입력으로 전환

## 폴더 구조

```
유튜브_프로그램/
├── desktop/                 # 데스크톱 앱 (CustomTkinter GUI)
│   ├── ui/                  # 화면별 UI 컴포넌트
│   └── client/              # 백엔드 API 호출 클라이언트
├── backend/                 # FastAPI 백엔드
│   ├── api/                 # API 라우터
│   ├── core/                # 핵심 비즈니스 로직
│   │   ├── content_sourcing/
│   │   ├── script_writer/
│   │   ├── uploader/
│   │   └── trend_analyzer/
│   └── db/                  # 데이터베이스 모델
├── shared/                  # 공통 유틸리티
│   ├── auth/                # API 인증 관리
│   ├── config/              # 설정 관리
│   └── utils/               # 공통 유틸 함수
├── deploy/                  # Docker, 서버 배포 설정
├── research/                # 초기화 리서치 결과
├── references/              # 외부 참조 자료
│   └── 01-design/           # UI/UX 디자인 시안
├── docs/
│   ├── decisions/           # 설계 결정 기록 (ADR)
│   ├── specs/               # 기능 명세서
│   └── logs/                # 작업 로그
├── tests/                   # 테스트
├── PROJECT.md               # 이 파일
├── PROGRESS.md              # 작업 현황
└── CLAUDE.md                # Claude Code 지침
```

## 개발 순서

```
[D0] UI/UX 디자인 (와이어프레임)
[M1] 공통 기반 (shared/) - 인증, 설정, 로거
[M2] 소재 수집 (content_sourcing)
[M3] 대본 작성 (script_writer)
[M4] 업로드 예약 (uploader)
[M5] 트렌드 분석 (trend_analyzer)
[M6] 데스크톱 UI 통합 (desktop/)
[M7] 패키징 및 배포 (deploy/)
```

## 네이밍 규칙

- **파일명**: snake_case (예: `content_sourcing.py`)
- **클래스명**: PascalCase (예: `ContentSourcing`)
- **함수/변수명**: snake_case (예: `fetch_posts`)
- **상수**: UPPER_SNAKE_CASE (예: `MAX_RETRY_COUNT`)
- **API 라우터 prefix**: `/api/v1/[모듈명]`
- **환경변수**: UPPER_SNAKE_CASE (예: `REDDIT_CLIENT_ID`)
