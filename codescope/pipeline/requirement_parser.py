import json
import logging
from typing import Any, Dict

from codescope.domain.requirement import Requirement
from codescope.llm.client import LLMClient
from codescope.prompt.system_templates import REQUIREMENT_SYSTEM_PROMPT_CN

logger = logging.getLogger(__name__)


class RequirementParser:
    """
    使用 LLM 将自然语言需求解析为 Requirement 对象。
    """

    def __init__(self, llm: LLMClient, max_retry: int = 1):
        self.llm = llm
        self.max_retry = max_retry

    def parse(self, text: str) -> Requirement:
        """
        主入口：返回一个结构化 Requirement
        """
        raw_output = self.llm.complete(
            system_prompt=REQUIREMENT_SYSTEM_PROMPT_CN,
            user_prompt=text,
            temperature=0.0,
        )

        try:
            return self._parse_output(raw_output)
        except Exception as e:
            logger.warning("需求解析失败，请重试一次: %s", e)

            if self.max_retry <= 0:
                raise

            # 二次尝试：强制 JSON 修复
            retry_output = self.llm.complete(
                system_prompt=REQUIREMENT_SYSTEM_PROMPT_CN
                              + "\n\n之前的输出是无效的JSON。"
                                "请只输出一个严格遵守规则的有效JSON对象。",
                user_prompt=text,
                temperature=0.0,
            )

            return self._parse_output(retry_output)

    def _parse_output(self, output: str) -> Requirement:
        """
        将 LLM 输出解析为 Requirement
        """
        data = self._load_json(output)
        self._validate_fields(data)
        return self._build_requirement(data)

    def _load_json(self, output: str) -> Dict[str, Any]:
        """
        解析 JSON，失败直接抛异常
        """
        try:
            return json.loads(output)
        except json.JSONDecodeError as e:
            logger.error("非法 JSON from LLM: %s\nRaw output:\n%s", e, output)
            raise

    def _validate_fields(self, data: Dict[str, Any]) -> None:
        """
        校验字段完整性与非法字段
        """
        allowed_fields = {
            "domain",
            "stage",
            "core_intent",
            "entities",
            "operations",
            "non_functional",
            "constraints",
            "implicit_signals",
            "warnings",
            "confidence",
            "assumptions",
        }

        extra_fields = set(data.keys()) - allowed_fields
        if extra_fields:
            raise ValueError(f"Unexpected fields in Requirement: {extra_fields}")

        if not data.get("core_intent"):
            raise ValueError("core_intent must be present and non-empty")

    def _build_requirement(self, data: Dict[str, Any]) -> Requirement:
        """
        构建 Requirement 对象，统一兜底
        """
        return Requirement(
            domain=data.get("domain"),
            stage=data.get("stage"),
            core_intent=data["core_intent"],
            entities=data.get("entities") or [],
            operations=data.get("operations") or [],
            non_functional=data.get("non_functional") or [],
            constraints=data.get("constraints") or [],
            implicit_signals=data.get("implicit_signals") or [],
            confidence=data.get("confidence") or 0.8,
            warnings=data.get("warnings") or [],
            assumptions=data.get("assumptions") or [],
        )
