from uuid import uuid4
from typing import List

from codescope.domain.intent_analysis import IntentAnalysis
from codescope.domain.semantic_models import (
    SemanticTask,
    EntityRef,
    Operation,
    Constraint,
    OutputSpec,
)

class SemanticTaskBuilder:
    """
    Phase 5 SemanticTask 构建器（最终版）

    设计原则：
    - 严格消费 IntentAnalysis，不引入新语义
    - 不进行二次推理，不调用 LLM
    - 所有语义折叠规则显式、可测试
    """

    def build(self, intent: IntentAnalysis) -> SemanticTask:
        """
        IntentAnalysis → SemanticTask
        """

        task_id = f"task-{uuid4().hex[:8]}"

        # 主意图直接映射
        task_intent = intent.primary_intent

        # Phase 5 任务类型规则化映射（保守、可预测）
        task_type = "analysis"
        if intent.complexity_level in ("low", "medium"):
            task_type = "explanation"
        if intent.complexity_level in ("high", "very_high"):
            task_type = "analysis"

        # Phase 5 不主动生成领域实体
        entities: List[EntityRef] = []

        # secondary_intents → 补充操作
        operations: List[Operation] = [
            Operation(
                action="generate",
                target_entity=None,
                parameters={
                    "intent": intent.primary_intent
                },
            )
        ]

        for sec in intent.secondary_intents:
            operations.append(
                Operation(
                    action="supplement",
                    target_entity=None,
                    parameters={"intent": sec},
                )
            )

        # risks → soft constraints
        constraints: List[Constraint] = [
            Constraint(rule=risk, level="soft")
            for risk in intent.risks
        ]

        # assumptions → assumption constraints（不丢失语义）
        constraints.extend(
            Constraint(rule=assumption, level="assumption")
            for assumption in intent.assumptions
        )

        # 输出规范折叠
        output_spec = OutputSpec(
            output_type="text",
            schema=None,
            quality_requirements=[
                f"复杂度等级: {intent.complexity_level}",
                *intent.key_decisions,
            ],
        )

        return SemanticTask(
            task_id=task_id,
            intent=task_intent,
            task_type=task_type,
            entities=entities,
            operations=operations,
            constraints=constraints,
            output_spec=output_spec,
        )