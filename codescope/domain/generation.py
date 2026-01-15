from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal, Type
from enum import Enum


@dataclass
class OutputSpec:
    """
    对最终输出的结构化期望

    职责：
    - 约束“输出是什么”
    - 不关心“如何生成”
    """

    output_type: Literal[
        "text",
        "markdown",
        "json",
        "code"
    ]

    schema: Optional[Type]
    # 若为结构化输出，对应的数据模型

    quality_requirements: List[str]
    # 例："包含示例" / "逐步解释"


@dataclass
class GenerationInput:
    """
    生成阶段的标准输入边界

    职责：
    - 隔离语义执行与 Prompt / LLM
    """

    task: SemanticTask

    retrieval_result: RetrievalResult

    output_spec: OutputSpec


# =========================
# Generation Config (Prompt Layer)
# =========================

@dataclass
class GenerationConfig:
    """
    Phase 5 中的 Prompt 配置实体（非语义主干）

    职责：
    - 控制 LLM 生成方式
    - 可替换、可 A/B、可回滚
    """

    config_id: str

    system_prompt: str

    template_ref: Optional[str]

    constraints: List[str]
    # 仅限生成层约束，如格式、语气、禁止项
