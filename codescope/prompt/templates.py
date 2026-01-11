"""
Prompt 模板定义。

职责：
- 存放静态 Prompt 模板
- 不包含拼装逻辑
"""

REQUIREMENT_FORMATTER_PROMPT = """
你是一个需求结构化助手。

请将用户输入转换为 JSON，严格遵守 Requirement Schema。
不允许新增字段，不确定请使用 null 或空数组。

用户输入：
{user_input}
"""
