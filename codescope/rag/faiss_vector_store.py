from langchain_community.vectorstores import FAISS
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from codescope.rag.base.vector_store import VectorStore
from codescope.domain.semantic_models import (
    RetrievalQuery,
    RetrievalResult,
    RetrievedChunk,
    ChunkSource,
    ChunkAnnotation
)
import uuid


class FAISSVectorStore(VectorStore):
    """
    FAISS 向量库实现
    约定接口：
        search(embedding_text: str, top_k: int, filters: dict | None) -> List[dict]
    """

    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model or FastEmbedEmbeddings()
        self._store = None

    # =========================
    # 构建索引阶段
    # =========================
    def add_chunks(self, chunks: list["ChunkSource"]) -> None:
        from langchain_community.docstore.document import Document
        from langchain_community.vectorstores import FAISS

        if not chunks:
            return

        docs = [
            Document(
                page_content=c.content,
                metadata={
                    "source_id": c.source_id,
                    "source_type": c.source_type,
                    **(c.metadata or {}),
                },
            )
            for c in chunks
        ]

        if self._store is None:
            self._store = FAISS.from_documents(docs, self.embedding_model)
        else:
            self._store.add_documents(docs)

    def is_ready(self) -> bool:
        return self._store is not None

    # =========================
    # 查询阶段
    # =========================
    def search(
            self,
            embedding_text: str,
            top_k: int = 5,
            filters: dict | None = None,
    ) -> list[dict]:

        if self._store is None:
            raise RuntimeError(
                "FAISSVectorStore 未初始化，请先调用 add_chunks() 构建索引"
            )

        # FAISS + LangChain：拿 score 必须用这个
        hits = self._store.similarity_search_with_score(
            embedding_text, k=top_k
        )

        results: list[dict] = []

        for doc, score in hits:
            # 简单 filters（可选）
            if filters:
                matched = True
                for k, v in filters.items():
                    if doc.metadata.get(k) != v:
                        matched = False
                        break
                if not matched:
                    continue

            results.append(
                {
                    "source_id": doc.metadata.get("source_id"),
                    "source_type": doc.metadata.get("source_type"),
                    "content": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata,
                }
            )

        return results
