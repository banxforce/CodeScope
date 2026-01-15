from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Literal, Type
from enum import Enum


@dataclass
class RetrievalQuery:
    """
    检索模块的标准输入契约

    职责：
    - 将语义任务映射为可执行的检索请求
    """

    query_id: str

    scope: Literal["code", "doc", "api"]

    keywords: List[str]

    entity_refs: List[EntityRef]

    filters: Dict[str, Any]
    # 例：{"language": "python", "layer": "service"}


@dataclass
class RetrievedChunk:
    """
    检索得到的最小信息单元
    """

    source_id: str
    source_type: Literal["code", "doc"]

    content: str

    metadata: Dict[str, Any]


@dataclass
class RetrievalResult:
    """
    检索模块输出的标准结果

    职责：
    - 为生成阶段提供“已定位上下文”
    - 可被缓存、复用、评估
    """

    query_id: str

    chunks: List[RetrievedChunk]

    confidence: float
    # 检索结果整体可信度
