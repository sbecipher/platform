from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Application-wide configuration loaded from the environment.
    All fields follow the Pydantic Settings convention: the environment
    variable name is the upper-cased version of the field name
    (e.g. LSEG_APP_KEY).
    """
    model_config = SettingsConfigDict(extra="ignore", env_file=".env", env_file_encoding="utf-8")

    # LSEG Workspace Configuration
    lseg_app_key: Optional[str] = None
    lseg_client_id: Optional[str] = None
    lseg_client_secret: Optional[str] = None
    lseg_signon_control: bool = True
    lseg_http_request_timeout_ms: int = 60000

    # API Configuration
    cors_allow_origins: str = "*"

    @property
    def cors_origins(self) -> list[str]:
        raw = self.cors_allow_origins.strip()
        if not raw:
            return []
        if raw == "*":
            return ["*"]
        return [origin.strip() for origin in raw.split(",") if origin.strip()]

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
