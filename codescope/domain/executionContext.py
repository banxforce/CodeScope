@dataclass
class ExecutionContext:
    """
    Prompt 执行过程中的上下文容器
    """

    requirement: Requirement
    intent_analysis: IntentAnalysis
    plan: PromptPlan

    step_outputs: Dict[str, Any]
    # key: step_id
    # value: 实际输出

    shared_memory: Dict[str, Any]
    # 跨步骤共享的信息
    # 例：领域词表、用户偏好、技术栈约定
