import uuid
from typing import Any, List
from codescope.rag.base.query_compiler import QueryCompiler
from codescope.domain.semantic_models import (
    RetrievalQuery,
    RetrievalResult,
    RetrievedChunk,
)


class InMemoryQueryCompiler(QueryCompiler):
    """用于测试 / Dry Run 的内存检索实现。"""

    def __init__(self, chunks: List[RetrievedChunk]):
        self._chunks = chunks

    def execute(self, query: RetrievalQuery) -> RetrievalResult:
        matched: List[RetrievedChunk] = []

        for chunk in self._chunks:
            if any(
                    kw.lower() in chunk.content.lower()
                    for kw in query.keywords
            ):
                matched.append(chunk)

        confidence = (
            sum(c.relevance_score for c in matched) / len(matched)
            if matched else 0.0
        )

        return RetrievalResult(
            query_id=query.query_id,
            chunks=matched,
            confidence=confidence,
            total_hits=len(matched),
        )
