from typing import Dict, Any, List

KNOWLEDGE_DOCUMENTS = [
    {
        "id": "doc1",
        "title": "Google Python & Concurrency Guide",
        "content": "In CPython, the Global Interpreter Lock (GIL) enforces single-threaded bytecode execution. For I/O bound tasks, multithreading or asyncio works efficiently. For CPU-bound tasks, multiprocessing or subinterpreters are mandatory."
    },
    {
        "id": "doc2",
        "title": "Transformer Attention Mechanics",
        "content": "Self-attention computes Scaled Dot-Product Attention: Softmax(Q K^T / sqrt(d_k)) V. Scaling by sqrt(d_k) prevents vanishing gradients in softmax when vector dimension d_k is large."
    },
    {
        "id": "doc3",
        "title": "Production RAG Best Practices",
        "content": "Enterprise RAG requires Hybrid Search combining dense vector embeddings (cosine similarity) and sparse keyword retrieval (BM25) fused via Reciprocal Rank Fusion (RRF), followed by Cross-Encoder reranking."
    },
    {
        "id": "doc4",
        "title": "STAR Behavioral Framework",
        "content": "The STAR method structures responses into Situation (context), Task (goal), Action (specific technical actions taken), and Result (quantifiable metrics and lessons learned)."
    }
]

def query_rag_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Simulates semantic vector search over the knowledge base documents.
    Returns grounded context and LLM response.
    """
    query_lower = query.lower()
    matched_docs = []
    
    for doc in KNOWLEDGE_DOCUMENTS:
        words = [w for w in doc["content"].lower().split() if len(w) > 4]
        if any(w in query_lower for w in words):
            matched_docs.append(doc)

    if not matched_docs:
        matched_docs = [KNOWLEDGE_DOCUMENTS[0]]

    context_str = "\n---\n".join([f"[{d['title']}]: {d['content']}" for d in matched_docs])
    
    answer = f"Based on grounded knowledge base documents:\n\n{context_str}\n\nSummary: To excel in MNC interviews for this topic, clearly distinguish theoretical design trade-offs from real-world production execution constraints."

    return {
        "query": query,
        "retrieved_documents": matched_docs,
        "grounded_answer": answer,
        "source_count": len(matched_docs)
    }
