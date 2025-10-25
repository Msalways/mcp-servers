from embeddings import EmbeddingModel
from vectorstore import VectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List, Dict
from utils.logger import log
from utils.file_loader import load_documents

class DocumentIngestor:
    """
    Handles the ingestion of documents into the vectorstore.
    """
    
    def __init__(self, embedding_model:EmbeddingModel, 
                 vectorstore:VectorStore,
                 chunk_size:int=500,
                 chunk_overlap:int=50):
        self.embedding_model = embedding_model
        self.vectorstore = vectorstore
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
    def _chunk_documents(self, docs: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Splits documents into smaller chunks.
        """
        chunked_docs = []
        for doc in docs:
            text = doc['content']
            chunks = self.splitter.split_text(text)
            for i,chunk in enumerate(chunks):
                chunked_docs.append({'content': chunk, 
                                     'path': f"{doc["path"]}#chunk{i}"
                                    })
        log.info(f"Chunked {len(docs)} documents into {len(chunked_docs)} chunks.")
        return chunked_docs
    
    def ingest(self, paths: List[str], namespace: str="default") -> int:
        """
        Loads, chunks, embeds, and ingests documents into the vectorstore.
        """
        log.info(f"[blue]Ingesting documents into namespace '{namespace}'[/blue]")
        
        # Load documents using the standalone function instead of a method
        docs = load_documents(paths)
        if not docs:
            log.warning("[yellow]No documents loaded for ingestion.[/yellow]")
            return 0
        
        # Chunk documents
        chunked_docs = self._chunk_documents(docs)
        
        # Embed
        embeddings = self.embedding_model.embed(
            [doc['content'] for doc in chunked_docs]
        )
        
        # Store in vectorstore
        self.vectorstore.add_documents(
            docs=chunked_docs,
            embeddings=embeddings,
            namespace=namespace
        )
        
        log.info(f"[green]Ingested {len(chunked_docs)} chunks into namespace '{namespace}'[/green]")
        return len(chunked_docs)
