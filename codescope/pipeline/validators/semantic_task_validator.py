from typing import List, Set, Dict, Any
from codescope.domain.semantic_models import SemanticTask


class SemanticTaskValidationError(Exception):
    """SemanticTask 校验失败异常"""
    pass


class SemanticTaskValidator:
    """
    对 SemanticTask 进行语义一致性与结构合法性校验。

    设计原则：
    1. 只做确定性校验（deterministic）
    2. 不引入任何推理或启发式逻辑
    3. 一旦失败，立即抛出异常
    """

    # task_type 与 operation.action 的合法映射
    TASK_OPERATION_MAP = {
        "code_search": {"search", "read"},
        "doc_query": {"search", "read", "summarize"},
        "analysis": {"analyze", "compare", "read"},
        "design": {"analyze", "compare", "summarize"},
        "explanation": {"read", "summarize"},
    }

    # 哪些 task_type 允许 entities 为空
    TASK_ALLOW_EMPTY_ENTITIES = {
        "design",
    }

    def validate_all(self, tasks: List[SemanticTask]) -> None:
        if not tasks:
            raise SemanticTaskValidationError("SemanticTask 列表不能为空")

        for task in tasks:
            self.validate(task)

    def validate(self, task: SemanticTask) -> None:
        self._validate_basic_fields(task)
        self._validate_entities(task)
        self._validate_operations(task)
        self._validate_constraints(task)
        self._validate_output_spec(task)

    # =========================
    # 各类校验规则
    # =========================

    def _validate_basic_fields(self, task: SemanticTask) -> None:
        if not task.task_id:
            raise SemanticTaskValidationError("task_id 不能为空")

        if not task.intent:
            raise SemanticTaskValidationError(
                f"SemanticTask[{task.task_id}] intent 不能为空"
            )

        if task.task_type not in self.TASK_OPERATION_MAP:
            raise SemanticTaskValidationError(
                f"SemanticTask[{task.task_id}] task_type 非法: {task.task_type}"
            )

    def _validate_entities(self, task: SemanticTask) -> None:
        if not task.entities and task.task_type not in self.TASK_ALLOW_EMPTY_ENTITIES:
            raise SemanticTaskValidationError(
                f"SemanticTask[{task.task_id}] entities 不能为空（task_type={task.task_type}）"
            )

        entity_names = set()
        for e in task.entities:
            if not e.name:
                raise SemanticTaskValidationError(
                    f"SemanticTask[{task.task_id}] EntityRef.name 不能为空"
                )
            entity_names.add(e.name)

        task._entity_name_set = entity_names  # 内部缓存，供后续校验使用

    def _validate_operations(self, task: SemanticTask) -> None:
        if not task.operations:
            raise SemanticTaskValidationError(
                f"SemanticTask[{task.task_id}] operations 不能为空"
            )

        allowed_actions = self.TASK_OPERATION_MAP[task.task_type]

        for op in task.operations:
            if op.action not in allowed_actions:
                raise SemanticTaskValidationError(
                    f"SemanticTask[{task.task_id}] "
                    f"operation.action={op.action} 与 task_type={task.task_type} 不匹配"
                )

            if op.target_entity:
                if op.target_entity not in task._entity_name_set:
                    raise SemanticTaskValidationError(
                        f"SemanticTask[{task.task_id}] "
                        f"operation.target_entity={op.target_entity} "
                        f"未在 entities 中声明"
                    )

    def _validate_constraints(self, task: SemanticTask) -> None:
        for c in task.constraints:
            if not c.rule:
                raise SemanticTaskValidationError(
                    f"SemanticTask[{task.task_id}] 存在空的 constraint.rule"
                )

            if c.level not in {"hard", "soft"}:
                raise SemanticTaskValidationError(
                    f"SemanticTask[{task.task_id}] constraint.level 非法: {c.level}"
                )

    def _validate_output_spec(self, task: SemanticTask) -> None:
        spec = task.output_spec

        if spec is None:
            raise SemanticTaskValidationError(
                f"SemanticTask[{task.task_id}] output_spec 不能为空"
            )

        if spec.output_type not in {"text", "markdown", "json", "code"}:
            raise SemanticTaskValidationError(
                f"SemanticTask[{task.task_id}] output_type 非法: {spec.output_type}"
            )

        if not isinstance(spec.quality_requirements, list):
            raise SemanticTaskValidationError(
                f"SemanticTask[{task.task_id}] quality_requirements 必须是列表"
            )
