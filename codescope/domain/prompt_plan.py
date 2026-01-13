@dataclass
class PromptPlan:
    """
    一次任务的 Prompt 执行蓝图
    """

    plan_id: str

    intent_summary: str
    # 人类可读的一句话总结
    # 例："这是一个需要先分析再生成的复杂需求"

    steps: List[PromptStep]

    execution_strategy: str
    # sequential / conditional / iterative
    # Phase 3 先支持 sequential 就够了

    fallback_strategy: Optional[str]
    # 当某一步失败时的策略
    # 例："跳过评审步骤" / "回退到单 Prompt 模式"
