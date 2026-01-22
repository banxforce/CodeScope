from typing import List, Set, Dict, Any
from codescope.domain.semantic_models import RetrievalResult

class RetrievalResultValidationError(ValueError):
    pass


class RetrievalResultValidator:

    def validate(self, result: RetrievalResult) -> None:
        if not result.query_id:
            raise RetrievalResultValidationError("query_id is required")

        if not result.chunks:
            raise RetrievalResultValidationError(
                "retrieval_result has no chunks"
            )

        for chunk in result.chunks:
            RetrievedChunkValidator().validate(chunk)

        if not (0.0 <= result.confidence <= 1.0):
            raise RetrievalResultValidationError(
                "confidence must be between 0.0 and 1.0"
            )
