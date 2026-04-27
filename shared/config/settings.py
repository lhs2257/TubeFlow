from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # 앱 설정
    app_env: str = Field(default="development")
    app_host: str = Field(default="127.0.0.1")
    app_port: int = Field(default=8421)
    log_level: str = Field(default="INFO")

    # Reddit API
    reddit_client_id: str = Field(default="")
    reddit_client_secret: str = Field(default="")
    reddit_user_agent: str = Field(default="TubeFlow/1.0")

    # Anthropic API
    anthropic_api_key: str = Field(default="")

    # YouTube API
    youtube_client_id: str = Field(default="")
    youtube_client_secret: str = Field(default="")
    youtube_api_key: str = Field(default="")

    # 데이터베이스
    database_url: str = Field(default="sqlite:///./tubeflow.db")

    # 팀 서버
    team_server_url: str = Field(default="")
    team_api_key: str = Field(default="")

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_team_mode(self) -> bool:
        return bool(self.team_server_url)


@lru_cache
def get_settings() -> Settings:
    return Settings()
