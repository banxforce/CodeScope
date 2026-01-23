import os
import uuid
from typing import List

from codescope.domain.semantic_models import ChunkSource


def load_chunks_from_project(
    *,
    code_dir: str,
    doc_dir: str | None = None,
) -> List[ChunkSource]:
    """
    从项目中加载代码 / 文档，构建 ChunkSource 列表
    仅在索引构建阶段调用
    """

    chunks: List[ChunkSource] = []

    # 1️⃣ 加载代码文件
    for root, _, files in os.walk(code_dir):
        for fname in files:
            if not fname.endswith((".py", ".java", ".js")):
                continue

            path = os.path.join(root, fname)

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            chunks.append(
                ChunkSource(
                    chunk_id=str(uuid.uuid4()),
                    source_id=path,
                    source_type="code",
                    content=content,
                    metadata={
                        "language": _detect_language(fname),
                        "filename": fname,
                    },
                )
            )

    # 2️⃣ 加载文档（可选）
    if doc_dir:
        for root, _, files in os.walk(doc_dir):
            for fname in files:
                if not fname.endswith((".md", ".txt")):
                    continue

                path = os.path.join(root, fname)

                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                chunks.append(
                    ChunkSource(
                        source_id=path,
                        source_type="doc",
                        uri=path,
                        version="1"
                    )
                )

    return chunks

    def _detect_language(filename: str) -> str:
        if filename.endswith(".py"):
            return "python"
        if filename.endswith(".java"):
            return "java"
        if filename.endswith(".js"):
            return "javascript"
        return "unknown"

