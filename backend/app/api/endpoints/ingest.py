from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.document_service import document_service

router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    results = []
    for file in files:
        success = await document_service.process_upload(file)
        results.append({"filename": file.filename, "success": success})
    
    return {"message": "Processing complete", "results": results}

@router.get("/files")
async def list_files():
    # Placeholder for actual file listing from storage or DB
    return {"files": []}
