from abc import ABC, abstractmethod
from typing import List
from codescope.domain.semantic_models import (
    RetrievalQuery,
    RetrievalResult,
)


class QueryCompiler(ABC):
    """检索执行器的抽象接口（语义层边界）。"""

    @abstractmethod
    def execute(self, query: RetrievalQuery) -> RetrievalResult:
        """执行一次检索查询并返回结构化结果。"""
        raise NotImplementedError
