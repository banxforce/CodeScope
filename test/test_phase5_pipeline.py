"""
Phase 5 Pipeline Test Case

职责：
- 验证 Pipeline 的结构正确性
- 不关心 LLM 质量
- 不依赖真实检索 / 向量库
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from codescope.pipeline.semantic_execution_pipeline import SemanticExecutionPipeline
from codescope.pipeline.requirement_parser import RequirementParser
from codescope.pipeline.intent_analyzer import IntentAnalyzer
from codescope.pipeline.builders.semantic_task_builder import SemanticTaskBuilder
from codescope.pipeline.builders.retrieval_query_builder import RetrievalQueryBuilder
from codescope.pipeline.builders.generation_input_builder import GenerationInputBuilder
from codescope.retriever.base import BaseRetriever


class FakeRequirementParser:
    def parse(self, raw_text: str) -> Requirement:
        return Requirement(raw_text=raw_text)


class FakeIntentAnalyzer:
    def analyze(self, requirement: Requirement) -> IntentAnalysis:
        return IntentAnalysis(
            intent_summary="分析登录模块设计",
            task_type="analysis",
            entities=["login", "auth"],
            constraints=[],
            output_expectations=["解释清晰"],
            complexity="medium",
        )


class FakeRetriever(BaseRetriever):
    def retrieve(self, query):
        from domain.retrieval import RetrievalResult

        return RetrievalResult(
            query_id=query.query_id,
            chunks=[],
            confidence=1.0,
        )


def test_phase5_pipeline_runs():
    pipeline = SemanticExecutionPipeline(
        requirement_parser=FakeRequirementParser(),
        intent_analyzer=FakeIntentAnalyzer(),
        semantic_task_builder=SemanticTaskBuilder(),
        retrieval_query_builder=RetrievalQueryBuilder(),
        retriever=FakeRetriever(),
        generation_input_builder=GenerationInputBuilder(),
    )

    result = pipeline.run("dummy input")

    # Phase 5 断言重点：结构存在即可
    assert result is not None
    assert result.task is not None
    assert result.retrieval_result is not None
    assert result.task.intent == "分析登录模块设计"
    assert len(result.task.entities) == 2
