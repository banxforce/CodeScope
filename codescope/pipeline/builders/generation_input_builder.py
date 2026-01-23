from typing import List, Optional
from dataclasses import dataclass, field
import uuid
from codescope.domain.semantic_models import (
    SemanticTask,
    OutputSpec,
    GenerationInput,
)


@dataclass
class GenerationInputBuilder:
    """
    将 RetrievalResult 转化为 LLM 可用的 GenerationInput。
    """
    task: "SemanticTask"
    output_spec: Optional["OutputSpec"] = None
    top_k: Optional[int] = None  # 取每个 RetrievalResult 的 top_k chunk
    min_confidence: float = 0.0  # 过滤过低置信度的 chunk

    def build(
            self,
            retrieval_results: List["RetrievalResult"]
    ) -> "GenerationInput":
        """
        将多个 RetrievalResult 转化为一个 GenerationInput
        """
        all_chunks: List["RetrievedChunk"] = []

        for result in retrieval_results:
            # 过滤掉低置信度 RetrievalResult
            if result.confidence < self.min_confidence:
                continue

            # 按 chunk relevance 排序
            chunks = sorted(
                result.chunks,
                key=lambda c: c.relevance_score,
                reverse=True
            )

            # top_k 限制
            if self.top_k:
                chunks = chunks[:self.top_k]

            all_chunks.extend(chunks)

        # 如果没有指定 output_spec，使用 task 自带的
        output_spec = self.output_spec or self.task.output_spec

        return GenerationInput(
            task=self.task,
            retrieval_result=RetrievalResult(
                query_id=str(uuid.uuid4()),
                chunks=all_chunks,
                confidence=self._compute_confidence(all_chunks),
                total_hits=len(all_chunks)
            ),
            output_spec=output_spec
        )

    def _compute_confidence(self, chunks: List["RetrievedChunk"]) -> float:
        """
        计算合并后的 confidence
        """
        if not chunks:
            return 0.0
        return sum(c.relevance_score for c in chunks) / len(chunks)
