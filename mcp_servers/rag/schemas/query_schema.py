from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    """Schema for querying vectorstore"""
    query: str = Field(..., description="Query to be passed to vectorstore")
    k: int = Field(default=5, description="Number of results to retrieve")
    namespace: str = Field(default="default", description="Namespace or collection")

class QueryResponse(BaseModel):
    """Schema for returning retrieved contexts."""
    contexts: List[str] = Field(..., description="List of retrieved text snippets.")
    sources: List[str] = Field(..., description="List of source file paths corresponding to contexts.")