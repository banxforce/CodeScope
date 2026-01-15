from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal, Type
from enum import Enum
from codescope.domain.generation import OutputSpec


@dataclass
class SemanticTask:
    """
    Phase 5 的核心语义中间表示（IR）

    职责：
    - 承载“系统级语义决策”的最终结果
    - 与 LLM / Prompt 解耦
    - 作为后续检索、执行、生成的唯一语义依据
    """

    task_id: str

    task_type: Literal[
        "code_search",
        "doc_query",
        "design",
        "analysis",
        "explanation"
    ]
    # 系统可识别的任务类型（而非自然语言）

    intent: str
    # 去 Prompt 化的一句话任务意图
    # 例："查找用户鉴权相关的代码实现并解释其设计"

    entities: List["EntityRef"]
    # 本任务涉及的核心语义实体

    operations: List["Operation"]
    # 对实体施加的操作
    # 例：read / analyze / compare

    constraints: List["Constraint"]
    # 语义层约束（与生成风格无关）

    output_spec: "OutputSpec"
    # 对最终输出“是什么”的结构性描述


# =========================
# Semantic Components
# =========================

@dataclass
class EntityRef:
    """
    对现实对象的稳定语义引用

    职责：
    - 统一代码 / 文档 / 模块 / 概念的引用方式
    - 为检索与工具提供定位锚点
    """

    entity_type: Literal[
        "module",
        "class",
        "function",
        "api",
        "document",
        "concept"
    ]

    name: str
    # 人类可识别名称

    identifiers: Dict[str, str]
    # 系统级标识
    # 例：{"path": "auth/user_service.py", "symbol": "login"}


@dataclass
class Operation:
    """
    对实体施加的语义操作

    职责：
    - 明确“要对实体做什么”
    - 与具体工具实现解耦
    """

    action: Literal[
        "read",
        "search",
        "analyze",
        "compare",
        "summarize"
    ]

    target_entity: Optional[str]
    # 操作作用的实体名称（引用 EntityRef.name）

    parameters: Dict[str, Any]
    # 操作参数（非 Prompt 参数）


@dataclass
class Constraint:
    """
    语义层约束条件

    职责：
    - 约束系统行为
    - 不涉及生成风格或语言表达
    """

    rule: str
    # 例："只分析后端代码"

    level: Literal["hard", "soft"]
    # hard：必须满足
    # soft：尽量满足
