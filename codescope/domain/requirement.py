from dataclasses import dataclass
from typing import List, Optional

'''
Requirement：需求结构化结果对象

职责定位（Phase 2.5）：
- 表示“用户自然语言需求”的结构化结果
- 由 LLM 根据 Prompt 生成，再由程序反序列化得到
- 不负责推理、不负责校验、不保证完整性
- 作为后续模板理解 / 匹配 / 指令生成的输入事实

设计原则：
- 字段可为空（null / 空数组），但不可编造
- 所有信息必须可在用户输入中直接或明确推导得到
'''
@dataclass
class Requirement:
    # 所属业务领域（如：订单、会议、用户、支付等）
    # 若用户未明确表达，允许为 None
    domain: Optional[str]

    # 需求所处阶段或场景（如：创建 / 查询 / 修改 / 运维 / 设计）
    # 用于后续模板匹配，不作为强约束
    stage: Optional[str]

    # 用户“最核心”的意图描述（一句话，必须存在）
    # 要求忠实反映用户表达，不进行系统级推断
    core_intent: str

    # 需求中涉及的关键业务实体（名词集合）
    # 例如：会议、订单、用户、接口、数据库等
    # 未出现时使用空列表 []
    entities: List[str]

    # 用户明确提到的操作或行为（动词集合）
    # 例如：创建、更新、查询、绑定、优化等
    # 不包含系统自动补充的行为
    operations: List[str]

    # 非功能性需求（如性能、安全、稳定性、可扩展性等）
    # 仅在用户明确提及时填写
    non_functional: List[str]

    # 明确的约束条件（如时间范围、规则限制、兼容性要求等）
    # 不包含隐含假设或行业常识
    constraints: List[str]

    # 用户表达中体现出的隐含信号或倾向
    # 如：对风险敏感、偏好稳定方案、追求快速交付等
    # 仅在表达明确时使用
    implicit_signals: List[str]
