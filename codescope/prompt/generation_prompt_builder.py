class GenerationPromptBuilder:
    """
    将 GenerationInput 转换为 LLM Prompt
    """

    def build(self, gen_input: "GenerationInput") -> str:
        task = gen_input.task
        retrieval = gen_input.retrieval_result
        output_spec = gen_input.output_spec

        evidence_blocks = []
        for idx, chunk in enumerate(retrieval.chunks, start=1):
            evidence_blocks.append(
                f"[Evidence {idx} | {chunk.source_type}:{chunk.source_id}]\n"
                f"{chunk.content}"
            )

        evidence_text = "\n\n".join(evidence_blocks)

        constraints_text = "\n".join(
            f"- {c.rule}" for c in task.constraints
        )

        quality_text = "\n".join(
            f"- {q}" for q in output_spec.quality_requirements
        )

        prompt = f"""
你正在执行一个任务。

【任务意图】
{task.intent}

【可用参考资料】
{evidence_text}

【约束条件】
{constraints_text}

【输出要求】
- 输出类型: {output_spec.output_type}
{quality_text}

请严格基于参考资料完成任务，不要编造不存在的信息。
"""

        return prompt.strip()
