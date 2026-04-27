import threading
from typing import Any, Callable

import requests

from shared.utils import get_logger

logger = get_logger(__name__)

DEFAULT_TIMEOUT = 30


class APIError(Exception):
    def __init__(self, message: str, status_code: int = 0):
        super().__init__(message)
        self.status_code = status_code


class APIClient:
    """FastAPI 백엔드와 통신하는 HTTP 클라이언트."""

    def __init__(self, base_url: str = "http://127.0.0.1:8421"):
        self.base_url = base_url.rstrip("/")
        self._session = requests.Session()

    def set_base_url(self, url: str) -> None:
        self.base_url = url.rstrip("/")

    def health(self) -> dict:
        return self._get("/health")

    # ── 소재 수집 ──────────────────────────────────────────────────

    def collect_sources(
        self,
        keywords: list[str] | None = None,
        sources: list[str] | None = None,
        limit: int = 30,
    ) -> dict:
        payload: dict[str, Any] = {"limit": limit}
        if keywords:
            payload["keywords"] = keywords
        if sources:
            payload["sources"] = sources
        return self._post("/api/v1/sourcing/collect", payload)

    def get_sources_info(self) -> dict:
        return self._get("/api/v1/sourcing/sources")

    # ── 대본 작성 ──────────────────────────────────────────────────

    def generate_script(
        self,
        source_title: str,
        source_body: str,
        source_url: str = "",
        tone: str = "informative",
        language: str = "ko",
        target_duration_min: int = 10,
    ) -> dict:
        return self._post("/api/v1/script/generate", {
            "source_title": source_title,
            "source_body": source_body,
            "source_url": source_url,
            "tone": tone,
            "language": language,
            "target_duration_min": target_duration_min,
        })

    def get_tones(self) -> dict:
        return self._get("/api/v1/script/tones")

    # ── 업로드 예약 ────────────────────────────────────────────────

    def add_upload(
        self,
        video_path: str,
        title: str,
        description: str = "",
        tags: list[str] | None = None,
        privacy: str = "private",
        scheduled_at: str | None = None,
        thumbnail_path: str = "",
    ) -> dict:
        return self._post("/api/v1/upload/add", {
            "video_path": video_path,
            "title": title,
            "description": description,
            "tags": tags or [],
            "privacy": privacy,
            "scheduled_at": scheduled_at,
            "thumbnail_path": thumbnail_path,
        })

    def get_upload_queue(self) -> dict:
        return self._get("/api/v1/upload/queue")

    def run_pending_uploads(self) -> dict:
        return self._post("/api/v1/upload/run", {})

    def cancel_upload(self, job_id: str) -> dict:
        return self._delete(f"/api/v1/upload/cancel/{job_id}")

    # ── 트렌드 분석 ────────────────────────────────────────────────

    def analyze_trends(
        self,
        regions: list[str] | None = None,
        google_keywords: list[str] | None = None,
        timeframe: str = "now 7-d",
        yt_limit_per_region: int = 10,
    ) -> dict:
        return self._post("/api/v1/trend/analyze", {
            "regions": regions or ["US", "GB", "JP", "AU", "KR"],
            "google_keywords": google_keywords or [],
            "timeframe": timeframe,
            "yt_limit_per_region": yt_limit_per_region,
        })

    def get_latest_trend_report(self) -> dict:
        return self._get("/api/v1/trend/report/latest")

    def list_trend_reports(self) -> dict:
        return self._get("/api/v1/trend/report/list")

    def get_trend_keywords(self, top: int = 20) -> dict:
        return self._get(f"/api/v1/trend/keywords?top={top}")

    def get_supported_regions(self) -> dict:
        return self._get("/api/v1/trend/regions")

    # ── 비동기 래퍼 ────────────────────────────────────────────────

    def async_call(
        self,
        func: Callable,
        *args,
        on_success: Callable[[Any], None] | None = None,
        on_error: Callable[[str], None] | None = None,
        **kwargs,
    ) -> threading.Thread:
        """별도 스레드에서 API 호출을 실행합니다."""
        def _run():
            try:
                result = func(*args, **kwargs)
                if on_success:
                    on_success(result)
            except APIError as e:
                logger.error("API 오류: %s", e)
                if on_error:
                    on_error(str(e))
            except Exception as e:
                logger.error("예상치 못한 오류: %s", e)
                if on_error:
                    on_error(f"연결 오류: {e}")

        t = threading.Thread(target=_run, daemon=True)
        t.start()
        return t

    # ── 내부 HTTP 메서드 ───────────────────────────────────────────

    def _get(self, path: str) -> dict:
        url = self.base_url + path
        try:
            resp = self._session.get(url, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            raise APIError(f"HTTP {resp.status_code}: {resp.text[:200]}", resp.status_code) from e
        except requests.ConnectionError as e:
            raise APIError(f"서버에 연결할 수 없습니다: {self.base_url}") from e
        except requests.Timeout:
            raise APIError("요청 시간이 초과되었습니다.")

    def _post(self, path: str, data: dict) -> dict:
        url = self.base_url + path
        try:
            resp = self._session.post(url, json=data, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            raise APIError(f"HTTP {resp.status_code}: {resp.text[:200]}", resp.status_code) from e
        except requests.ConnectionError as e:
            raise APIError(f"서버에 연결할 수 없습니다: {self.base_url}") from e
        except requests.Timeout:
            raise APIError("요청 시간이 초과되었습니다.")

    def _delete(self, path: str) -> dict:
        url = self.base_url + path
        try:
            resp = self._session.delete(url, timeout=DEFAULT_TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as e:
            raise APIError(f"HTTP {resp.status_code}: {resp.text[:200]}", resp.status_code) from e
        except requests.ConnectionError as e:
            raise APIError(f"서버에 연결할 수 없습니다: {self.base_url}") from e
        except requests.Timeout:
            raise APIError("요청 시간이 초과되었습니다.")
