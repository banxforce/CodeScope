from langchain_community.vectorstores import FAISS
from langchain_community.docstore.document import Document

class TemplateRetriever:
    def __init__(self, vectorstore):
        self.vectorstore = vectorstore

    def retrieve(self, query: str):
        # 返回最相似的模板文本
        results = self.vectorstore.similarity_search(query, k=1)
        return results[0].page_content

