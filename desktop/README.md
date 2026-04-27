# desktop/ - 데스크톱 애플리케이션

## 개요

CustomTkinter 기반의 데스크톱 GUI 애플리케이션입니다.
FastAPI 백엔드와 HTTP 통신하며, PyInstaller로 .exe 단일 파일로 패키징됩니다.

## 구조

```
desktop/
  client/
    api_client.py    HTTP 클라이언트 (requests) - 모든 백엔드 API 호출 래핑
    __init__.py
  ui/
    main_window.py   메인 윈도우 + 사이드바 네비게이션 + 서버 모드 전환
    tab_sourcing.py  소재 수집 탭 (Guardian / NewsAPI / RSS / YouTube)
    tab_script.py    대본 작성 탭 (OpenAI gpt-4o)
    tab_uploader.py  업로드 예약 탭 (YouTube 큐 관리)
    tab_trend.py     트렌드 분석 탭 (YouTube + Google Trends)
    __init__.py
  __init__.py
```

## 실행 방법

```bash
# 1단계: 백엔드 서버 실행 (별도 터미널)
python -m backend.main

# 2단계: 데스크톱 앱 실행
python run_app.py
```

## 디자인 컬러 팔레트

| 토큰 | 코드 | 용도 |
|------|------|------|
| bg | #0E1014 | 최외곽 배경 |
| panel | #15181F | 사이드바, 헤더 |
| panel2 | #1B1F27 | 카드, 입력창 |
| panel3 | #22262F | 선택됨, 호버 |
| accent | #FF4655 | 주요 액션 버튼, 강조 |
| green | #3DD68C | 성공, 완료 상태 |
| amber | #F5B544 | 경고, 예약 상태 |
| blue | #5B9CFF | Guardian, Google |

## 배포 모드 전환

사이드바 하단 SERVER 토글에서 전환합니다.
- 로컬 모드: `http://127.0.0.1:8421` (기본값)
- 팀 서버 모드: `.env`의 `TEAM_SERVER_URL` 값

## 상태

- [v] 개발 완료 (M6 단계, 2026-04-27)
