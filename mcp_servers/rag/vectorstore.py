
import os
from typing import List, Dict, Optional
from chromadb import Client
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from utils.logger import log

DEFAULT_DB_DIR = os.path.expanduser("~/.loopmind_chroma")

class VectorStore:
    """
    Handles ChromaDB vector store and retrive operation    
    """
    
    def __init__(self, persist_directory: Optional[str] = DEFAULT_DB_DIR):
        if persist_directory is None:
            persist_directory = DEFAULT_DB_DIR
        os.makedirs(persist_directory, exist_ok=True)
        self.client = Client(Settings(
            is_persistent=True,
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        self.persist_directory = persist_directory
        self.collections = {}
        
    def get_collection(self, namespace: str = "default"):
        """Returns or creates a collection"""
        if namespace not in self.collections:
            self.collections[namespace] = self.client.get_or_create_collection(name=namespace)
        return self.collections[namespace]
    
    def add_documents(self, namespace:str, docs: List[Dict[str,str]], embeddings:List[List[float]]):
        """Add documents with embeddings to chroma collections"""
        collection = self.get_collection(namespace)
        ids = [f'doc-{i}' for i in range(len(docs))]
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=[d["content"] for d in docs],
            metadatas=[{"path":d["path"]} for d in docs]            
        )
        log.info(f"Added {len(docs)} documents to namespace '{namespace}'")
    
    def similarity_search(self, namespace: str, query_embedding: List[float], k: int =5) -> tuple[List[str], List[str]]:
        """Perform similarity search in the vectorstore"""
        collection = self.get_collection(namespace)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        context = results["documents"][0]
        sources = [m["path"] for m in results["metadatas"][0]]
        return context, sources
