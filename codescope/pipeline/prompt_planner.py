from typing import List

from codescope.domain.requirement import Requirement
from codescope.domain.intent.intent_analysis import IntentAnalysis
from codescope.domain.prompt_plan import PromptPlan
from codescope.domain.prompt_step import PromptStep



class PromptPlanner:
    """
    PromptPlanner 根据 IntentAnalysis 构建 PromptPlan。

    设计原则：
    1. Planner 负责“步骤决策”，不负责 Prompt 内容
    2. 所有规则应可读、可调试
    3. 第一版采用规则驱动（Rule-based）
    """

    def build_plan(
        self,
        requirement: Requirement,
        intent: IntentAnalysis
    ) -> PromptPlan:
        """
        构建 PromptPlan（Prompt 执行蓝图）。
        """

        steps: List[PromptStep] = []

        # 1. 高复杂度 design 任务 → 先领域建模
        if intent.primary_intent == "design" and intent.is_complex():
            steps.append(self._build_domain_model_step())

        # 2. 主生成 / 设计步骤
        if intent.primary_intent in ("generate", "design"):
            steps.append(self._build_generation_step(intent))

        # 3. 如果存在 review / 风险 → 加评审步骤
        if "review" in intent.secondary_intents or intent.risks:
            steps.append(self._build_review_step())

        return PromptPlan(
            plan_id=self._generate_plan_id(requirement),
            intent_summary=self._build_intent_summary(intent),
            steps=steps,
            execution_strategy="sequential",
            fallback_strategy="fallback_to_single_prompt"
        )

    # =========================
    # Step Builder Methods
    # =========================

    def _build_domain_model_step(self) -> PromptStep:
        """
        构建领域建模步骤。
        """

        return PromptStep(
            step_id="step-domain-model",
            purpose="抽象业务领域模型，为后续设计提供语义基础",
            prompt_ref="domain_model_extraction_prompt",
            input_requirements=["Requirement"],
            output_type="DomainModel",
            constraints=[
                "不生成任何技术实现",
                "只描述业务实体及其关系"
            ]
        )

    def _build_generation_step(self, intent: IntentAnalysis) -> PromptStep:
        """
        构建核心生成 / 设计步骤。
        """

        return PromptStep(
            step_id="step-generate",
            purpose=f"完成核心 {intent.primary_intent} 任务",
            prompt_ref="structure_generation_prompt",
            input_requirements=[
                "DomainModel" if intent.is_complex() else "Requirement"
            ],
            output_type="PrimaryResult",
            constraints=[
                "输出应结构化",
                "明确设计或生成理由"
            ]
        )

    def _build_review_step(self) -> PromptStep:
        """
        构建评审 / 风险分析步骤。
        """

        return PromptStep(
            step_id="step-review",
            purpose="对生成结果进行工程评审与风险分析",
            prompt_ref="result_review_prompt",
            input_requirements=["PrimaryResult"],
            output_type="ReviewNotes",
            constraints=[
                "指出潜在问题",
                "给出改进建议"
            ],
            optional=True
        )

    # =========================
    # Helper Methods
    # =========================

    def _generate_plan_id(self, requirement: Requirement) -> str:
        """
        生成 Plan 的唯一标识。
        """

        return f"plan-{hash(requirement.core_intent) & 0xffff}"

    def _build_intent_summary(self, intent: IntentAnalysis) -> str:
        """
        生成人类可读的计划摘要。
        """

        parts = [f"主意图：{intent.primary_intent}"]

        if intent.secondary_intents:
            parts.append(f"辅助意图：{', '.join(intent.secondary_intents)}")

        parts.append(f"复杂度：{intent.complexity_level}")

        return "；".join(parts)
