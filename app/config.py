import socket
from typing import Literal

from pydantic_settings import BaseSettings

VERSION = "0.1.0"


def _get_local_ip() -> str:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as connection:
            connection.connect(("8.8.8.8", 80))
            return connection.getsockname()[0]
    except OSError:
        return "127.0.0.1"


class Settings(BaseSettings):
    ENVIRONMENT: Literal["development", "production"] = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    ALLOWED_ORIGINS: str = ""
    ALLOW_LOCAL_NETWORK: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001
    ROOT_PATH: str = "/api-geo"
    FORWARDED_ALLOW_IPS: str = "127.0.0.1"
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_STORAGE: str = "memory://"
    RATE_LIMIT: str = "120/minute"
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    @property
    def origins(self) -> list[str]:
        external = [o.strip() for o in self.ALLOWED_ORIGINS.split(",") if o.strip()]

        if self.ALLOW_LOCAL_NETWORK:
            local_ip = _get_local_ip()
            local = [
                "http://localhost",
                f"http://localhost:{self.PORT}",
                "http://127.0.0.1",
                f"http://127.0.0.1:{self.PORT}",
                f"http://{local_ip}",
                f"http://{local_ip}:{self.PORT}",
            ]
            return local + external

        return external

    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == "development"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
