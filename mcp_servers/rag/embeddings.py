import logging
from typing import List, Union
from sentence_transformers import SentenceTransformer

# Suppress sentence_transformers debug/info logs to avoid stdout pollution
logging.getLogger('sentence_transformers').setLevel(logging.WARNING)

class EmbeddingModel:
    """
    Wrapper around an embedding model
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
    
    def embed(self, texts: Union[str, List[str]]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=False).tolist()
    
    def embed_query(self, text: str) -> List[float]:
        embedded = self.model.encode(text, show_progress_bar=False)
        return embedded.tolist()
