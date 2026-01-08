from codescope.config.settings import INSTRUCTION_TEMPLATES
from codescope.domain.requirement import Requirement
from codescope.domain.instruction import Instruction


def build_instruction(req: Requirement, template_type="java_backend") -> Instruction:

    """
    根据模板类型生成 Instruction
    """
    template = INSTRUCTION_TEMPLATES.get(template_type, INSTRUCTION_TEMPLATES["java_backend"])

    return Instruction(
        role=template["role"],
        task=req.raw_text,
        constraints=template["constraints"],
        output_requirements=template["output_requirements"]
    )

