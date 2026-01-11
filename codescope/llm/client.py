"""
LLM Client 抽象封装。

职责：
- 对外提供统一的 LLM 调用接口
- 内部可切换 OpenAI / 本地模型 / Mock
"""

class LLMClient:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def complete(self, prompt: str) -> str:
        """
        执行一次文本生成。

        :param prompt: 拼装完成的 Prompt
        :return: LLM 输出文本
        """
        raise NotImplementedError("LLMClient.complete 必须由具体实现类实现")
