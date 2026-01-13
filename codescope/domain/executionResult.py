@dataclass
class ExecutionResult:
    """
    一次完整执行的结果
    """

    success: bool

    final_output: Any
    # 最终交付给用户的内容

    intermediate_outputs: Dict[str, Any]
    # 可选：用于调试或回放

    warnings: List[str]
    # 非致命问题
