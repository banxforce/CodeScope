from codescope.rag.faiss_vector_store import FAISSVectorStore
from .loader import load_chunks_from_project


def build_vector_index(vector_store: FAISSVectorStore):
    """
    系统启动时调用
    """
    chunks = load_chunks_from_project(
        code_dir="src",
        doc_dir="docs",
    )

    vector_store.add_chunks(chunks)
