from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PromptStep:
    """
    Prompt 执行计划中的一个步骤
    """

    step_id: str
    # 唯一标识，如 step-1

    purpose: str
    # 这个 Prompt 存在的目的
    # 例："抽取领域对象"

    prompt_ref: str
    # Prompt 模板的引用（ID / 文件名 / 向量ID）

    input_requirements: List[str]
    # 执行该 Prompt 需要哪些输入
    # 例：["Requirement", "上一步输出"]

    output_type: str
    # 输出的语义类型
    # 例："DomainModel", "ReviewNotes"

    constraints: List[str]
    # 本步骤必须满足的约束
    # 例：["不要生成代码", "只输出 JSON"]

    optional: bool = False
    # 是否为可跳过步骤
