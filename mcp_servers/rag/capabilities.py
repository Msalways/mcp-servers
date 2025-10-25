from embeddings import EmbeddingModel
from ingest import DocumentIngestor
from vectorstore import VectorStore
from fastmcp import FastMCP as Server
from schemas.ingest_schema import IngestResponse
from utils.logger import log
from schemas.query_schema import QueryRequest, QueryResponse
import tempfile
import os
from pathlib import Path

try:
    log.info("Initializing embedding model...")
    embedding_model = EmbeddingModel()
    log.info("Embedding model initialized.")
    log.info("Initializing vectorstore...")
    vectorstore = VectorStore()
    log.info("Vectorstore initialized.")
    log.info("Initializing ingestor...")
    ingestor = DocumentIngestor(embedding_model=embedding_model, vectorstore=vectorstore)
    log.info("Ingestor initialized.")
except Exception as e:
    log.error(f"Failed to initialize components: {e}")
    raise

def setup_capabilities(server: Server):
    """Set up RAG capabilities on the given server."""

    @server.tool(
        description="Embed text content into the RAG vector store"
    )
    def embed_text(text_content: str, title: str, namespace: str = "default") -> dict:
        """Embed text content directly into the RAG vector store"""
        try:
            # Prepare document for chunking
            docs = [{"content": text_content, "path": f"{title}.txt"}]

            # Chunk documents
            chunked_docs = ingestor._chunk_documents(docs)

            # Embed
            embeddings = ingestor.embedding_model.embed(
                [doc['content'] for doc in chunked_docs]
            )

            # Store in vectorstore
            ingestor.vectorstore.add_documents(
                docs=chunked_docs,
                embeddings=embeddings,
                namespace=namespace
            )

            count = len(chunked_docs)
            return {
                "message": "Text content embedded successfully",
                "chunks_processed": count,
                "namespace": namespace
            }
        except Exception as e:
            log.exception(f"Failed to embed text content: {e}")
            raise e

    @server.resource(
        "namespace://list",
        description="List all available namespaces in the vector store"
    )
    def list_namespaces() -> list:
        """List all available namespaces in the vector store"""
        try:
            # Get all collection names from the vector store
            collections = list(vectorstore.collections.keys())
            return collections
        except Exception as e:
            log.exception(f"Failed to list namespaces: {e}")
            raise e

    @server.tool(
        description="Query RAG vector store across all namespaces"
    )
    def query_all_docs(query: str, k: int = 5) -> dict:
        """Query the RAG vector store for relevant documents across all namespaces"""
        try:
            q_emb = embedding_model.embed_query(query)
            all_contexts = []
            all_sources = []
            namespaces = list(vectorstore.collections.keys())
            if not namespaces:
                return QueryResponse(contexts=[], sources=[]).model_dump()
            per_namespace_k = max(1, k // len(namespaces))
            for ns in namespaces:
                contexts, sources = vectorstore.similarity_search(
                    namespace=ns,
                    query_embedding=q_emb,
                    k=per_namespace_k
                )
                all_contexts.extend(contexts)
                all_sources.extend(sources)
            # Take top k overall - since no scores, just slice
            contexts = all_contexts[:k]
            sources = all_sources[:k]
            return QueryResponse(contexts=contexts, sources=sources).model_dump()
        except Exception as e:
            log.exception(f"Query failed: {e}")
            raise e

    @server.tool(
        description="Query RAG vector store within a specific namespace"
    )
    def query_namespace(query: str, namespace: str, k: int = 5) -> dict:
        """Query the RAG vector store for relevant documents within a specific namespace"""
        try:
            q_emb = embedding_model.embed_query(query)
            contexts, sources = vectorstore.similarity_search(
                namespace=namespace,
                query_embedding=q_emb,
                k=k
            )
            return QueryResponse(contexts=contexts, sources=sources).model_dump()
        except Exception as e:
            log.exception(f"Query failed: {e}")
            raise e
