from codescope.config.settings import settings
from codescope.llm.openai_like import OpenAILikeClient
from codescope.pipeline.semantic_execution_pipeline import SemanticExecutionPipeline
from codescope.rag.vector_store_compiler import VectorStoreCompiler
from codescope.rag.faiss_vector_store import FAISSVectorStore
from codescope.pipeline.builders.generation_input_builder import GenerationInputBuilder
from codescope.pipeline.generation_executor import GenerationExecutor
from codescope.prompt.generation_prompt_builder import GenerationPromptBuilder
from codescope.output.markdown_writer import MarkdownWriter
from codescope.rag.index_bootstrap import build_vector_index

# 将 runner 的获取抽成一个方法
def get_runner() -> SemanticExecutionPipeline:
    llm_client = get_llm_client()

    return SemanticExecutionPipeline(
        llm=llm_client,
    )


def get_llm_client() -> OpenAILikeClient:
    """创建并返回配置好的 SemanticExecutionPipeline 实例"""
    llm_client = OpenAILikeClient(
        api_key=settings.llm_api_key,
        base_url=settings.llm_base_url,
        model=settings.llm_model,
    )
    return llm_client


if __name__ == "__main__":
    # 1️⃣ 获取 runner（raw_text → RetrievalQuery）
    runner = get_runner()

    raw_text2 = "看看 UserService 里是怎么做用户登录校验的。"

    queries = runner.run(raw_text2)

    # 2️⃣ VectorStore + Compiler（Retrieval 阶段）
    vector_store = FAISSVectorStore()

    build_vector_index(vector_store)

    compiler = VectorStoreCompiler(vector_store)

    retrieval_results = []
    for query in queries:
        result = compiler.execute(query)
        retrieval_results.append(result)

    # 3️⃣ 构建 GenerationInput
    generation_input_builder = GenerationInputBuilder(
        task=queries[0].task,   # 或 runner 输出的 SemanticTask
        top_k=5,
        min_confidence=0.0,
    )

    gen_input = generation_input_builder.build(retrieval_results)

    executor = GenerationExecutor(
        llm_client=get_llm_client(),
        prompt_builder=GenerationPromptBuilder()
    )

    # 5️⃣ 执行生成
    generation_result = executor.execute(gen_input)

    # 6️⃣ 输出结果
    print("====== 最终生成结果 ======")
    print(generation_result.content)

    output_dir = r"D:\PythonProj\CodeScope\target"
    # 7️⃣ 写入 markdown 文件
    writer = MarkdownWriter(output_dir=output_dir)

    md_path = writer.write(generation_result)

    print(f"结果已写入 Markdown 文件: {md_path}")
