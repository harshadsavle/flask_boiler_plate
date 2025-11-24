from fastapi import FastAPI
from core.middlewares.logging_middleware import LoggingMiddleware
from core.middlewares.response_formatter_middleware import ResponseFormatterMiddleware

def register_middleware(app: FastAPI):
    """
    The last middleware added is the outermost and runs first on the incoming request
    """
    app.add_middleware(ResponseFormatterMiddleware)
    app.add_middleware(LoggingMiddleware)