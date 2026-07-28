from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import settings

storage_uri = settings.RATE_LIMIT_STORAGE if settings.RATE_LIMIT_ENABLED else "memory://"

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=storage_uri,
    default_limits=[settings.RATE_LIMIT] if settings.RATE_LIMIT_ENABLED else [],
    enabled=settings.RATE_LIMIT_ENABLED,
)
