# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.vectorstores import FAISS

def build_vectorstore(docs):
    # embedding = OpenAIEmbeddings()  # 或自己用本地 embedding
    embedding = FastEmbedEmbeddings()
    vectorstore = FAISS.from_documents(docs, embedding)
    return vectorstore
