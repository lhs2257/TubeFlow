from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class PrivacyStatus(str, Enum):
    public   = "public"
    unlisted = "unlisted"
    private  = "private"


class UploadStatus(str, Enum):
    pending    = "pending"
    uploading  = "uploading"
    processing = "processing"
    done       = "done"
    failed     = "failed"


@dataclass
class VideoMetadata:
    title: str
    description: str
    tags: list[str] = field(default_factory=list)
    category_id: str = "19"          # 19 = 여행 & 이벤트
    privacy: PrivacyStatus = PrivacyStatus.private
    thumbnail_path: str = ""
    scheduled_at: datetime | None = None   # None = 즉시 업로드


@dataclass
class UploadJob:
    id: str
    video_path: str
    metadata: VideoMetadata
    status: UploadStatus = UploadStatus.pending
    video_id: str = ""
    video_url: str = ""
    error: str = ""
    created_at: datetime = field(default_factory=datetime.utcnow)
    uploaded_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "video_path": self.video_path,
            "title": self.metadata.title,
            "description": self.metadata.description,
            "tags": self.metadata.tags,
            "category_id": self.metadata.category_id,
            "privacy": self.metadata.privacy.value,
            "scheduled_at": self.metadata.scheduled_at.isoformat() if self.metadata.scheduled_at else None,
            "status": self.status.value,
            "video_id": self.video_id,
            "video_url": self.video_url,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
            "uploaded_at": self.uploaded_at.isoformat() if self.uploaded_at else None,
        }
