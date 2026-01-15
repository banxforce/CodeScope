"""
SemanticTaskBuilder

职责：
- 将 IntentAnalysis 转换为系统级语义中间表示 SemanticTask
- 承担“语义决策”的最终落点
- 允许内部使用 LLM，但对外必须是确定性结构输出
"""

from uuid import uuid4
from typing import List

from domain.intent_analysis import IntentAnalysis
from domain.semantic import (
    SemanticTask,
    EntityRef,
    Operation,
    Constraint,
    OutputSpec,
)


class SemanticTaskBuilder:
    """
    SemanticTask 构建器

    设计约束：
    - 不返回 Prompt
    - 不做检索
    - 不做生成
    """

    def build(self, intent: IntentAnalysis) -> SemanticTask:
        """
        IntentAnalysis → SemanticTask
        """

        # 以下逻辑在 Phase 5 可先规则化
        # 后续允许替换为 LLM / 混合策略

        task_id = f"task-{uuid4().hex[:8]}"

        entities: List[EntityRef] = [
            EntityRef(
                entity_type="concept",
                name=e,
                identifiers={}
            )
            for e in intent.entities
        ]

        operations: List[Operation] = [
            Operation(
                action="analyze",
                target_entity=None,
                parameters={}
            )
        ]

        constraints: List[Constraint] = [
            Constraint(rule=r, level="soft")
            for r in intent.constraints
        ]

        output_spec = OutputSpec(
            output_type="text",
            schema=None,
            quality_requirements=intent.output_expectations,
        )

        return SemanticTask(
            task_id=task_id,
            task_type=intent.task_type,
            intent=intent.intent_summary,
            entities=entities,
            operations=operations,
            constraints=constraints,
            output_spec=output_spec,
        )
