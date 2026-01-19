# generation_input_builder.py

"""
GenerationInputBuilder

职责：
- 构建生成阶段的唯一输入边界 GenerationInput
- 隔离语义执行与生成实现
"""

from codescope.domain.semantic_models import (
    SemanticTask,
    RetrievalResult,
    GenerationInput,
)


class GenerationInputBuilder:
    """
    GenerationInput 构建器
    """

    def build(
        self,
        semantic_task: SemanticTask,
        retrieval_result: RetrievalResult,
    ) -> GenerationInput:
        """
        SemanticTask + RetrievalResult → GenerationInput
        """

        return GenerationInput(
            task=semantic_task,
            retrieval_result=retrieval_result,
            output_spec=semantic_task.output_spec,
        )
