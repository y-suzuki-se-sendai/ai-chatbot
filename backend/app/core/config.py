import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# .env ファイルから環境変数を読み込みます
load_dotenv()

class Settings(BaseSettings):
    """
    アプリケーション全体の設定（環境変数やモデル名など）を管理するクラス。
    """
    # Google API Key（Gemini LLM / Embedding 用）
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # ChromaDBのデータ保存ディレクトリ
    CHROMA_DB_DIR: str = os.getenv("CHROMA_DB_DIR", "./data/chroma")
    
    # 使用する埋め込みモデル
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"
    
    # 使用するLLMモデル
    LLM_MODEL: str = "gemini-1.5-pro"

# 設定のインスタンスを生成してエクスポート
settings = Settings()
