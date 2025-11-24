from fastapi import UploadFile, HTTPException
from pathlib import Path
import json

class FileConstants:
    MAX_FILE_SIZE = 1024 * 1024 * 1024  # 1GB
    CHUNK_SIZE = 1024 * 1024  # 1MB chunks
    UPLOAD_DIR = "uploads"
    ALLOWED_EXTENSIONS = {".txt", ".pdf", ".doc", ".docx", ".csv", ".xlsx", ".json", ".xml", ".zip", ".tar", ".gz"}
    MAX_FILES_PER_REQUEST = 10


# Utility functions
def validate_file_extension(filename: str) -> bool:
    """Validate if file extension is allowed"""
    file_ext = Path(filename).suffix.lower()
    return file_ext in FileConstants.ALLOWED_EXTENSIONS

def validate_callback(callback: str) -> dict:
    """Validate if callback is a valid JSON string"""
    try:
        data= json.loads(callback)
        if not data.get('url'):
            raise Exception("Callback URL is required")
        return data
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid callback: {callback}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid callback: {callback} - {e}"
        )

def validate_extra(extra: str) -> dict:
    """Validate if extra is a valid JSON string"""
    try:
        return json.loads(extra)
    except:
        return {}

        
async def save_file_chunked(upload_file: UploadFile) -> tuple[str, int]:
    """Save file in chunks to handle large files efficiently"""
    file_content = bytearray()  # keeps everything in memory
    total_size = 0

    while chunk := await upload_file.read(FileConstants.CHUNK_SIZE):
        file_content.extend(chunk)
        total_size += len(chunk)

        # Check file size limit
        if total_size > FileConstants.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File size exceeds maximum limit of {FileConstants.MAX_FILE_SIZE} bytes"
            )

    return bytes(file_content),total_size  # convert to immutable bytes if needed