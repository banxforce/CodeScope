from dataclasses import dataclass
from typing import List


@dataclass
class IntentAnalysis:
    """
    IntentAnalysis 表示系统对一个 Requirement 的意图理解结果。

    设计原则：
    1. 只表达“想清楚了什么”，不表达“怎么想的”
    2. 字段应可解释、可记录、可回放
    3. 不包含任何 Prompt / LLM / 规划细节
    """

    primary_intent: str
    """
    本次需求的主意图类型。
    示例：
    - generate   : 生成某种结果
    - analyze    : 分析已有信息
    - design     : 设计结构或方案
    - review     : 审查、评估、指出问题
    """

    secondary_intents: List[str]
    """
    辅助或隐含意图。
    示例：
    - risk_analysis
    - constraint_check
    - refactor
    """

    complexity_level: str
    """
    任务复杂度评估，用于决定是否需要多 Prompt 组合。
    可选值（约定）：
    - low     : 单一步骤即可完成
    - medium  : 少量推理或补充步骤
    - high    : 必须拆解为多步骤
    """

    key_decisions: List[str]
    """
    本次任务中必须明确或做出判断的关键决策点。
    示例：
    - 是否需要领域建模
    - 是否存在技术选型权衡
    """

    risks: List[str]
    """
    潜在风险或失败点。
    示例：
    - 上下文信息不足
    - 输出结果不可逆（如 ES mapping）
    """

    assumptions: List[str]
    """
    系统在当前分析中默认接受的前提条件。
    示例：
    - 使用 Java 技术栈
    - 目标系统版本 >= 某版本
    """

    def is_complex(self) -> bool:
        """
        判断该意图是否为高复杂度任务。
        PromptPlanner 可基于此决定是否启用多步骤规划。
        """
        return self.complexity_level == "high"
