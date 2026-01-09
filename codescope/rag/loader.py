from langchain_community.docstore.document import Document
from pathlib import Path

def load_templates(template_dir: str):
    docs = []
    for file in Path(template_dir).glob("*.md"):
        content = file.read_text(encoding="utf-8")
        docs.append(Document(page_content=content, metadata={"name": file.stem}))
    return docs
