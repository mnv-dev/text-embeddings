from typing import List

from pydantic import BaseModel, Field

class EmbedRequest(BaseModel):
    text: str = Field(min_length=1)

class EmbedResponse(BaseModel):
    text:str
    embedding: List[float]
    dimension: int