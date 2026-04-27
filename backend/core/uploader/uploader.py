import hashlib
from datetime import datetime, timezone
from pathlib import Path

from googleapiclient.http import MediaFileUpload

from shared.auth import get_youtube_client
from shared.utils import get_logger
from .models import UploadJob, UploadStatus, VideoMetadata

logger = get_logger(__name__)

CHUNK_SIZE = 256 * 1024 * 10  # 2.5MB


class YouTubeUploader:
    def __init__(self):
        self._client = None

    @property
    def client(self):
        if self._client is None:
            self._client = get_youtube_client()
        return self._client

    def upload(self, job: UploadJob) -> UploadJob:
        video_path = Path(job.video_path)
        if not video_path.exists():
            job.status = UploadStatus.failed
            job.error = f"파일 없음: {job.video_path}"
            return job

        try:
            job.status = UploadStatus.uploading
            body = self._build_body(job.metadata)
            media = MediaFileUpload(str(video_path), chunksize=CHUNK_SIZE, resumable=True)

            request = self.client.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media,
            )

            response = None
            while response is None:
                _, response = request.next_chunk()
                if response:
                    logger.info("업로드 완료: %s", response.get("id"))

            job.video_id  = response.get("id", "")
            job.video_url = f"https://www.youtube.com/watch?v={job.video_id}"
            job.status    = UploadStatus.done
            job.uploaded_at = datetime.utcnow()

            if job.metadata.thumbnail_path:
                self._set_thumbnail(job.video_id, job.metadata.thumbnail_path)

        except Exception as e:
            job.status = UploadStatus.failed
            job.error  = str(e)
            logger.error("업로드 실패: %s", e)

        return job

    def get_status(self, video_id: str) -> dict:
        try:
            resp = self.client.videos().list(part="status,processingDetails", id=video_id).execute()
            items = resp.get("items", [])
            if not items:
                return {"video_id": video_id, "status": "not_found"}
            item = items[0]
            return {
                "video_id": video_id,
                "upload_status": item["status"].get("uploadStatus"),
                "privacy_status": item["status"].get("privacyStatus"),
                "processing_status": item.get("processingDetails", {}).get("processingStatus"),
            }
        except Exception as e:
            logger.warning("상태 조회 실패: %s", e)
            return {"video_id": video_id, "error": str(e)}

    def _build_body(self, meta: VideoMetadata) -> dict:
        body = {
            "snippet": {
                "title":       meta.title,
                "description": meta.description,
                "tags":        meta.tags,
                "categoryId":  meta.category_id,
            },
            "status": {
                "privacyStatus": meta.privacy.value,
            },
        }
        if meta.scheduled_at:
            # 예약 업로드는 private -> publishAt 조합으로 설정
            body["status"]["privacyStatus"] = "private"
            body["status"]["publishAt"] = meta.scheduled_at.astimezone(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S.000Z"
            )
        return body

    def _set_thumbnail(self, video_id: str, thumbnail_path: str) -> None:
        path = Path(thumbnail_path)
        if not path.exists():
            logger.warning("썸네일 파일 없음: %s", thumbnail_path)
            return
        try:
            self.client.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(path)),
            ).execute()
            logger.info("썸네일 설정 완료: %s", video_id)
        except Exception as e:
            logger.warning("썸네일 설정 실패: %s", e)
