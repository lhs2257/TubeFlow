# uploader/ - 업로드 예약 모듈

## 개요

YouTube Data API v3를 통해 영상 업로드 및 예약을 자동화합니다.

## 주요 기능

- 영상 파일 업로드 (제목, 설명, 태그, 썸네일 설정)
- 예약 업로드 (날짜/시간 지정)
- 업로드 상태 모니터링

## 인터페이스

```python
upload_video(video_path: str, metadata: VideoMetadata) -> str
schedule_upload(video_path: str, metadata: VideoMetadata, scheduled_at: datetime) -> str
get_upload_status(video_id: str) -> UploadStatus
```

## 필요 환경변수

```
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=
YOUTUBE_REFRESH_TOKEN=
```

## 상태

- [ ] 개발 예정 (M4 단계)
