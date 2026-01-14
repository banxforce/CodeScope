from dataclasses import dataclass, asdict
from typing import List, Optional
import json

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

    '''
    LLM 对“当前 Requirement 结构是否准确反映用户真实意图”的自评
    < 0.6 → 阻断流程，要求澄清
    0.6 ~ 0.8 → 继续，但 Planner 保守
    0.8 → 正常自动编排
    '''
    confidence: float  # 0.0 ~ 1.0

    '''
    结构化风险说明
    定义：codescope/domain/enums/requirement_warning.py
    '''
    warnings: List[str]

    '''
    隐式假设
    示例：
        “假设这是一个后端系统”
        “假设使用 MySQL 而非 PostgreSQL”
        “假设是面向内部系统而非对外产品”
    作用：
        Review 阶段人可以快速判断“是不是你自己脑补的”
        Phase5 可以把它作为 反问澄清模板的输入
    '''
    assumptions: List[str]

    def to_json(self) -> str:
        """将Requirement对象转换为JSON字符串"""
        # 使用dataclasses.asdict将数据类转换为字典
        data = asdict(self)
        # 处理特殊类型（如果需要）
        return json.dumps(data, ensure_ascii=False, indent=2)

    def to_dict(self) -> dict:
        """将Requirement对象转换为字典"""
        return asdict(self)