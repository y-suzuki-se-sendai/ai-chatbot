from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from app.core.config import settings
from app.services.vector_store_service import vector_store_service

class ChatService:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-3-flash-preview",
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2,
            version="v1alpha"
        )

        # 2. Embeddingの設定（ここで v1 を指定するのが重要！）
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=settings.GOOGLE_API_KEY,
        )
        self.vector_store = vector_store_service.get_vector_store()
        self.retriever = self.vector_store.as_retriever()
        
        system_prompt = (
            "You are an assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, just say that you don't know. "
            "Use three sentences maximum and keep the answer concise."
            "\n\n"
            "{context}"
        )
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )
        
        self.question_answer_chain = create_stuff_documents_chain(self.llm, self.prompt)
        self.rag_chain = create_retrieval_chain(self.retriever, self.question_answer_chain)

    async def get_response(self, user_message: str):
        response = self.rag_chain.invoke({"input": user_message})
        return {
            "response": response["answer"],
            "sources": [doc.metadata.get("source", "unknown") for doc in response["context"]]
        }

chat_service = ChatService()
