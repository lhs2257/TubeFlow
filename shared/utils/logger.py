import logging
import sys
from pathlib import Path
from shared.config import get_settings


def get_logger(name: str) -> logging.Logger:
    settings = get_settings()
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 콘솔 핸들러 (Windows cp949 환경에서 UTF-8 강제 출력)
    import io
    stream = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace") \
        if hasattr(sys.stdout, "buffer") else sys.stdout
    console = logging.StreamHandler(stream)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # 파일 핸들러
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    file_handler = logging.FileHandler(log_dir / "tubeflow.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
