from codescope.config.settings import settings
from codescope.llm.openai_like import OpenAILikeClient
from codescope.pipeline.intent_analyzer import LLMIntentAnalyzer
from codescope.pipeline.prompt_planner import PromptPlanner
from codescope.pipeline.requirement_parser import RequirementParserLLM
from codescope.utils.logger import get_logger

logger = get_logger("codescope.main")


def main():
    logger.info("CodeScope Phase 4 启动")

    user_input = input("请输入需求描述：").strip()
    if not user_input:
        logger.warning("用户输入为空，流程终止")
        return

    # 1. 初始化 LLM Client
    llm_client = OpenAILikeClient(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )

    # 2. Requirement 语义解析（LLM 驱动）
    parser = RequirementParserLLM(llm_client)
    requirement = parser.parse(user_input)

    print("\n=== Requirement ===")
    print(requirement)

    # 3. Intent 分析（仍可先用规则 / 半 LLM）
    analyzer = LLMIntentAnalyzer(llm_client)
    intent = analyzer.analyze(requirement)

    print("\n=== IntentAnalysis ===")
    print(intent)

    # 4. Prompt 规划（Phase 4 可仍是确定性）
    planner = PromptPlanner()
    plan = planner.build_plan(requirement, intent)

    print("\n=== PromptPlan ===")
    print(plan)

    print("\n=== Steps ===")
    for step in plan.steps:
        print(f"- {step.step_id}: {step.purpose}")


if __name__ == "__main__":
    main()
