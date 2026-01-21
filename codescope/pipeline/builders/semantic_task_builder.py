from uuid import uuid4
from typing import List,Dict, Any

from codescope.domain.intent_analysis import IntentAnalysis
from codescope.domain.semantic_models import (
    SemanticTask,
    EntityRef,
    Operation,
    Constraint,
    OutputSpec,
)
from codescope.llm.client import LLMClient
from codescope.prompt.semantic_task_prompt import SEMANTIC_TASK_PROMPT_CN
import json


class SemanticTaskBuilder:
    """
    将 IntentAnalysis 转换为 SemanticTask 列表的构建器。

    设计目标：
    1. SemanticTask 的生成完全由 LLM 决定
    2. Builder 只负责 Prompt 组装、调用、解析与强校验
    3. 失败时可进行一次 JSON 修复重试
    """

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def build(self, intent: IntentAnalysis) -> List[SemanticTask]:
        prompt = self._build_prompt(intent)

        output = self.llm.complete(
            system_prompt=SEMANTIC_TASK_PROMPT_CN,
            user_prompt=prompt,
            temperature=0.0,
        )

        try:
            return self._parse_output(output)
        except Exception as e:
            logger.warning("SemanticTask 返回解析失败，尝试进行 JSON 修复重试: %s", e)

            retry_output = self.llm.complete(
                system_prompt=SEMANTIC_TASK_PROMPT_CN
                              + "\n\n之前的输出是无效的 JSON。请仅返回一个严格符合 SemanticTask 结构的有效 JSON 数组。",
                user_prompt=prompt,
                temperature=0.0,
            )
            try:
                return self._parse_output(retry_output)
            except Exception as e:
                logger.error("SemanticTask 返回解析又又又失败了，我没招了")

    # =========================
    # Prompt 构建
    # =========================

    def _build_prompt(self, intent: IntentAnalysis) -> str:
        return f"""
输入 IntentAnalysis 如下：

{self._intent_to_json(intent)}

请根据以上 IntentAnalysis，
构建一个或多个 SemanticTask，
并仅以 JSON 数组形式返回结果。
"""

    def _intent_to_json(self, intent: IntentAnalysis) -> str:
        return json.dumps(
            {
                "primary_intent": intent.primary_intent,
                "secondary_intents": intent.secondary_intents,
                "complexity_level": intent.complexity_level,
                "key_decisions": intent.key_decisions,
                "risks": intent.risks,
                "assumptions": intent.assumptions,
            },
            ensure_ascii=False,
            indent=2,
        )

    # =========================
    # 输出解析（强结构校验）
    # =========================

    def _parse_output(self, output: str) -> List[SemanticTask]:
        data = json.loads(output)
        if not isinstance(data, list):
            raise ValueError("SemanticTask 输出必须是 JSON 数组")

        tasks: List[SemanticTask] = []
        for item in data:
            tasks.append(self._parse_task(item))

        return tasks

    def _parse_task(self, data: Dict[str, Any]) -> SemanticTask:
        entities = [
            EntityRef(
                entity_type=e["entity_type"],
                name=e["name"],
                identifiers=e.get("identifiers", {}),
            )
            for e in data.get("entities", [])
        ]

        operations = [
            Operation(
                action=o["action"],
                target_entity=o.get("target_entity"),
                parameters=o.get("parameters", {}),
            )
            for o in data.get("operations", [])
        ]

        constraints = [
            Constraint(
                rule=c["rule"],
                level=c["level"],
            )
            for c in data.get("constraints", [])
        ]

        output_spec_data = data["output_spec"]
        output_spec = OutputSpec(
            output_type=output_spec_data["output_type"],
            schema=None,
            quality_requirements=output_spec_data.get("quality_requirements", []),
        )

        return SemanticTask(
            task_id=data["task_id"],
            intent=data["intent"],
            task_type=data["task_type"],
            entities=entities,
            operations=operations,
            constraints=constraints,
            output_spec=output_spec,
        )
