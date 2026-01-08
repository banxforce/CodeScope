from dataclasses import dataclass
from typing import Optional


@dataclass
class Requirement:
    """
    用户的原始需求（口语化输入）
    """
    raw_text: str

    # 可选：后续可以在这里加解析结果
    business_context: Optional[str] = None
