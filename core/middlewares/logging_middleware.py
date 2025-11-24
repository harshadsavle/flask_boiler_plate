import uuid
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from core.logger import info,error

class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for request logging and request ID tracking"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(("/docs", "/redoc", "/openapi.json")):
            return await call_next(request)
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Add request ID to request state
        request.state.request_id = request_id
        
        # Log request start
        start_time = time.time()
        info(
            f"Request started: {request.method} {request.url.path}",
            extra={
                'extra_fields': {
                    'request_id': request_id,
                    'method': request.method,
                    'path': request.url.path,
                    'query_params': str(request.query_params),
                    'client_ip': request.client.host if request.client else None,
                    'user_agent': request.headers.get('user-agent')
                }
            }
        )
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log request completion
            info(
                f"Request completed: {request.method} {request.url.path} - {response.status_code}",
                extra={
                    'extra_fields': {
                        'request_id': request_id,
                        'method': request.method,
                        'path': request.url.path,
                        'status_code': response.status_code,
                        'process_time_ms': round(process_time * 1000, 2)
                    }
                }
            )
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            response.headers["X-Process-Time"] = str(round(process_time * 1000, 2))
            return response
            
        except Exception as e:
            # Log request error
            process_time = time.time() - start_time
            error(
                f"Request failed: {request.method} {request.url.path}",
                extra={
                    'extra_fields': {
                        'request_id': request_id,
                        'method': request.method,
                        'path': request.url.path,
                        'error': str(e),
                        'process_time_ms': round(process_time * 1000, 2)
                    }
                },
                exc_info=True
            )
            raise

