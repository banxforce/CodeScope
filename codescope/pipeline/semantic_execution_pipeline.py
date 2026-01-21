"""
Phase 5 Semantic Execution Pipeline

职责：
- 串联 Phase 4 已完成「认知层」组件
- 在不引入任何新 LLM 推理的前提下
- 将 IntentAnalysis 转化为可执行的 GenerationInput

⚠️ 重要设计原则：
- 本 Pipeline 不关心 PromptPlan
- 不重新解析 Requirement
- 不重新分析 Intent
- 只消费 Phase 4 的稳定输出
"""

from typing import Any, List

from codescope.domain.requirement import Requirement
from codescope.domain.intent_analysis import IntentAnalysis
from codescope.domain.semantic_models import (
    SemanticTask,
    GenerationInput,
    RetrievalQuery,
    RetrievalResult,
)
from codescope.utils.logger import get_logger
import json


class SemanticExecutionPipeline:
    """
    Phase 5 主执行 Pipeline（Execution Layer）

    数据流：
    raw_text
      → Requirement              （Phase 4 / LLM）
      → IntentAnalysis           （Phase 4 / LLM）
      → SemanticTask             （Phase 5 / 确定性）
      → RetrievalQuery           （Phase 5 / 确定性）
      → RetrievalResult          （基础设施）
      → GenerationInput          （Phase 5 / 确定性）
    """

    def __init__(
            self,
            requirement_parser: Any,
            intent_analyzer: Any,
            semantic_task_builder: Any,
            retrieval_query_builder: Any,
            retriever: Any,
            generation_input_builder: Any,
    ):
        """
        这里不对具体类型做强约束的原因：

        - requirement_parser / intent_analyzer 已在 Phase 4 定型
        - 它们依赖 LLMClient，且不是纯数据类
        - Phase 5 只要求它们“行为正确”，不要求继承某个基类

        👉 这是「依赖接口行为，而不是继承层级」的典型用法
        """
        # 初始化logger
        self.logger = get_logger(__name__)

        self.requirement_parser = requirement_parser
        self.intent_analyzer = intent_analyzer
        self.semantic_task_builder = semantic_task_builder
        self.retrieval_query_builder = retrieval_query_builder
        self.retriever = retriever
        self.generation_input_builder = generation_input_builder

    def run(self, raw_text: str) -> GenerationInput:
        """
        Pipeline 执行入口

        输入：
            raw_text: 用户原始自然语言需求

        输出：
            GenerationInput：
            - 已包含：
              - 明确语义目标（SemanticTask）
              - 已检索上下文（RetrievalResult）
              - 可直接用于生成阶段
        """
        self.logger.info(f"raw_text: {raw_text}")

        # ========= Phase 4：认知层（LLM） =========

        # 1. Raw Text → Requirement
        requirement: Requirement = self.requirement_parser.parse(raw_text)

        self.logger.info(f"======================== Requirement ===========================")
        self.logger.info(f"requirement: {self.format_for_logging(requirement)}")

        # 2. Requirement → IntentAnalysis
        intent_analysis: IntentAnalysis = (
            self.intent_analyzer.analyze(requirement)
        )

        self.logger.info(f"======================== intent_analysis ===========================")
        self.logger.info(f"intent_analysis: {self.format_for_logging(intent_analysis)}")

        # ========= Phase 5：执行层（确定性） =========

        # 3. IntentAnalysis → SemanticTask
        # 使用类型注释而不是类型注解
        semantic_tasks = self.semantic_task_builder.build(intent_analysis)

        self.logger.info(f"======================== semantic_task ===========================")
        self.logger.info(f"Found {len(semantic_tasks)} semantic tasks")

        for i, task in enumerate(semantic_tasks):
            self.logger.info(f"\n=== Semantic Task {i + 1} ===")
            self.logger.info(f"task: {self.format_for_logging(task)}")

        # # 4. SemanticTask → RetrievalQuery
        # retrieval_query: RetrievalQuery = (
        #     self.retrieval_query_builder.build(semantic_task)
        # )
        #
        # self.logger.info(f"retrieval_query: {retrieval_query}")
        #
        # # 5. RetrievalQuery → RetrievalResult
        # retrieval_result: RetrievalResult = (
        #     self.retriever.retrieve(retrieval_query)
        # )
        #
        # self.logger.info(f"retrieval_result: {retrieval_result}")
        #
        # # 6. SemanticTask + RetrievalResult → GenerationInput
        # generation_input: GenerationInput = (
        #     self.generation_input_builder.build(
        #         semantic_task=semantic_task,
        #         retrieval_result=retrieval_result,
        #     )
        # )
        #
        # self.logger.info(f"generation_input: {generation_input}")

        return None

    @staticmethod
    def format_for_logging(obj):
        """格式化对象用于日志记录"""
        if hasattr(obj, 'model_dump'):
            return json.dumps(obj.model_dump(), indent=2, ensure_ascii=False)
        elif hasattr(obj, 'dict'):
            return json.dumps(obj.dict(), indent=2, ensure_ascii=False)
        elif isinstance(obj, (list, dict)):
            return json.dumps(obj, indent=2, ensure_ascii=False)
        else:
            return str(obj)