import os
from datetime import datetime


class MarkdownWriter:
    """
    将 GenerationResult 写入 markdown 文件
    """

    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def write(self, result: "GenerationResult") -> str:
        """
        写入 markdown 文件
        返回生成的文件路径
        """
        filename = self._build_filename(result)
        path = os.path.join(self.output_dir, filename)

        content = self._build_markdown(result)

        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

        return path

    def _build_filename(self, result: "GenerationResult") -> str:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{result.task_id}_{ts}.md"

    def _build_markdown(self, result: "GenerationResult") -> str:
        return f"""# 任务结果

## Task ID
{result.task_id}

## 生成内容
{result.content}

## 使用的 Evidence
{chr(10).join(f"- {cid}" for cid in result.used_chunks)}

## 生成置信度
{result.confidence:.2f}
"""
