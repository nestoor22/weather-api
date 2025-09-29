from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.context_vars import TraceId


class TraceIdMiddleware(BaseHTTPMiddleware):
    HEADER_NAME = "x-trace-id"

    async def dispatch(self, request: Request, call_next):
        trace_id = request.headers.get(self.HEADER_NAME, str(uuid4()))
        request.state.trace_id = trace_id
        TraceId.set(trace_id)
        response = await call_next(request)
        response.headers[self.HEADER_NAME] = trace_id
        return response
