from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal
from urllib.parse import urlsplit, urlunsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from pydantic import AliasChoices, AnyHttpUrl, Field, SecretStr, TypeAdapter, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


_HTTP_URL_ADAPTER = TypeAdapter(AnyHttpUrl)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    web_mode: bool = Field(default=False, validation_alias=AliasChoices("ENERGY_WEB_MODE", "WEB_MODE", "web_mode"))
    web_origin: str = "https://energy.viyao.cn"
    web_max_pdf_pages: int = Field(default=100, ge=1)
    web_user_storage_mb: int = Field(default=200, ge=1)
    web_model_concurrency: int = Field(default=2, ge=1)
    web_task_queue_limit: int = Field(default=20, ge=1)
    web_model_call_reserve_cny: float = Field(default=0, ge=0, allow_inf_nan=False)
    web_embedding_call_reserve_cny: float = Field(default=0, ge=0, allow_inf_nan=False)
    web_user_daily_budget_cny: float = Field(default=5, ge=0, allow_inf_nan=False)
    web_user_monthly_budget_cny: float = Field(default=50, ge=0, allow_inf_nan=False)
    web_model_queue_timeout_seconds: float = Field(default=30, gt=0, allow_inf_nan=False)
    auth_admin_email: str = ""
    auth_code_secret: SecretStr = Field(default_factory=lambda: SecretStr(""), repr=False)
    auth_code_ttl_seconds: int = Field(default=600, ge=1)
    auth_code_resend_seconds: int = Field(default=60, ge=1)
    auth_code_hourly_limit: int = Field(default=10, ge=1)
    auth_client_hourly_limit: int = Field(default=30, ge=1)
    auth_trust_proxy: bool = False
    auth_code_max_attempts: int = Field(default=5, ge=1)
    auth_session_days: int = Field(default=7, ge=1)
    auth_smtp_host: str = ""
    auth_smtp_port: int = Field(default=587, ge=1, le=65535)
    auth_smtp_username: str = ""
    auth_smtp_password: SecretStr = Field(default_factory=lambda: SecretStr(""), repr=False)
    auth_smtp_from: str = ""
    auth_smtp_ssl: bool = False
    auth_smtp_starttls: bool = True
    database_url: str = "sqlite:///./data/energy_copilot.db"
    paper_storage_path: str = "./data/papers"
    document_ai_model_path: str = ""
    whisper_model_path: str = ""
    model_provider: str = "mock"
    model_name: str = "mock-energy-research-v1"
    model_vision_model: str = ""
    model_api_key: str = ""
    model_base_url: str = "https://api.openai.com/v1"
    model_timeout_seconds: int = 60
    max_upload_size_mb: int = Field(default=30, validation_alias=AliasChoices("MAX_UPLOAD_MB", "MAX_UPLOAD_SIZE_MB"))
    paper_budget: float = Field(default=1.0, validation_alias=AliasChoices("PAPER_BUDGET_CNY", "PAPER_BUDGET"))
    daily_budget: float = Field(default=5.0, validation_alias=AliasChoices("DAILY_BUDGET_CNY", "DAILY_BUDGET"))
    monthly_budget: float = Field(default=50.0, validation_alias=AliasChoices("MONTHLY_BUDGET_CNY", "MONTHLY_BUDGET"))
    daily_task_time: str = "08:00"
    user_timezone: str = "Asia/Shanghai"
    openalex_enabled: bool = True
    openalex_base_url: str = "https://api.openalex.org"
    crossref_enabled: bool = True
    crossref_base_url: str = "https://api.crossref.org"
    crossref_mailto: str = ""
    arxiv_enabled: bool = True
    arxiv_base_url: str = "https://export.arxiv.org/api"
    semantic_scholar_enabled: bool = False
    semantic_scholar_base_url: str = "https://api.semanticscholar.org"
    semantic_scholar_api_key: SecretStr = Field(
        default_factory=lambda: SecretStr(""),
        repr=False,
    )
    paper_source_timeout_seconds: int = Field(default=15, ge=1, le=120)
    paper_download_timeout_seconds: int = Field(default=30, ge=1, le=600)
    paper_download_max_mb: int = Field(default=50, ge=1, le=1000)
    embedding_provider: str = "ollama"
    embedding_model: str = "bge-m3"
    embedding_base_url: str = "http://host.docker.internal:11434"
    embedding_api_key: SecretStr = Field(default_factory=lambda: SecretStr(""), repr=False)
    embedding_timeout_seconds: int = Field(default=120, ge=5, le=600)
    knowledge_chunk_size: int = Field(default=1600, ge=500, le=4000)
    knowledge_chunk_overlap: int = Field(default=180, ge=0, le=800)
    redis_url: str = ""
    rq_queue_name: str = "energy-research"
    storage_backend: Literal["local", "s3"] = "local"
    s3_endpoint_url: str = ""
    s3_bucket: str = ""
    s3_region: str = "us-east-1"
    s3_access_key: SecretStr = Field(default_factory=lambda: SecretStr(""), repr=False)
    s3_secret_key: SecretStr = Field(default_factory=lambda: SecretStr(""), repr=False)
    backup_path: str = ""
    backup_retention: int = Field(default=7, ge=1, le=365)
    backup_interval_hours: int = Field(default=24, ge=1, le=720)

    @field_validator("user_timezone")
    @classmethod
    def validate_user_timezone(cls, value: str) -> str:
        candidate = value.strip()
        try:
            ZoneInfo(candidate)
        except (ValueError, ZoneInfoNotFoundError) as exc:
            raise ValueError("user timezone must be a valid IANA timezone") from exc
        return candidate

    @field_validator(
        "openalex_base_url",
        "crossref_base_url",
        "arxiv_base_url",
        "semantic_scholar_base_url",
        "embedding_base_url",
        mode="before",
    )
    @classmethod
    def validate_paper_source_base_url(cls, value: object) -> str:
        if not isinstance(value, str) or not (candidate := value.strip()):
            raise ValueError("paper source base URL must be a nonempty HTTP(S) URL")
        _HTTP_URL_ADAPTER.validate_python(candidate)
        parsed = urlsplit(candidate)
        if parsed.username is not None or parsed.password is not None:
            raise ValueError("paper source base URL must not contain credentials")
        if parsed.query or parsed.fragment:
            raise ValueError(
                "paper source base URL must not contain query or fragment"
            )
        return urlunsplit(
            (
                parsed.scheme,
                parsed.netloc,
                parsed.path.rstrip("/"),
                "",
                "",
            )
        )

    @property
    def paper_storage_dir(self) -> Path:
        root = Path(self.paper_storage_path).resolve()
        if self.web_mode:
            from app.ownership import current_user_id

            user_id = current_user_id.get()
            if user_id is not None:
                return root / "users" / str(user_id) / "papers"
        return root

    @property
    def document_ai_model_dir(self) -> Path:
        return Path(self.document_ai_model_path).resolve() if self.document_ai_model_path.strip() else self.paper_storage_dir.parent / "document-ai-models"

    @property
    def whisper_model_dir(self) -> Path:
        return Path(self.whisper_model_path).resolve() if self.whisper_model_path.strip() else self.paper_storage_dir.parent / "models" / "faster-whisper-small"

    @property
    def backup_dir(self) -> Path:
        return Path(self.backup_path).resolve() if self.backup_path.strip() else self.paper_storage_dir.parent / "backups"


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
