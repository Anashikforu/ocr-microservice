from pydantic import BaseModel, Field
from fastapi import Body
from typing import Optional,Annotated

class OCRRequest(BaseModel):
    data: Annotated[str, Body(..., description="data")] = Field(..., description="Base64-encoded image data")

class OCRResponseSync(BaseModel):
    text: str = Field(..., description="OCR text")
    entities: list = Field(..., description="List of named entities")
    sentiment_polarity: float = Field(..., description="Sentiment Polarity score")
    sentiment_subjectivity: float = Field(..., description="Sentiment Subjectivity score")


class OCRResponseAsync(BaseModel):
    job_id: str = Field(..., description="Unique identifier for the OCR job")
    status: str = Field(..., description="Current status of the OCR job")
    result: Optional[OCRResponseSync] = Field(None, description="Job result")