from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from app.core.config import settings
import os

class VectorStoreService:
    def __init__(self):
        # API Key is automatically read from GOOGLE_API_KEY environment variable
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            client_options={"api_version": "v1beta"},
            transport="rest"
        )
        self.persist_directory = settings.CHROMA_DB_DIR
        
    def get_vector_store(self, collection_name: str = "documents"):
        return Chroma(
            collection_name=collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add_documents(self, documents, collection_name: str = "documents"):
        vector_store = self.get_vector_store(collection_name)
        vector_store.add_documents(documents)
        return vector_store

vector_store_service = VectorStoreService()
