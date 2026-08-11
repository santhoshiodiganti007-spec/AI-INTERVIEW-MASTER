from fastapi import APIRouter
from pydantic import BaseModel
from app.services.rag_service import query_rag_knowledge_base

router = APIRouter(prefix="/rag", tags=["RAG Knowledge Engine"])

class RAGQueryRequest(BaseModel):
    query: str

@router.post("/query")
def query_rag(req: RAGQueryRequest):
    return query_rag_knowledge_base(req.query)
