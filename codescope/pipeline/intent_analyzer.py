from typing import List

from codescope.domain.intent.intent_analysis import IntentAnalysis
from codescope.domain.requirement import Requirement


class IntentAnalyzer:
    """
    IntentAnalyzer 用于从 Requirement 中推断用户的真实意图。

    当前版本特点：
    - 基于规则与约定（Rule-based）
    - 行为可预测、可调试
    - 适合作为 Phase 3 的第一版实现

    后续可演进方向：
    - 引入 LLM 进行意图分类与复杂度评估
    - 人工规则 + LLM 结果融合
    """

    def analyze(self, requirement: Requirement) -> IntentAnalysis:
        """
        从 Requirement 推断 IntentAnalysis。

        :param requirement: 已格式化的用户需求
        :return: IntentAnalysis
        """

        primary_intent = self._detect_primary_intent(requirement)
        secondary_intents = self._detect_secondary_intents(requirement)
        complexity_level = self._assess_complexity(requirement, secondary_intents)
        key_decisions = self._extract_key_decisions(requirement, primary_intent)
        risks = self._identify_risks(requirement, primary_intent)
        assumptions = self._build_assumptions(requirement)

        return IntentAnalysis(
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            complexity_level=complexity_level,
            key_decisions=key_decisions,
            risks=risks,
            assumptions=assumptions,
        )

    # =========================
    # 以下为内部规则方法
    # =========================

    def _detect_primary_intent(self, requirement: Requirement) -> str:
        """
        判断主意图类型。

        优先级说明：
        - design > generate > analyze > review
        """

        ops = set(requirement.operations)

        if "设计" in ops or "design" in ops:
            return "design"
        if "生成" in ops or "generate" in ops:
            return "generate"
        if "分析" in ops or "analyze" in ops:
            return "analyze"
        if "评审" in ops or "review" in ops:
            return "review"

        # 默认兜底
        return "generate"

    def _detect_secondary_intents(self, requirement: Requirement) -> List[str]:
        """
        检测隐含或辅助意图。
        """

        secondary = []

        ops = set(requirement.operations)
        nfrs = set(requirement.non_functional)

        if "评估" in ops or "风险" in ops:
            secondary.append("risk_analysis")

        if nfrs:
            secondary.append("constraint_check")

        if "重构" in ops or "refactor" in ops:
            secondary.append("refactor")

        return secondary

    def _assess_complexity(
        self,
        requirement: Requirement,
        secondary_intents: List[str]
    ) -> str:
        """
        评估任务复杂度，用于指导 Prompt 是否需要拆解。
        """

        # 显式多意图
        if len(secondary_intents) >= 2:
            return "high"

        # 设计类任务通常不简单
        if requirement.stage == "design":
            return "high"

        # 实体和约束较多
        if len(requirement.entities) >= 4 or len(requirement.constraints) >= 2:
            return "medium"

        return "low"

    def _extract_key_decisions(
        self,
        requirement: Requirement,
        primary_intent: str
    ) -> List[str]:
        """
        提取关键决策点。
        """

        decisions = []

        if primary_intent == "design":
            decisions.append("是否需要进行领域建模")
            decisions.append("结构是否需要考虑未来扩展")

        if requirement.non_functional:
            decisions.append("非功能性需求如何影响设计")

        return decisions

    def _identify_risks(
        self,
        requirement: Requirement,
        primary_intent: str
    ) -> List[str]:
        """
        识别潜在风险。
        """

        risks = []

        if not requirement.entities:
            risks.append("缺乏明确的业务实体描述")

        if primary_intent == "design":
            risks.append("设计结果一旦落地修改成本较高")

        if requirement.constraints:
            risks.append("约束条件可能限制方案灵活性")

        return risks

    def _build_assumptions(self, requirement: Requirement) -> List[str]:
        """
        构建系统默认接受的前提条件。
        """

        assumptions = []

        if requirement.domain:
            assumptions.append(f"领域为 {requirement.domain}")

        if requirement.stage:
            assumptions.append(f"当前阶段为 {requirement.stage}")

        return assumptions
