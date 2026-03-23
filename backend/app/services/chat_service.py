from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.services.vector_store_service import vector_store_service

class ChatService:
    """
    チャットボットのメインロジックを管理するサービス。
    LangChainを使用してRAG（検索拡張生成）のパイプラインを構築します。
    """
    def __init__(self):
        # Gemini-3 LLMの初期化
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2,
            version="v1alpha"
        )

        # 埋め込みモデル（Embedding）の初期化。テキストをベクトル形式に変換します。
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.GOOGLE_API_KEY,
        )
        
        # ベクターストアの取得。過去にインジェストしたドキュメントが含まれています。
        self.vector_store = vector_store_service.get_vector_store()
        
        # 検索機（Retriever）の設定。ユーザーの質問に関連する情報を検索します。
        self.retriever = self.vector_store.as_retriever()
        
        # システムプロンプトの設定。モデルの役割と回答の仕方を指示します。
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "Use three sentences maximum and keep the answer concise."
            "\n\n"
            "{context}"
        )
        
        # プロンプトテンプレートの定義。システムメッセージとユーザーの入力を組み合わせます。
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        
        # ドキュメントを統合してLLMに渡すチェーン（Stuff Documents Chain）を作成します。
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        
        # 検索結果を元に回答を生成するRAG（Retrieval-Augmented Generation）チェーンを構成します。
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    async def get_response(self, user_message: str):
        """
        ユーザーのメッセージに対して、関連する情報を検索し、LLMで回答を生成します。
        """
        # RAGチェーンの実行
        response = self.rag_chain.invoke({"input": user_message})
        
        # 回答と、参考にしたドキュメントのソースを返します。
        return {
            "response": response["answer"],
            "sources": [doc.metadata.get("source", "unknown") for doc in response["context"]]
        }

# シングルトンとしてインスタンスを生成。他のモジュールで共有されます。
chat_service = ChatService()
