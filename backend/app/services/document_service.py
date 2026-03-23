from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.services.vector_store_service import vector_store_service
import os
import tempfile

class DocumentService:
    """
    ドキュメントのロード、分割、およびベクターストアへの保存を管理するサービス。
    """
    def __init__(self):
        # テキストを適切なチャンクサイズに分割するためのスプリッターの初期化。
        # 意味のあるまとまりを維持するために overlap を設定します。
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )

    async def process_file(self, file_path: str, filename: str):
        """
        ファイルパスとファイル名に基づき、適切なローダーを選択してドキュメントを処理します。
        """
        loader = None
        # 拡張子によって異なるローダーを使用します。
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
        elif filename.endswith(".txt"):
            loader = TextLoader(file_path, encoding="utf-8")
        elif filename.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
        
        if loader:
            # ドキュメントをロード
            documents = loader.load()
            # 指定されたチャンクサイズで分割
            split_docs = self.text_splitter.split_documents(documents)
            # ベクターストアに分割されたドキュメントを追加
            vector_store_service.add_documents(split_docs)
            return True
        return False

    async def process_upload(self, upload_file):
        """
        FastAPIのアップロードファイル（UploadFileオブジェクト）を受け取り、一時ファイルに保存して処理します。
        """
        # 一時ファイルを作成してアップロード内容を書き込みます。
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{upload_file.filename}") as temp_file:
            content = await upload_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # 一時ファイルを使ってドキュメント処理を実行
            success = await self.process_file(temp_file_path, upload_file.filename)
            return success
        finally:
            # 処理完了後、一時ファイルを削除します（クリーンアップ）。
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

# シングルトンとしてインスタンスを生成。
document_service = DocumentService()
