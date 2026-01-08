from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Instruction:
    """
    发送给 Codex 的指令模型（编译产物）
    """
    role: str
    task: str

    constraints: List[str] = field(default_factory=list)
    context: Optional[str] = None
    output_requirements: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """
        编译为 Codex 友好的 Markdown 指令
        """
        lines = []

        lines.append("# Role")
        lines.append(self.role)
        lines.append("")

        lines.append("# Task")
        lines.append(self.task)
        lines.append("")

        if self.constraints:
            lines.append("# Constraints")
            for c in self.constraints:
                lines.append(f"- {c}")
            lines.append("")

        if self.context:
            lines.append("# Context")
            lines.append(self.context)
            lines.append("")

        if self.output_requirements:
            lines.append("# Output Requirements")
            for r in self.output_requirements:
                lines.append(f"- {r}")
            lines.append("")

        return "\n".join(lines)
