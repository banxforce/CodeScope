from typing import List, Dict, Any, Optional, Literal
from codescope.domain.semantic_models import (
    SemanticTask,
    RetrievalQuery,
)


class RetrievalQueryBuilder:

    def build(self, tasks: List[SemanticTask]) -> List[RetrievalQuery]:
        queries: List[RetrievalQuery] = []

        for task in tasks:
            query = self._build_from_task(task)
            if query:
                queries.append(query)

        return queries

    # 单 task 构建逻辑
    def _build_from_task(self, task: SemanticTask) -> Optional[RetrievalQuery]:
        # 1. 只要出现 search/read 操作，就认为是可检索任务
        retrieval_ops = [
            op for op in task.operations
            if op.action in ("search", "read")
        ]

        if not retrieval_ops:
            return None

        return RetrievalQuery(
            query_id=f"rq_{task.task_id}",
            scope=self._infer_scope(task),
            keywords=self._extract_keywords(task),
            entity_refs=task.entities,
            filters=self._build_filters(task),
        )

    # scope 推断（集中策略）
    def _infer_scope(self, task: SemanticTask) -> Literal["code", "doc", "api"]:
        for entity in task.entities:
            if entity.entity_type in ("class", "function", "module"):
                return "code"
            if entity.entity_type == "api":
                return "api"
        return "doc"

    # keywords 抽取（语义信号集中）
    def _extract_keywords(self, task: SemanticTask) -> List[str]:
        keywords = []

        keywords.extend(task.intent.split())
        keywords.extend(
            e.name for e in task.entities
        )
        keywords.extend(
            op.action for op in task.operations
        )

        return list(dict.fromkeys(keywords))  # 去重保序

    # filters 构建（给未来升级留口子）
    def _build_filters(self, task: SemanticTask) -> Dict[str, Any]:
        filters: Dict[str, Any] = {}

        if task.task_type:
            filters["task_type"] = task.task_type

        if task.constraints:
            filters["constraints"] = [
                c.rule for c in task.constraints
                if c.level == "hard"
            ]

        return filters
