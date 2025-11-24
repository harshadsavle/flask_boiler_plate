import os
from typing import Optional

class Config:
    """Application configuration"""
    
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false" if APP_ENV == "production" else "true").lower() == "true"
    # Logging configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FILE: Optional[str] = os.getenv("LOG_FILE", 'app.log')
    LOG_MAX_BYTES: int = int(os.getenv("LOG_MAX_BYTES", "10485760"))  # 10MB
    LOG_BACKUP_COUNT: int = int(os.getenv("LOG_BACKUP_COUNT", "5"))
    LOG_ENABLE_CONSOLE: bool = os.getenv("LOG_ENABLE_CONSOLE", "true").lower() == "true"
    LOG_ENABLE_FILE: bool = os.getenv("LOG_ENABLE_FILE", "true").lower() == "true"
    
    # Server configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"

    # Redis configuration
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_DB: int = int(os.getenv("REDIS_DB", "1"))
    REDIS_PASSWORD: Optional[str] = os.getenv("REDIS_PASSWORD", None)
    # Queue configuration
    MAX_WORKERS: int = int(os.getenv("MAX_WORKERS", "3"))
    QUEUE_CLEANUP_INTERVAL: int = int(os.getenv("QUEUE_CLEANUP_INTERVAL", "300"))  # 5 minutes
    
    # Job configuration
    JOB_TIMEOUT: int = int(os.getenv("JOB_TIMEOUT", "3600"))  # 1 hour
    MAX_RETRIES: int = int(os.getenv("MAX_RETRIES", "3"))
    
    @classmethod
    def get_logging_config(cls) -> dict:
        """Get logging configuration as dictionary"""
        return {
            "log_level": cls.LOG_LEVEL,
            "log_file": cls.LOG_FILE,
            "max_bytes": cls.LOG_MAX_BYTES,
            "backup_count": cls.LOG_BACKUP_COUNT,
            "enable_console": cls.LOG_ENABLE_CONSOLE,
            "enable_file": cls.LOG_ENABLE_FILE
        }

    @classmethod
    def get_redis_url(cls) -> str:
        """Get Redis URL"""
        return f"redis://{cls.REDIS_HOST}:{cls.REDIS_PORT}/{cls.REDIS_DB}"
    
   