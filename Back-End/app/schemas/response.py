from pydantic import BaseModel

class RedactResponse(BaseModel):
    success: bool
    redacted_text: str