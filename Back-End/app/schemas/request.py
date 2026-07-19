from pydantic import BaseModel

class RedactRequest(BaseModel):
    text: str