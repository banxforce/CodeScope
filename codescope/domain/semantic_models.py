"""语义、检索、生成三层的领域模型。"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal, Type


# =========================
# 语义层组件
# =========================

@dataclass
class EntityRef:
    """实体的稳定语义引用。"""

    entity_type: Literal[
        "module",
        "class",
        "function",
        "api",
        "document",
        "concept",
    ]
    name: str
    identifiers: Dict[str, str]


@dataclass
class Operation:
    """对实体施加的语义操作。"""

    action: Literal[
        "read",
        "search",
        "analyze",
        "compare",
        "summarize",
    ]
    target_entity: Optional[str]
    parameters: Dict[str, Any]


@dataclass
class Constraint:
    """语义层约束（与生成风格无关）。"""

    rule: str
    level: Literal["hard", "soft"]


@dataclass
class OutputSpec:
    """对最终输出的结构化期望。"""

    output_type: Literal[
        "text",
        "markdown",
        "json",
        "code",
    ]
    schema: Optional[Type]
    quality_requirements: List[str]


@dataclass
class SemanticTask:
    """标准化的语义任务表示。"""

    task_id: str
    intent: str
    task_type: Literal[
        "code_search",
        "doc_query",
        "design",
        "analysis",
        "explanation",
    ]
    entities: List[EntityRef]
    operations: List[Operation]
    constraints: List[Constraint]
    output_spec: OutputSpec


# =========================
# 检索层组件
# =========================

@dataclass
class RetrievalQuery:
    """检索模块的标准输入契约。"""

    query_id: str
    scope: Literal["code", "doc", "api"]
    keywords: List[str]
    entity_refs: List[EntityRef]
    filters: Dict[str, Any]


@dataclass
class RetrievedChunk:
    """检索得到的最小信息单元。"""

    source_id: str
    source_type: Literal["code", "doc"]
    content: str
    metadata: Dict[str, Any]


@dataclass
class RetrievalResult:
    """检索模块的标准输出结果。"""

    query_id: str
    chunks: List[RetrievedChunk]
    confidence: float


# =========================
# 生成层组件
# =========================

@dataclass
class GenerationInput:
    """生成阶段的标准输入边界。"""

    task: SemanticTask
    retrieval_result: RetrievalResult
    output_spec: OutputSpec


@dataclass
class GenerationConfig:
    """生成层的 Prompt 配置实体。"""

    config_id: str
    system_prompt: str
    template_ref: Optional[str]
    constraints: List[str]


__all__ = [
    "EntityRef",
    "Operation",
    "Constraint",
    "OutputSpec",
    "SemanticTask",
    "RetrievalQuery",
    "RetrievedChunk",
    "RetrievalResult",
    "GenerationInput",
    "GenerationConfig",
]
