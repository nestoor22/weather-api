from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.caches import RateLimitCache
from app.core.loggers import logger

__all__ = ["RateLimitMiddleware"]

RATE_LIMIT = 10
RATE_LIMIT_WINDOW = 60


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cache: RateLimitCache):
        super().__init__(app)
        self.cache = cache

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host

        current = await self.cache.increase_usage(ip)

        if current == 1:
            await self.cache.set_expiry(ip, RATE_LIMIT_WINDOW)

        if current > RATE_LIMIT:
            ttl = await self.cache.get_ttl(ip)
            logger.info(
                "Rate limit exceeded for %s",
                ip,
                extra={"current": current, "ttl": ttl},
            )
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": f"Rate limit exceeded. Try again in {ttl} seconds."
                },
            )

        return await call_next(request)
