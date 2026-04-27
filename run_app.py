"""TubeFlow 데스크톱 앱 진입점. 백엔드 서버를 먼저 실행 후 이 파일을 실행하세요."""
import sys
from pathlib import Path

# 프로젝트 루트를 sys.path에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent))

from desktop.ui.main_window import main

if __name__ == "__main__":
    main()
