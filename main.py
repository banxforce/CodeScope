from codescope.domain.requirement import Requirement
from codescope.pipeline.build_instruction import build_instruction


def main():
    text = input("请输入你的需求：")
    template_type = input("选择模板类型 (java_backend/python_script)：") or "java_backend"

    req = Requirement(raw_text=text)
    instruction = build_instruction(req, template_type)

    md = instruction.to_markdown()
    print("\n===== Generated Codex Instruction =====\n")
    print(md)


if __name__ == "__main__":
    main()
