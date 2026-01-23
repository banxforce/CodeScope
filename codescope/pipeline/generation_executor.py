from codescope.domain.semantic_models import GenerationInput, GenerationResult
from codescope.llm.client import LLMClient
from codescope.prompt.generation_prompt_builder import GenerationPromptBuilder


class GenerationExecutor:

    def __init__(
        self,
        llm_client: LLMClient,
        prompt_builder: GenerationPromptBuilder
    ):
        self.llm_client = llm_client
        self.prompt_builder = prompt_builder

    def execute(self, gen_input: GenerationInput) -> GenerationResult:
        prompt = self.prompt_builder.build(gen_input)
        output = self.llm_client.generate(prompt)

        used_chunk_ids = [
            c.chunk_id for c in gen_input.retrieval_result.chunks
        ]

        return GenerationResult(
            task_id=gen_input.task.task_id,
            content=output,
            used_chunks=used_chunk_ids,
            confidence=gen_input.retrieval_result.confidence
        )
