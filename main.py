from codescope.config.settings import settings
from codescope.llm.openai_like import OpenAILikeClient
from codescope.pipeline.builders.retrieval_query_builder import RetrievalQueryBuilder
from codescope.pipeline.builders.semantic_task_builder import SemanticTaskBuilder
from codescope.pipeline.intent_analyzer import IntentAnalyzer
from codescope.pipeline.requirement_parser import RequirementParser
from codescope.pipeline.semantic_execution_pipeline import SemanticExecutionPipeline
from codescope.pipeline.validators.semantic_task_validator import SemanticTaskValidator
from typing import Any, List
from codescope.domain.semantic_models import RetrievedChunk, RetrievalQuery
from codescope.rag.in_memory_query_compiler import InMemoryQueryCompiler
from codescope.pipeline.validators.retrieval_query_validator import RetrievalQueryValidator
import uuid


# 将 runner 的获取抽成一个方法
def get_runner() -> SemanticExecutionPipeline:
    """创建并返回配置好的 SemanticExecutionPipeline 实例"""
    llm_client = OpenAILikeClient(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )

    requirement_parser = RequirementParser(llm_client)
    intent_analyzer = IntentAnalyzer(llm_client)
    task_builder = SemanticTaskBuilder(llm_client)
    query_builder = RetrievalQueryBuilder()

    task_validator = SemanticTaskValidator()
    retrieval_query_validator = RetrievalQueryValidator()

    return SemanticExecutionPipeline(
        llm=llm_client,
        requirement_parser=requirement_parser,
        intent_analyzer=intent_analyzer,
        task_builder=task_builder,
        query_builder=query_builder,
        task_validator=task_validator,
        retrieval_query_validator=retrieval_query_validator,
    )


def make_mock_chunks() -> List[RetrievedChunk]:
    """创建模拟的检索结果块"""
    return [
        RetrievedChunk(
            chunk_id="c1",
            source_id="doc_auth",
            source_type="doc",
            content="User authentication should use JWT tokens.",
            relevance_score=0.9,
            metadata={},
        ),
        RetrievedChunk(
            chunk_id="c2",
            source_id="code_user_service",
            source_type="code",
            content="class UserService handles user login logic",
            relevance_score=0.8,
            metadata={},
        ),
    ]


if __name__ == "__main__":
    # 获取 runner
    runner = get_runner()

    raw_text = (
        "我们准备设计一个内部使用的代码检索工具，"
        "目标是让后端开发可以快速定位到某个业务功能相关的类和方法。"
        "请帮我设计整体方案，并分析是否有现成的开源方案可以参考，"
        "同时指出可能的风险和限制条件。"
    )

    raw_text2 = "“看看 UserService 里是怎么做用户登录校验的。"

    # 执行 runner
    queries = runner.run(raw_text2)

    # 创建查询编译器并执行
    compiler = InMemoryQueryCompiler(make_mock_chunks())

    for query in queries:
        result = compiler.execute(query)
        print(f"查询结果: {result}")
