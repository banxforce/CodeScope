from typing import List, Set, Dict, Any
from codescope.domain.semantic_models import RetrievedChunk


class RetrievedChunkValidationError(ValueError):
    pass


class RetrievedChunkValidator:

    def validate(self, chunk: RetrievedChunk) -> None:
        if not chunk.chunk_id:
            raise RetrievedChunkValidationError("chunk_id is required")

        if not chunk.source_id:
            raise RetrievedChunkValidationError("source_id is required")

        if chunk.source_type not in ("code", "doc", "api"):
            raise RetrievedChunkValidationError(
                f"invalid source_type: {chunk.source_type}"
            )

        if not chunk.content.strip():
            raise RetrievedChunkValidationError("content is empty")

        if not (0.0 <= chunk.relevance_score <= 1.0):
            raise RetrievedChunkValidationError(
                "relevance_score must be between 0.0 and 1.0"
            )
