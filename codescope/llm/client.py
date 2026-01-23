from abc import ABC, abstractmethod


"""
LLM Client 抽象封装。

职责：
- 对外提供统一的 LLM 调用接口
- 内部可切换 OpenAI / 本地模型 / Mock
"""
class LLMClient(ABC):

    @abstractmethod
    def complete(
        self,
        *,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> str:
        pass

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass