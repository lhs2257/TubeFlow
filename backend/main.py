import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api import sourcing, script, uploader, trend
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

app.include_router(sourcing.router,  prefix="/api/v1")
app.include_router(script.router,    prefix="/api/v1")
app.include_router(uploader.router,  prefix="/api/v1")
app.include_router(trend.router,     prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "env": settings.app_env,
        "mode": "team" if settings.is_team_mode else "local",
    }


if __name__ == "__main__":
    logger.info("TubeFlow 백엔드 시작 중... http://%s:%d", settings.app_host, settings.app_port)
    uvicorn.run("backend.main:app", host=settings.app_host, port=settings.app_port, reload=True)
