from pydantic_settings import BaseSettings

VERSION = "0.1.0"


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    ALLOWED_ORIGINS: str = ""
    ALLOW_LOCAL_NETWORK: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8001

    @property
    def origins(self) -> list[str]:
        external = [
            o.strip()
            for o in self.ALLOWED_ORIGINS.split(",")
            if o.strip()
        ]

        if self.ALLOW_LOCAL_NETWORK:
            local = [
                "http://localhost",
                "http://127.0.0.1",
                "http://localhost:3000",
                "http://localhost:5173",
                "http://localhost:8000",
                "http://localhost:8001",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:5173",
                "http://127.0.0.1:8000",
                "http://127.0.0.1:8001",
            ]
            return local + external

        return external

    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == "development"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
