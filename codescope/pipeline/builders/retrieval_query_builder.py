# retrieval_query_builder.py

"""
RetrievalQueryBuilder

职责：
- 将 SemanticTask 映射为标准化的 RetrievalQuery
- 明确“查什么、从哪查、怎么过滤”
"""

from uuid import uuid4
from typing import List

from domain.semantic import SemanticTask
from domain.retrieval import RetrievalQuery


class RetrievalQueryBuilder:
    """
    RetrievalQuery 构建器
    """

    def build(self, task: SemanticTask) -> RetrievalQuery:
        """
        SemanticTask → RetrievalQuery
        """

        query_id = f"rq-{uuid4().hex[:8]}"

        keywords: List[str] = []
        for entity in task.entities:
            keywords.append(entity.name)

        return RetrievalQuery(
            query_id=query_id,
            scope="code",
            keywords=keywords,
            entity_refs=task.entities,
            filters={
                "intent_type": task.task_type
            },
        )
