from pydantic import BaseModel

class EntityCounts(BaseModel):

    person: int = 0
    email: int = 0
    phone: int = 0
    id: int = 0
    address: int = 0
    date: int = 0


class RedactResponse(BaseModel):
    success: bool
    redacted_text: str
    entity_counts: EntityCounts
    total_entities: int
    processing_time_ms: float

class RestoreResponse(BaseModel):
    success: bool
    restored_text: str
    entity_counts: EntityCounts
    total_entities: int
    processing_time_ms: float