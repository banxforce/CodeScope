"""
CodeScope - Phase 2.5 主入口（main.py）

职责：
- 接收用户的自然语言输入
- 触发 Phase 2.5 流水线：
  1. 构建需求格式化 Prompt
  2. 调用 LLM 将输入转换为结构化 Requirement
  3. 输出结构化结果，供后续模板检索与指令生成使用

说明：
- 本文件只负责“串流程”，不承载业务判断
- 不做模板选择、不做指令生成（那是 Phase 3 的事）
"""

from codescope.llm.client import LLMClient
from codescope.pipeline.format_requirement import format_requirement
from codescope.prompt.assembler import build_requirement_formatter_prompt
from codescope.utils.logger import get_logger
from codescope.pipeline.intent_analyzer import IntentAnalyzer
from codescope.pipeline.prompt_planner import PromptPlanner


logger = get_logger("codescope.main")


class MockLLMClient(LLMClient):
    """
    Mock LLM Client（Phase 2.5 使用）

    职责：
    - 在未接入真实 LLM 前，返回固定结构化结果
    - 用于验证 Phase 2.5 流水线是否打通
    """

    def complete(self, prompt: str) -> str:
        logger.info("Mock LLM 接收到 Prompt，开始返回模拟结果")
        return """
{
  "domain": "会议系统",
  "stage": "接口设计",
  "core_intent": "实现会议报名并支持并发安全",
  "entities": ["会议", "报名记录"],
  "operations": ["创建", "更新"],
  "non_functional": ["并发", "幂等"],
  "constraints": ["Java 后端"],
  "implicit_signals": []
}
"""


def main():
    """
    Phase 2.5 主流程入口。
    """
    logger.info("CodeScope Phase 2.5 启动")

    user_input = input("请输入需求描述：").strip()
    if not user_input:
        logger.warning("用户输入为空，流程终止")
        return

    # 1. 构建需求格式化 Prompt
    prompt = build_requirement_formatter_prompt(user_input)

    # 2. 初始化 LLM Client（当前使用 Mock）
    llm_client = MockLLMClient(model_name="mock")

    # 3. 调用 Phase 2.5 流水线，生成结构化 Requirement
    requirement = format_requirement(
        prompt=prompt,
        llm_client=llm_client
    )

    # 需求结构化结果
    print("\n=== Requirement ===")
    print(requirement)

    # 2. 意图分析
    analyzer = IntentAnalyzer()
    intent = analyzer.analyze(requirement)

    print("\n=== IntentAnalysis ===")
    print(intent)

    # 3. Prompt 规划
    planner = PromptPlanner()
    plan = planner.build_plan(requirement, intent)

    print("\n=== PromptPlan ===")
    print(plan)

    print("\n=== Steps ===")
    for step in plan.steps:
        print(f"- {step.step_id}: {step.purpose}")


if __name__ == "__main__":
    main()
