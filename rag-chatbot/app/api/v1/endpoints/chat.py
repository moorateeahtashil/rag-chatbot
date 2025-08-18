from fastapi import APIRouter, Depends
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag_service import RAGService
from app.services.vector_db import VectorDBService

router = APIRouter()

def get_rag_service():
    vector_db_service = VectorDBService()
    return RAGService(vector_db_service=vector_db_service)

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service),
):
    """
    Chat with the RAG model.

    - **query**: The user's query.
    - **domain**: The domain to use (e.g., `default`, `medical`).
    """
    result = rag_service.get_answer(request.query, request.domain)
    return ChatResponse(answer=result["answer"], sources=result["sources"])
