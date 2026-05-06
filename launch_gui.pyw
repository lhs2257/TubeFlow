"""
TubeFlow 런처 (콘솔창 없이 실행).
백엔드 서버와 데스크톱 앱을 함께 시작하고,
앱 종료 시 백엔드도 자동으로 정리합니다.
"""
import os
import subprocess
import sys
import time

# 현재 스크립트 위치를 작업 디렉터리로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
os.environ["PYTHONUTF8"] = "1"

PYTHON = sys.executable
PORT = 8421


def kill_port(port: int) -> None:
    """해당 포트를 점유 중인 프로세스를 종료합니다."""
    try:
        result = subprocess.run(
            ["netstat", "-aon"],
            capture_output=True, text=True, creationflags=0x08000000
        )
        for line in result.stdout.splitlines():
            if f":{port} " in line and "LISTENING" in line:
                parts = line.strip().split()
                pid = parts[-1]
                subprocess.run(
                    ["taskkill", "/F", "/PID", pid],
                    capture_output=True, creationflags=0x08000000
                )
    except Exception:
        pass


# 기존 백엔드 프로세스 정리
kill_port(PORT)
time.sleep(1)

# 백엔드 서버 시작 (백그라운드, 창 없음)
backend = subprocess.Popen(
    [PYTHON, "-m", "uvicorn", "backend.main:app",
     "--host", "127.0.0.1", "--port", str(PORT),
     "--log-level", "warning"],
    creationflags=0x08000000,  # CREATE_NO_WINDOW
    cwd=BASE_DIR,
)

# 백엔드 준비 대기
time.sleep(4)

# 데스크톱 앱 실행 (앱이 닫힐 때까지 블로킹)
subprocess.run([PYTHON, "run_app.py"], cwd=BASE_DIR)

# 앱 종료 후 백엔드 정리
try:
    backend.terminate()
    backend.wait(timeout=5)
except Exception:
    pass
kill_port(PORT)
