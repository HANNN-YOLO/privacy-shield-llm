from pydantic import BaseModel

class RedactRequest(BaseModel):
    text: str

class RestoreRequest(BaseModel):
    text: str