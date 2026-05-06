@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PYTHONUTF8=1

echo.
echo  ==============================
echo   TubeFlow 시작 중...
echo  ==============================
echo.

REM 포트 8421 기존 프로세스 정리
for /f "tokens=5" %%i in ('netstat -aon 2^>nul ^| find ":8421 " ^| find "LISTENING"') do (
    taskkill /F /PID %%i >nul 2>&1
)

REM 백엔드 서버 시작 (최소화된 창)
start /min "TubeFlow-Backend" python -m uvicorn backend.main:app --host 127.0.0.1 --port 8421 --log-level warning

echo  백엔드 서버 시작 중... (잠시 대기)
timeout /t 4 /nobreak >nul

echo  앱 실행 중...
echo.

REM 앱 실행 (창이 닫힐 때까지 대기)
python run_app.py

REM 앱 종료 시 백엔드도 함께 종료
echo.
echo  TubeFlow 종료 중...
for /f "tokens=5" %%i in ('netstat -aon 2^>nul ^| find ":8421 " ^| find "LISTENING"') do (
    taskkill /F /PID %%i >nul 2>&1
)
echo  종료 완료.
timeout /t 2 /nobreak >nul
