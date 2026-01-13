@dataclass
class IntentAnalysis:
    """
    对 Requirement 的推理结果
    用于回答：这是一个什么类型的任务？是否复杂？是否需要拆解？
    """

    primary_intent: str
    # 例：generate / analyze / review / refactor / plan / explain

    secondary_intents: List[str]
    # 隐含或辅助意图
    # 例：["constraint_check", "risk_analysis"]

    complexity_level: str
    # low / medium / high
    # 决定是否需要多 Prompt 组合

    key_decisions: List[str]
    # 本次任务中必须做出的关键判断
    # 例：["是否需要领域建模", "是否涉及性能权衡"]

    risks: List[str]
    # 潜在失败点
    # 例：["上下文不足", "需求描述不完整"]

    assumptions: List[str]
    # 系统当前默认接受的前提
    # 例：["使用 Java 技术栈", "ES 版本 >= 8.x"]
