# 작업 현황 (PROGRESS.md)

> 최종 업데이트: 2026-04-27

## 현재 단계

**[M2] 소재 수집 (content_sourcing)** - 대기중

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
│   ├── [v] M1-3. API 인증 모듈 (shared/auth/ - Reddit, YouTube, Anthropic)
│   ├── [v] M1-4. 공통 유틸리티 (shared/utils/ - 로거, 파일 처리)
│   └── [v] M1-5. 백엔드 진입점 (backend/main.py)
├── [ ] [M2] 소재 수집 (content_sourcing)
│   ├── [ ] M2-1. Reddit 소재 수집기
│   ├── [ ] M2-2. 소재 필터링 및 정리
│   └── [ ] M2-3. 소재 저장/출력 (JSON, CSV)
├── [ ] [M3] 대본 작성 (script_writer)
│   ├── [ ] M3-1. 소재 입력 -> 대본 생성 (Claude API)
│   └── [ ] M3-2. 대본 템플릿 관리
├── [ ] [M4] 업로드 예약 (uploader)
│   ├── [ ] M4-1. 영상 메타데이터 설정
│   ├── [ ] M4-2. 유튜브 업로드 자동화
│   └── [ ] M4-3. 예약 업로드 스케줄러
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
- [v] M1 공통 기반 완료
  - requirements.txt, .env.example
  - shared/config/settings.py (pydantic-settings)
  - shared/auth/ (Reddit, YouTube, Anthropic 인증)
  - shared/utils/ (로거, 파일 유틸)
  - backend/main.py (FastAPI 진입점)

---

## 다음 할 일

**[M2-1] Reddit 소재 수집기** (backend/core/content_sourcing/)
