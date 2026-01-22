import uuid
from typing import Any, List
from query_compiler import QueryCompiler


class VectorStoreCompiler(QueryCompiler):
    """基于向量库的 QueryCompiler 实现。"""

    def __init__(self, vector_store):
        """
        vector_store: 具体向量库实例
        约定接口：
          - search(embedding, top_k, filters) -> List[dict]
        """
        self.vector_store = vector_store

    def _compile(self, query: RetrievalQuery) -> dict:
        # 非常刻意：这里只使用 RetrievalQuery 的一部分
        return {
            "text": " ".join(query.keywords),
            "filters": query.filters,
            "top_k": 5,
        }

    def execute(self, query: RetrievalQuery) -> RetrievalResult:
        compiled = self._compile(query)

        raw_hits = self.vector_store.search(
            embedding_text=compiled["text"],
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
                    relevance_score=float(hit["score"]),
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
