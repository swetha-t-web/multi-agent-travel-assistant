from pathlib import Path
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from app.config import EMBED_MODEL
def build_vectorstore():
    data_path = Path("data/travel_knowledge.txt")
    text = data_path.read_text(encoding="utf-8")

    docs = [Document(page_content=chunk.strip()) for chunk in text.split("\n\n") if chunk.strip()]

    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore