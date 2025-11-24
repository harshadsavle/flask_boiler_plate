from fastapi import FastAPI
from api.api import api_router
from api.users import user_router
from core.exception_handlers import register_exception_handlers
from core.middlewares.middleware import register_middleware
from database import init_db
import uvicorn
from core.config import Config

app = FastAPI(
    title="FastAPI Boilerplate", 
    description="Production-ready FastAPI boilerplate with user authentication",
    version="1.0.0",
    debug=Config.DEBUG
)

# Initialize database
init_db()

# Register middleware and exception handlers
register_exception_handlers(app)
register_middleware(app)

# Include routers
app.include_router(user_router, prefix="/api")
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Boilerplate",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host=Config.HOST, port=Config.PORT)