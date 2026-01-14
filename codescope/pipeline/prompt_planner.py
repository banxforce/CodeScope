import json
from typing import Any, Dict, List
from dataclasses import asdict

from codescope.domain.requirement import Requirement
from codescope.domain.intent_analysis import IntentAnalysis
from codescope.domain.prompt_plan import PromptPlan
from codescope.domain.prompt_step import PromptStep
from codescope.prompt.system_templates import PROMPT_PLANNER_SYSTEM_PROMPT_CN

class DrivenPromptPlannerLLM:
    """
    Phase 4 最终版 Prompt Planner（LLM 驱动）

    职责边界：
    1. 接收 Requirement + IntentAnalysis
    2. 调用 LLM 生成 PromptPlan（JSON）
    3. 将 JSON 解析为 PromptPlan / PromptStep
    4. 做最小、确定性的工程校验

    明确不做的事情：
    - 不执行 Prompt
    - 不解释规划理由
    - 不兜底生成内容
    """

    def __init__(self, llm):
        self.llm = llm

    # ==================================================
    # 对外唯一入口
    # ==================================================
    def plan(
        self,
        requirement: Requirement,
        intent: IntentAnalysis
    ) -> PromptPlan:
        """
        基于 Requirement + IntentAnalysis 生成 PromptPlan
        """

        system_prompt = PROMPT_PLANNER_SYSTEM_PROMPT_CN
        user_prompt = self._build_user_prompt(requirement, intent)

        raw_output = self.llm.complete(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )

        plan_dict = self._parse_llm_output(raw_output)
        plan = self._dict_to_prompt_plan(plan_dict)

        self._validate_plan(plan)

        return plan

    # ==================================================
    # Prompt 构造
    # ==================================================
    def _build_user_prompt(
        self,
        requirement: Requirement,
        intent: IntentAnalysis
    ) -> str:
        """
        将结构化对象转为 Planner 视角的上下文输入
        """

        return f"""
【Requirement】
{asdict(requirement)}

【IntentAnalysis】
{asdict(intent)}

请严格按照系统指令，生成 PromptPlan（JSON 格式）。
"""

    # ==================================================
    # LLM 输出解析
    # ==================================================
    def _parse_llm_output(self, raw_text: str) -> Dict[str, Any]:
        """
        将 LLM 返回内容解析为 dict

        约定：
        - LLM 必须返回合法 JSON
        - 不允许 Markdown 包裹
        """

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError as e:
            raise ValueError(
                "LLM 返回内容不是合法 JSON，无法解析为 PromptPlan\n"
                f"Error: {e}\n"
                f"Raw Output:\n{raw_text}"
            )

    # ==================================================
    # dict → PromptPlan
    # ==================================================
    def _dict_to_prompt_plan(self, data: Dict[str, Any]) -> PromptPlan:
        """
        将 dict 转换为 PromptPlan 对象
        """

        steps: List[PromptStep] = []

        for step_data in data.get("steps", []):
            step = PromptStep(
                step_id=step_data["step_id"],
                purpose=step_data["purpose"],
                prompt_ref=step_data["prompt_ref"],
                input_requirements=step_data.get("input_requirements", []),
                output_type=step_data["output_type"],
                constraints=step_data.get("constraints", []),
                optional=step_data.get("optional", False)
            )
            steps.append(step)

        return PromptPlan(
            plan_id=data["plan_id"],
            intent_summary=data["intent_summary"],
            steps=steps,
            execution_strategy=data.get("execution_strategy", "sequential"),
            fallback_strategy=data.get("fallback_strategy")
        )

    # ==================================================
    # Phase 4 级别校验（最小但严格）
    # ==================================================
    def _validate_plan(self, plan: PromptPlan):
        """
        Phase 4 的工程底线校验：
        - Planner 产物必须是确定、可执行、可回放的
        """

        if not plan.steps:
            raise ValueError("PromptPlan 至少必须包含一个 PromptStep")

        if plan.execution_strategy != "sequential":
            raise ValueError("Phase 4 仅支持 sequential 执行策略")

        step_ids = set()
        previous_outputs = {"Requirement"}

        for step in plan.steps:
            # step_id 唯一性
            if step.step_id in step_ids:
                raise ValueError(f"检测到重复的 step_id: {step.step_id}")
            step_ids.add(step.step_id)

            # 输入必须来自 Requirement 或前序输出
            for inp in step.input_requirements:
                if inp not in previous_outputs:
                    raise ValueError(
                        f"Step {step.step_id} 使用了非法 input: {inp}"
                    )

            previous_outputs.add(step.output_type)
