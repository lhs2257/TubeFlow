# desktop/ - 데스크톱 애플리케이션

## 개요

CustomTkinter 기반의 데스크톱 GUI 애플리케이션입니다.
백엔드 API와 HTTP 통신하며, PyInstaller로 .exe 단일 파일로 패키징됩니다.

## 구조

```
desktop/
├── ui/                  # 화면별 UI 컴포넌트
│   ├── main_window.py   # 메인 윈도우 및 탭 네비게이션
│   ├── tab_sourcing.py  # 소재 수집 탭
│   ├── tab_script.py    # 대본 작성 탭
│   ├── tab_uploader.py  # 업로드 예약 탭
│   └── tab_trend.py     # 트렌드 분석 탭
└── client/              # 백엔드 API 호출 클라이언트
    └── api_client.py    # HTTP 클라이언트 (requests)
```

## 실행 방법

```bash
python desktop/ui/main_window.py
```

## 배포 모드 전환

설정 화면에서 서버 주소를 변경합니다.
- 로컬 모드: `http://localhost:8000`
- 팀 서버 모드: `http://[서버IP]:8000`

## 상태

- [ ] 개발 예정 (M6 단계)
