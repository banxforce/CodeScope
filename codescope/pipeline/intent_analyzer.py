from typing import List
from codescope.domain.intent_analysis import IntentAnalysis
from codescope.domain.requirement import Requirement
from codescope.prompt.system_templates import INTENT_ANALYSIS_SYSTEM_PROMPT_CN
from codescope.llm.client import LLMClient
import json

"""
基于 LLM 的 IntentAnalyzer（Phase 4）。

特点：
- 输入仍然是 Requirement（结构化）
- 输出 IntentAnalysis（结构不变）
- 通过 Prompt 显式约束分析逻辑
"""


class LLMIntentAnalyzer:

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def analyze(self, requirement: Requirement) -> IntentAnalysis:
        prompt = self._build_prompt(requirement)
        output = self.llm.complete(
            system_prompt=INTENT_ANALYSIS_SYSTEM_PROMPT_CN,
            user_prompt=prompt,
            temperature=0.0,
        )
        try:
            return self._parse_output(output)
        except Exception as e:
            logger.warning("IntentAnalysis返回解析失败，请重试一次: %s", e)

            # 二次尝试：强制 JSON 修复
            retry_output = self.llm.complete(
                system_prompt=INTENT_ANALYSIS_SYSTEM_PROMPT_CN
                              + "\n\n之前的输出是无效的JSON。"
                                "请只输出一个严格遵守规则的有效JSON对象。",
                user_prompt=text,
                temperature=0.0,
            )

            return self._parse_output(retry_output)

    # User Prompt（Requirement 注入）
    def _build_prompt(self, requirement: Requirement) -> str:
        return f"""
    输入 Requirement 如下：

    {requirement.to_json()}

    请输出一个 IntentAnalysis JSON，字段必须且仅允许包含：

    - primary_intent
    - secondary_intents
    - complexity_level
    - key_decisions
    - risks
    - assumptions
    """

    # 输出解析（强校验）
    def _parse_output(self, output: str) -> IntentAnalysis:
        data = json.loads(output)

        return IntentAnalysis(
            primary_intent=data["primary_intent"],
            secondary_intents=data.get("secondary_intents", []),
            complexity_level=data["complexity_level"],
            key_decisions=data.get("key_decisions", []),
            risks=data.get("risks", []),
            assumptions=data.get("assumptions", []),
        )
