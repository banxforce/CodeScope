import uuid
from typing import Any, List
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from codescope.rag.base.query_compiler import QueryCompiler
from codescope.domain.semantic_models import (
    RetrievalQuery,
    RetrievalResult,
    RetrievedChunk,
)


class VectorStoreCompiler(QueryCompiler):
    """基于向量库的 QueryCompiler 实现。"""

    def __init__(self, vector_store, embed_model=None):
        """
        vector_store: VectorStore 实例，遵循 search(embedding, top_k, filters) -> List[dict]
        embed_model: 文本到向量的模型，可选
        """
        self.vector_store = vector_store
        if embed_model is None:
            self.embed_model = FastEmbedEmbeddings()
        else:
            self.embed_model = embed_model

    def _compile(self, query: RetrievalQuery) -> dict:
        filters = query.filters or {}
        return {
            "text": " ".join(query.keywords),
            "filters": filters,
            "top_k": filters.get("top_k", 5),
        }

    def _embed_text(self, text: str) -> list[float]:
        if self.embed_model is None:
            raise ValueError("需要embed_model来生成嵌入。")
        return self.embed_model.embed_documents(text)

    def execute(self, query: RetrievalQuery) -> RetrievalResult:
        compiled = self._compile(query)
        embedding = self._embed_text(compiled["text"])

        raw_hits = self.vector_store.search(
            embedding=embedding,
            top_k=compiled["top_k"],
            filters=compiled["filters"],
        )

        chunks: List[RetrievedChunk] = []
        for hit in raw_hits:
            chunks.append(
                RetrievedChunk(
                    chunk_id=hit.get("id", str(uuid.uuid4())),
                    source_id=hit["source_id"],
                    source_type=hit["source_type"],
                    content=hit["content"],
                    relevance_score=float(hit.get("score", 1.0)),
                    metadata=hit.get("metadata", {}),
                )
            )

        confidence = (
            sum(c.relevance_score for c in chunks) / len(chunks)
            if chunks else 0.0
        )

        return RetrievalResult(
            query_id=query.query_id,
            chunks=chunks,
            confidence=confidence,
            total_hits=len(raw_hits),
        )
