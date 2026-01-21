from typing import List, Dict, Any
from codescope.domain.semantic_models import (
    SemanticTask,
    RetrievalQuery,
)

class RetrievalQueryBuilder:
    """
    将 SemanticTask 映射为 RetrievalQuery 的构建器。

    设计原则：
    1. 完全确定性（deterministic）
    2. 不依赖 LLM
    3. 规则可冻结、可回放
    """

    TASK_SCOPE_MAP = {
        "code_search": "code",
        "doc_query": "doc",
        "analysis": "doc",
        "design": "doc",
        "explanation": "doc",
    }

    def build_all(self, tasks: List[SemanticTask]) -> List[RetrievalQuery]:
        queries: List[RetrievalQuery] = []
        for task in tasks:
            queries.append(self.build(task))
        return queries

    def build(self, task: SemanticTask) -> RetrievalQuery:
        scope = self._resolve_scope(task)
        keywords = self._build_keywords(task)
        filters = self._build_filters(task)

        return RetrievalQuery(
            query_id=task.task_id,
            scope=scope,
            keywords=keywords,
            entity_refs=task.entities,
            filters=filters,
        )

    # =========================
    # 内部规则方法
    # =========================

    def _resolve_scope(self, task: SemanticTask) -> str:
        try:
            return self.TASK_SCOPE_MAP[task.task_type]
        except KeyError:
            raise ValueError(f"未知 task_type，无法生成 RetrievalQuery: {task.task_type}")

    def _build_keywords(self, task: SemanticTask) -> List[str]:
        keywords: List[str] = []

        # 1. 实体名
        for e in task.entities:
            if e.name:
                keywords.append(e.name)

        # 2. 操作动作
        for op in task.operations:
            if op.action:
                keywords.append(op.action)

        # 3. intent 原文（v1 不拆词）
        if task.intent:
            keywords.append(task.intent)

        # 去重但保序
        return list(dict.fromkeys(keywords))

    def _build_filters(self, task: SemanticTask) -> Dict[str, Any]:
        hard_constraints = [
            c.rule for c in task.constraints if c.level == "hard"
        ]

        if not hard_constraints:
            return {}

        return {
            "constraint": hard_constraints
        }
