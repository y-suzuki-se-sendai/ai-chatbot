from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_store_service import vector_store_service
import os
import tempfile

class DocumentService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    async def process_file(self, file_path: str, filename: str):
        loader = None
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        
        if loader:
            documents = loader.load()
            split_docs = self.text_splitter.split_documents(documents)
            vector_store_service.add_documents(split_docs)
            return True
        return False

    async def process_upload(self, upload_file):
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{upload_file.filename}") as temp_file:
            content = await upload_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            success = await self.process_file(temp_file_path, upload_file.filename)
            return success
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

document_service = DocumentService()
