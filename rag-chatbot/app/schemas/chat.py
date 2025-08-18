from pydantic import BaseModel
from typing import List, Optional

class ChatRequest(BaseModel):
    query: str
    domain: str = "default"

class SourceDocument(BaseModel):
    source: str
    content: str
    metadata: Optional[dict] = None

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceDocument]
