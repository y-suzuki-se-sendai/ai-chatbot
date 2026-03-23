from fastapi import APIRouter
from pydantic import BaseModel
from app.services.chat_service import chat_service

# APIルーターの初期化
router = APIRouter()

class ChatRequest(BaseModel):
    """
    チャットリクエストのデータ構造を定義します。
    """
    message: str          # ユーザーからのメッセージ
    history_id: str = None # 会話履歴を管理する場合のID（オプション）

@router.post("/")
async def chat(request: ChatRequest):
    """
    POST /api/chat/ エンドポイント。
    ユーザーのメッセージを受け取り、チャットサービスで回答を生成して返します。
    """
    # チャットサービスを呼び出して回答を取得
    response_data = await chat_service.get_response(request.message)
    
    # 重複するソース（参照元）を除去して返却
    return {
        "response": response_data["response"],
        "sources": list(set(response_data["sources"]))
    }
