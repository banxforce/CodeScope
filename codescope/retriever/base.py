from abc import ABC, abstractmethod
from typing import List, Any

from codescope.domain.semantic_models import RetrievalQuery, RetrievalResult


class BaseRetriever(ABC):
    """
    Retriever 抽象基类

    语义定位：
    - 输入：结构化 RetrievalQuery（由语义任务推导，而非 prompt）
    - 输出：RetrievalResult（原始外部知识 + 元信息）
    """

    @abstractmethod
    def retrieve(self, query: RetrievalQuery) -> RetrievalResult:
        """
        执行一次检索

        Args:
            query: RetrievalQuery
                - 已经完成语义建模
                - 不包含任何 prompt / LLM 指令

        Returns:
            RetrievalResult
                - 文档片段
                - score / source / metadata
        """
        raise NotImplementedError
