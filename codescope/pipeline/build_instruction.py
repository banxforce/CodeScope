from codescope.rag.retriever import TemplateRetriever
from codescope.domain.requirement import Requirement
from codescope.domain.instruction import Instruction
import re
from typing import Tuple


def parse_template(md_text: str) -> Tuple[str, list[str], list[str]]:
    """
    解析模板 Markdown
    """
    if not md_text:
        raise ValueError("template markdown is empty")

    role_match = re.search(r"# Role\n(.+?)(\n#|$)", md_text, re.S)
    constraints_match = re.search(r"# Constraints\n(.+?)(\n#|$)", md_text, re.S)
    output_match = re.search(r"# Output Requirements\n(.+?)(\n#|$)", md_text, re.S)

    if not role_match or not constraints_match or not output_match:
        raise ValueError("template markdown format invalid")

    role = role_match.group(1).strip()
    constraints = re.findall(r"- (.+)", constraints_match.group(1))
    output_reqs = re.findall(r"- (.+)", output_match.group(1))

    return role, constraints, output_reqs


def build_instruction(req: Requirement, retriever: TemplateRetriever) -> Instruction:
    """
    使用 RAG 自动匹配模板生成 Instruction
    """
    if not req or not req.raw_text:
        raise ValueError("Requirement or raw_text is empty")

    if not retriever:
        raise ValueError("TemplateRetriever is None")

    template_md = retriever.retrieve(req.raw_text)
    if not template_md:
        raise ValueError("No template retrieved")

    role, constraints, output_reqs = parse_template(template_md)

    return Instruction(
        role=role,
        task=req.raw_text,
        constraints=constraints,
        output_requirements=output_reqs
    )
