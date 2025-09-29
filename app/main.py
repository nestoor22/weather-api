from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import weather_api_router
from app.core.caches import RateLimitCache
from app.core.config import settings
from app.core.loggers import configure_logger, logger
from app.core.middlewares import RateLimitMiddleware, TraceIdMiddleware

configure_logger()


app = FastAPI(docs_url=settings.DOCS_URL)

app.add_middleware(RateLimitMiddleware, cache=RateLimitCache())
app.add_middleware(TraceIdMiddleware)


@app.exception_handler(RequestValidationError)
async def safe_validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = exc.errors()
    for error in errors:
        error.pop("url", None)
        if "loc" in error and len(error["loc"]) > 1:
            error["loc"] = [error["loc"][-1]]

    logger.error(
        "Validation error occurred for %s: %s",
        _request.url,
        errors,
        extra={"errors": errors},
    )
    return JSONResponse(
        status_code=422,
        content={"detail": errors},
    )


@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request, exc: Exception
) -> JSONResponse:
    logger.exception(
        "Unhandled exception: %s",
        str(exc),
        extra={
            "path": request.url.path,
            "method": request.method,
            "exception_type": exc.__class__.__name__,
        },
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Something went wrong."},
    )


@app.get("/health")
async def read_root():
    return {"message": "Weather API is up and running!"}


app.include_router(weather_api_router)
