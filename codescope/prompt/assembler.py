"""
Prompt 拼装器。

职责：
- 将模板 + 上下文拼装为最终 Prompt
"""

from codescope.prompt.templates import REQUIREMENT_FORMATTER_PROMPT


def build_requirement_formatter_prompt(user_input: str) -> str:
    """
    构建需求格式化 Prompt。
    """
    return REQUIREMENT_FORMATTER_PROMPT.format(user_input=user_input)
