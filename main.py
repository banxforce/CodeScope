from codescope.pipeline.semantic_execution_pipeline import SemanticExecutionPipeline
from codescope.pipeline.requirement_parser import RequirementParser
from codescope.pipeline.intent_analyzer import IntentAnalyzer
from codescope.pipeline.builders.semantic_task_builder import SemanticTaskBuilder
from codescope.pipeline.builders.retrieval_query_builder import RetrievalQueryBuilder
from codescope.pipeline.builders.generation_input_builder import GenerationInputBuilder
from codescope.retriever.base import BaseRetriever
from codescope.config.settings import settings
from codescope.llm.openai_like import OpenAILikeClient

"""
Phase 5 入口（MVP）

职责：
- 以最小可运行方式串起 Phase 5 SemanticExecutionPipeline
- 不涉及 Prompt / LLM / 生成
- 仅验证：raw_text → GenerationInput 是否跑通
"""


class DummyRetriever(BaseRetriever):
    """
    Phase 5 用的假 Retriever
    只用于验证 Pipeline 结构是否闭合
    """

    def retrieve(self, query):
        from codescope.domain.semantic_models import RetrievalResult, RetrievedChunk

        return RetrievalResult(
            query_id=query.query_id,
            chunks=[
                RetrievedChunk(
                    source_id="dummy",
                    source_type="doc",
                    content="This is a dummy retrieval result for Phase 5.",
                    metadata={},
                )
            ],
            confidence=0.5,
        )


def main():
    llm_client = OpenAILikeClient(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )

    pipeline = SemanticExecutionPipeline(
        requirement_parser=RequirementParser(llm_client),
        intent_analyzer=IntentAnalyzer(llm_client),
        semantic_task_builder=SemanticTaskBuilder(llm_client),
        retrieval_query_builder=RetrievalQueryBuilder(),
        retriever=DummyRetriever(),
        generation_input_builder=GenerationInputBuilder(),
    )
    raw_text = """
    我有一个基于 Spring Boot 的老项目，启动速度很慢。
    帮我分析可能的原因，并看看是否有必要拆分模块或者引入异步初始化。
    默认使用 Java 17，不考虑更换技术栈。
"""
    raw_text_2 = """
我们准备设计一个内部使用的代码检索工具，目标是让后端开发可以快速定位到某个业务功能相关的类和方法。
请帮我设计整体方案，并分析是否有现成的开源方案可以参考，同时指出可能的风险和限制条件。
"""

    generation_input = pipeline.run(raw_text_2)

    # # Phase 5 的“成功标准”：能稳定打印这些内容
    # print("=== Phase 5 Pipeline Result ===")
    # print("Task ID:", generation_input.task.task_id)
    # print("Intent:", generation_input.task.intent)
    # print("Entities:", [e.name for e in generation_input.task.entities])
    # print("Retrieved Chunks:", len(generation_input.retrieval_result.chunks))


if __name__ == "__main__":
    main()
