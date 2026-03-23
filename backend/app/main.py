from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings
import os

# データの保存ディレクトリ（ChromaDB用など）が存在することを確認し、なければ作成します
os.makedirs(settings.CHROMA_DB_DIR, exist_ok=True)

# FastAPIアプリケーションのインスタンス化
app = FastAPI(title="AI Chatbot API")

# CORS（Cross-Origin Resource Sharing）の設定
# フロントエンドからのリクエストを許可するために必要です
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンからのリクエストを許可
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッド（GET, POSTなど）を許可
    allow_headers=["*"],  # すべてのHTTPヘッダーを許可
)

# APIルーターの登録（/api プレフィックスを付けて、エンドポイントを統合します）
app.include_router(api_router, prefix="/api")

# ルートパスへのGETリクエストに対するハンドラ
@app.get("/")
async def root():
    """
    APIの動作確認用のルートエンドポイント
    """
    return {"message": "AI Chatbot API is running"}
