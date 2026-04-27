import hashlib
from datetime import datetime
from pathlib import Path

from shared.utils import get_logger, save_json, load_json, timestamped_filename
from .models import UploadJob, UploadStatus, VideoMetadata
from .uploader import YouTubeUploader

logger = get_logger(__name__)
QUEUE_PATH = Path("data/upload_queue.json")


class UploadScheduler:
    def __init__(self):
        self.uploader = YouTubeUploader()
        self._queue: list[UploadJob] = []
        self._load_queue()

    def add(self, video_path: str, metadata: VideoMetadata) -> UploadJob:
        job_id = hashlib.md5(f"{video_path}{datetime.utcnow()}".encode()).hexdigest()[:12]
        job = UploadJob(id=job_id, video_path=video_path, metadata=metadata)
        self._queue.append(job)
        self._save_queue()
        logger.info("업로드 큐 추가: %s (예약: %s)", job_id, metadata.scheduled_at)
        return job

    def run_pending(self) -> list[UploadJob]:
        now = datetime.utcnow()
        done: list[UploadJob] = []
        for job in self._queue:
            if job.status != UploadStatus.pending:
                continue
            scheduled = job.metadata.scheduled_at
            if scheduled and scheduled > now:
                continue
            logger.info("업로드 실행: %s - %s", job.id, job.metadata.title)
            self.uploader.upload(job)
            done.append(job)
        self._save_queue()
        return done

    def get_queue(self) -> list[dict]:
        return [j.to_dict() for j in self._queue]

    def cancel(self, job_id: str) -> bool:
        for job in self._queue:
            if job.id == job_id and job.status == UploadStatus.pending:
                job.status = UploadStatus.failed
                job.error = "사용자 취소"
                self._save_queue()
                return True
        return False

    def _save_queue(self) -> None:
        QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
        save_json([j.to_dict() for j in self._queue], QUEUE_PATH)

    def _load_queue(self) -> None:
        if not QUEUE_PATH.exists():
            return
        try:
            raw = load_json(QUEUE_PATH)
            # 큐 복원은 pending 항목만 (완료/실패 제외)
            self._queue = []
            for item in raw:
                if item.get("status") not in ("done", "failed"):
                    meta = VideoMetadata(
                        title=item["title"],
                        description=item["description"],
                        tags=item.get("tags", []),
                        category_id=item.get("category_id", "19"),
                        thumbnail_path=item.get("thumbnail_path", ""),
                        scheduled_at=datetime.fromisoformat(item["scheduled_at"]) if item.get("scheduled_at") else None,
                    )
                    job = UploadJob(id=item["id"], video_path=item["video_path"], metadata=meta)
                    self._queue.append(job)
            logger.info("업로드 큐 복원: %d건", len(self._queue))
        except Exception as e:
            logger.warning("큐 복원 실패: %s", e)
