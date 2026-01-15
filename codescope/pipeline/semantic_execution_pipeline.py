"""
SemanticExecutionPipeline (Phase 5)

职责：
- 定义 Phase 5 的标准语义执行主链路
- 严格基于结构化契约串联各阶段
- 不包含 Prompt / LLM / 具体检索实现
"""

from domain.requirement import Requirement
from domain.generation import GenerationInput
from domain.intent_analysis import IntentAnalysis
from domain.semantic import SemanticTask
from domain.retrieval import RetrievalQuery, RetrievalResult


class SemanticExecutionPipeline:
    """
    Phase 5 主 Pipeline
    """

    def __init__(
            self,
            requirement_parser,
            intent_analyzer,
            semantic_task_builder,
            retrieval_query_builder,
            retriever,
            generation_input_builder,
    ):
        self.requirement_parser = requirement_parser
        self.intent_analyzer = intent_analyzer
        self.semantic_task_builder = semantic_task_builder
        self.retrieval_query_builder = retrieval_query_builder
        self.retriever = retriever
        self.generation_input_builder = generation_input_builder

    def run(self, raw_text: str) -> GenerationInput:
        """
        执行入口

        raw_text → GenerationInput
        """

        # 1. Raw Text → Requirement
        requirement: Requirement = self.requirement_parser.parse(raw_text)

        # 2. Requirement → IntentAnalysis
        intent: IntentAnalysis = self.intent_analyzer.analyze(requirement)

        # 3. IntentAnalysis → SemanticTask
        semantic_task: SemanticTask = (
            self.semantic_task_builder.build(intent)
        )

        # 4. SemanticTask → RetrievalQuery
        retrieval_query: RetrievalQuery = (
            self.retrieval_query_builder.build(semantic_task)
        )

        # 5. RetrievalQuery → RetrievalResult
        retrieval_result: RetrievalResult = (
            self.retriever.retrieve(retrieval_query)
        )

        # 6. SemanticTask + RetrievalResult → GenerationInput
        generation_input: GenerationInput = (
            self.generation_input_builder.build(
                semantic_task=semantic_task,
                retrieval_result=retrieval_result,
            )
        )

        return generation_input
