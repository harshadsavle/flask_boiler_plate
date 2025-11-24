import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class ResponseFormatterMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
            return await call_next(request)

        try:
            response = await call_next(request)

            # Read response body
            body = b"".join([chunk async for chunk in response.body_iterator])

            # Try parse JSON
            try:
                data = json.loads(body.decode("utf-8"))
            except Exception:
                data = body.decode("utf-8") if body else None

            if response.status_code == 200:
                return JSONResponse(
                    status_code=200,
                    content={"success": True, "data": data},
                )
            return JSONResponse(
                status_code=response.status_code,
                content={
                    "success": False,
                    "error": data if isinstance(data, str) else None,
                    "details": data if isinstance(data, dict) else None,
                },
            )

        except Exception as exc:
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "Internal Server Error",
                    "details": str(exc),
                },
            )

