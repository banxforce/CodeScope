"""
Markdown 工具。

职责：
- 文本 / Markdown 格式化辅助
"""


def code_block(code: str, language: str = "") -> str:
    """
    生成 Markdown 代码块。
    """
    return f"```{language}\n{code}\n```"
