from fastapi import APIRouter
from app.api.endpoints import chat, ingest

# アプリ全体のルートAPIルーター
api_router = APIRouter()

# チャットエンドポイントの登録（/api/chat/）
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])

# ドキュメント取り込み（インジェスト）エンドポイントの登録（/api/ingest/）
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
