from codescope.rag.retriever import TemplateRetriever
from codescope.domain.requirement import Requirement
from codescope.domain.instruction import Instruction


def build_instruction(req: Requirement, retriever: TemplateRetriever) -> Instruction:
    """
    使用 RAG 自动匹配模板生成 Instruction
    """

    def parse_template(md_text: str):
        # 简单解析 Markdown
        role = re.search(r"# Role\n(.+?)(\n#|$)", md_text, re.S).group(1).strip()
        constraints = re.findall(r"- (.+)", re.search(r"# Constraints\n(.+?)(\n#|$)", md_text, re.S).group(1))
        output_reqs = re.findall(r"- (.+)", re.search(r"# Output Requirements\n(.+?)(\n#|$)", md_text, re.S).group(1))
        return role, constraints, output_reqs

    def build_instruction_rag(req: Requirement, retriever):
        template_md = retriever.retrieve(req.raw_text)
        print(f"template:{template_md}")
        role, constraints, output_reqs = parse_template(template_md)
        return Instruction(
            role=role,
            task=req.raw_text,
            constraints=constraints,
            output_requirements=output_reqs
        )
