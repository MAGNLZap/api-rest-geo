from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    ALLOWED_ORIGINS: str = ""
    ALLOW_LOCAL_NETWORK: bool = True
    PORT: int = 8000

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
                "http://localhost:*",
                "http://127.0.0.1:*",
            ]
            return local + external

        return external

    @property
    def is_dev(self) -> bool:
        return self.ENVIRONMENT == "development"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
