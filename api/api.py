from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from api.api_helper import validate_file_extension, save_file_chunked, validate_callback, validate_extra
from ai_agent.init_agent import init_agent
from typing import Optional

api_router = APIRouter(
    prefix="/agent",
    tags=["Agent Data Extraction"],
)


@api_router.post("/start")
async def start_agent(
    file: UploadFile = File(..., description="File to upload"),
    callback: str = Form(..., description="Callback JSON as string"),
    jobid: str = Form(..., description="Job ID"),
    extra: Optional[str] = Form(None, description="Extra JSON as string")
):
    """
    Start a data extraction agent.
    
    - **file**: File to upload (max 1GB)
    - **callback**: Callback JSON as string
    - **jobid**: Job ID
    - **extra**: Extra JSON as string
    """
    callback = validate_callback(callback)
    extra = validate_extra(extra)
    # Validate file extension
    if not validate_file_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed: {file.filename}"
        )
    
    try:
        # Save file
        file_content, file_size = await save_file_chunked(file)
        init_agent.apply_async(args=[file_content,callback,jobid,extra],queue='data_extraction')
        # Create metadata
        return {
            "success": True,
            "message": "Agent started successfully",
            "file_size": file_size
        }
        
    except HTTPException:
        raise
    except Exception as e:
        # Clean up uploaded file on error
        
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )