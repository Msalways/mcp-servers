
from pydantic import BaseModel, Field
from typing import List, Optional

class IngestSchema(BaseModel):
    """Schema for ingesting documents."""
    paths: List[str] = Field(..., description="List of file paths to ingest.")
    namespace: Optional[str] = Field(default="default", description="Namespace or collection")
    
class IngestResponse(BaseModel):
    """Schema for ingest response."""
    status: str = Field(..., description="Status of the ingestion process. eg:- sucess or failure")
    count: int = Field(..., description="Number of documents ingested.")