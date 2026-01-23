from abc import ABC, abstractmethod
from typing import List, Dict, Any
from codescope.domain.semantic_models import (
    RetrievalQuery,
    RetrievalResult,
    RetrievedChunk,
    ChunkSource,
    ChunkAnnotation
)


class VectorStore(ABC):
    """向量库抽象接口：接收 embedding、返回 dict 结果"""

    @abstractmethod
    def add_chunks(self, chunks: List["ChunkSource"]) -> None:
        """
        将 ChunkSource 写入向量库
        """
        pass

    @abstractmethod
    def search(
            self,
            embedding: List[float],
            top_k: int = 5,
            filters: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        向量检索接口
        返回 list[dict]，每个 dict 至少包含：
            - source_id
            - source_type
            - content
            - score（可选）
            - metadata（可选）
        """
        pass
