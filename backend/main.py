from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from shared.config import get_settings
from shared.utils import get_logger

logger = get_logger(__name__)
settings = get_settings()

app = FastAPI(
    title="TubeFlow API",
    description="유튜브 채널 운영 자동화 백엔드",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "env": settings.app_env,
        "mode": "team" if settings.is_team_mode else "local",
    }


# 라우터는 각 모듈 개발 완료 후 여기에 등록
# from backend.api import sourcing, script, uploader, trend
# app.include_router(sourcing.router, prefix="/api/v1")
# app.include_router(script.router,   prefix="/api/v1")
# app.include_router(uploader.router, prefix="/api/v1")
# app.include_router(trend.router,    prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn
    logger.info("TubeFlow 백엔드 시작 중... http://%s:%d", settings.app_host, settings.app_port)
    uvicorn.run("backend.main:app", host=settings.app_host, port=settings.app_port, reload=True)
