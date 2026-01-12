"""
Phase 2.5：需求格式化流水线。

职责：
- 调用 LLM
- 将自然语言需求转换为结构化 Requirement
"""

from codescope.domain.requirement import Requirement
from codescope.llm.client import LLMClient


def format_requirement(
    prompt: str,
    llm_client: LLMClient
) -> Requirement:
    """
    将用户输入格式化为 Requirement 对象。

    当前阶段：
    - 仅负责调用 LLM
    - 不做模板选择、不做推理
    """

    # TODO：后续接入 schema 校验
    response = llm_client.complete(prompt)

    # TODO：这里先假设 response 是 JSON 字符串
    # Phase 2.5 只要求流程通，不要求完美健壮
    data = eval(response)  # ⚠️ Phase 3 前需替换为安全解析

    return Requirement(
        domain=data.get("domain"),
        stage=data.get("stage"),
        core_intent=data.get("core_intent"),
        entities=data.get("entities", []),
        operations=data.get("operations", []),
        non_functional=data.get("non_functional", []),
        constraints=data.get("constraints", []),
        implicit_signals=data.get("implicit_signals", []),
    )
