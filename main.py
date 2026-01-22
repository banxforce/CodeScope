from codescope.config.settings import settings
from codescope.llm.openai_like import OpenAILikeClient
from codescope.pipeline.builders.retrieval_query_builder import RetrievalQueryBuilder
from codescope.pipeline.builders.semantic_task_builder import SemanticTaskBuilder
from codescope.pipeline.intent_analyzer import IntentAnalyzer
from codescope.pipeline.requirement_parser import RequirementParser
from codescope.pipeline.semantic_execution_pipeline import SemanticExecutionPipeline
from codescope.pipeline.validators.semantic_task_validator import SemanticTaskValidator

# =========================
# 示例 main（本地 Dry Run）
# =========================

if __name__ == "__main__":
    llm_client = OpenAILikeClient(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )

    requirement_parser = RequirementParser(llm_client)
    intent_analyzer = IntentAnalyzer(llm_client)
    task_builder = SemanticTaskBuilder(llm_client)
    task_validator = SemanticTaskValidator()
    query_builder = RetrievalQueryBuilder()

    runner = SemanticExecutionPipeline(
        llm=llm_client,
        requirement_parser=requirement_parser,
        intent_analyzer=intent_analyzer,
        task_builder=task_builder,
        task_validator=task_validator,
        query_builder=query_builder,
    )

    raw_text1 = (
        "我们准备设计一个内部使用的代码检索工具，"
        "目标是让后端开发可以快速定位到某个业务功能相关的类和方法。"
        "请帮我设计整体方案，并分析是否有现成的开源方案可以参考，"
        "同时指出可能的风险和限制条件。"
    )

    raw_text2 = "根据新的约见流程文档内容在当前项目中搭建新的约见流程接口和事件处理。别修改旧代码，用后缀`V3`来区别代表新的"

    runner.run(raw_text2)
