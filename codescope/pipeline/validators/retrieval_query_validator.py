from typing import List, Set, Dict, Any
from codescope.domain.semantic_models import RetrievalQuery


class RetrievalQueryValidationError(ValueError):
    pass


class RetrievalQueryValidator:
    """对 RetrievalQuery 进行结构与语义层校验。"""

    ALLOWED_SCOPES = {"code", "doc", "api"}

    def validate(self, query: RetrievalQuery) -> None:
        self._validate_basic_fields(query)
        self._validate_scope(query)
        self._validate_keywords(query)
        self._validate_entity_refs(query)
        self._validate_filters(query)

    # 基础字段校验
    def _validate_basic_fields(self, query: RetrievalQuery) -> None:
        if not query.query_id:
            raise RetrievalQueryValidationError("query_id is required")

        if not isinstance(query.query_id, str):
            raise RetrievalQueryValidationError("query_id must be str")

    # scope 校验（防止“全库乱查”）
    def _validate_scope(self, query: RetrievalQuery) -> None:
        if query.scope not in self.ALLOWED_SCOPES:
            raise RetrievalQueryValidationError(
                f"invalid scope: {query.scope}"
            )

    # keywords 校验（防止空检索）
    def _validate_keywords(self, query: RetrievalQuery) -> None:
        if not query.keywords:
            raise RetrievalQueryValidationError(
                "keywords must not be empty"
            )

        if not all(isinstance(k, str) and k.strip() for k in query.keywords):
            raise RetrievalQueryValidationError(
                "keywords must be non-empty strings"
            )

    # entity_refs 校验（语义锚点）
    def _validate_entity_refs(self, query: RetrievalQuery) -> None:
        if not query.entity_refs:
            # 允许没有实体，但必须靠 keywords 驱动
            return

        for ref in query.entity_refs:
            if not ref.name:
                raise RetrievalQueryValidationError(
                    "entity_ref.name is required"
                )

            if not ref.entity_type:
                raise RetrievalQueryValidationError(
                    "entity_ref.entity_type is required"
                )

    # filters 校验（限制自由度）
    def _validate_filters(self, query: RetrievalQuery) -> None:
        if query.filters is None:
            return

        if not isinstance(query.filters, dict):
            raise RetrievalQueryValidationError(
                "filters must be a dict"
            )

        # 防止不可序列化对象混入
        for key, value in query.filters.items():
            if not isinstance(key, str):
                raise RetrievalQueryValidationError(
                    "filter keys must be strings"
                )

            if isinstance(value, (list, dict, str, int, float, bool, type(None))):
                continue

            raise RetrievalQueryValidationError(
                f"unsupported filter value type: {type(value)}"
            )
