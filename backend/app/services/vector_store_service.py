from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings
import os

class VectorStoreService:
    """
    ベクターストア（ChromaDB）へのアクセルと管理を担当するサービス。
    """
    def __init__(self):
        # Google Generative AIを用いた埋め込み（Embedding）設定
        # 埋め込みモデルを使って、テキストデータをベクトル形式に変換します。
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            client_options={"api_version": "v1beta"},
            transport="rest"
        )
        # ベクトルデータの保存先ディレクトリを設定
        self.persist_directory = settings.CHROMA_DB_DIR
        
    def get_vector_store(self, collection_name: str = "documents"):
        """
        指定されたコレクション名でベクターストア（Chroma）をインスタンス化します。
        """
        return Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add_documents(self, documents, collection_name: str = "documents"):
        """
        ベクターストアにドキュメントを追加します。
        """
        vector_store = self.get_vector_store(collection_name)
        # ドキュメントをストアに追加
        vector_store.add_documents(documents)
        return vector_store

# シングルトンとしてインスタンスを生成。
vector_store_service = VectorStoreService()
