import requests
from codescope.llm.client import LLMClient
from .client import LLMClient


class OpenAILikeClient(LLMClient):

    def __init__(self, api_key: str, base_url: str, model: str):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model

    def complete(
            self,
            *,
            system_prompt: str,
            user_prompt: str,
            temperature: float = 0.0,
    ) -> str:
        url = f"{self.base_url}/v1/chat/completions"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()

        data = resp.json()
        return data["choices"][0]["message"]["content"]

    # ✅ 新增：统一的 generate 接口
    def generate(self, prompt: str) -> str:
        """
        对外统一生成接口，供 GenerationExecutor 调用
        """
        return self.complete(
            system_prompt="你是一个严谨、基于证据回答问题的助手。",
            user_prompt=prompt,
            temperature=0.0,
        )
