from codescope.domain.requirement import Requirement
from codescope.pipeline.build_instruction import build_instruction
from codescope.rag.embedder import build_vectorstore
from codescope.rag.loader import load_templates
from codescope.rag.retriever import TemplateRetriever


def main():
    # 1. 加载模板
    docs = load_templates("data/templates")
    vectorstore = build_vectorstore(docs)
    retriever = TemplateRetriever(vectorstore)

    # 2. 输入需求
    text = input("请输入需求: ")
    req = Requirement(raw_text=text)

    # 3. 生成指令
    instruction = build_instruction(req, retriever)
    print("\n===== Generated Codex Instruction =====\n")
    print(instruction.to_markdown())


if __name__ == "__main__":
    main()
