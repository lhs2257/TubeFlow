from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.core.uploader import VideoMetadata, PrivacyStatus, UploadScheduler

router = APIRouter(prefix="/upload", tags=["업로드 예약"])
_scheduler = UploadScheduler()


class UploadRequest(BaseModel):
    video_path: str = Field(..., examples=["C:/videos/travel_bali.mp4"])
    title: str = Field(..., examples=["발리 여행의 충격적인 진실 - 현지인도 몰랐던 사실"])
    description: str = Field(default="")
    tags: list[str] = Field(default_factory=list)
    category_id: str = Field(default="19")
    privacy: PrivacyStatus = Field(default=PrivacyStatus.private)
    thumbnail_path: str = Field(default="")
    scheduled_at: datetime | None = Field(default=None)


class UploadResponse(BaseModel):
    id: str
    title: str
    status: str
    scheduled_at: str | None
    video_url: str


@router.post("/add", response_model=UploadResponse)
async def add_to_queue(req: UploadRequest):
    metadata = VideoMetadata(
        title=req.title,
        description=req.description,
        tags=req.tags,
        category_id=req.category_id,
        privacy=req.privacy,
        thumbnail_path=req.thumbnail_path,
        scheduled_at=req.scheduled_at,
    )
    job = _scheduler.add(req.video_path, metadata)
    return UploadResponse(
        id=job.id,
        title=job.metadata.title,
        status=job.status.value,
        scheduled_at=job.metadata.scheduled_at.isoformat() if job.metadata.scheduled_at else None,
        video_url=job.video_url,
    )


@router.post("/run")
async def run_pending():
    done = _scheduler.run_pending()
    return {
        "processed": len(done),
        "results": [j.to_dict() for j in done],
    }


@router.get("/queue")
async def get_queue():
    return {"queue": _scheduler.get_queue()}


@router.delete("/cancel/{job_id}")
async def cancel_job(job_id: str):
    success = _scheduler.cancel(job_id)
    if not success:
        raise HTTPException(status_code=404, detail="취소할 수 없는 작업입니다.")
    return {"message": f"{job_id} 취소 완료"}


@router.get("/status/{video_id}")
async def get_video_status(video_id: str):
    uploader = _scheduler.uploader
    return uploader.get_status(video_id)
