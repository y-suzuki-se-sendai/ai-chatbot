from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.document_service import document_service

# インジェスト用のルーター。ドキュメントのアップロードや管理を担当。
router = APIRouter()

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """
    POST /api/ingest/upload エンドポイント。
    複数のファイルを受け取り、ドキュメントサービスで処理（分割・保存）します。
    """
    results = []
    # 各ファイルをループして順番に処理
    for file in files:
        # ドキュメントサービスで処理（一時保存、ロード、分割、ベクターストア保存）を実行
        success = await document_service.process_upload(file)
        results.append({"filename": file.filename, "success": success})
    
    return {"message": "Processing complete", "results": results}

@router.get("/files")
async def list_files():
    """
    GET /api/ingest/files エンドポイント（現在はプレースホルダ）。
    処理済みのファイル一覧を返す想定です。
    """
    return {"files": []}
