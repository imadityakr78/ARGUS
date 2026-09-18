from pydantic import BaseModel
from typing import List, Optional

class Track(BaseModel):
    trackId: str
    cameraId: str
    startTimestampMs: int
    endTimestampMs: int
    observationIds: List[str]
    entityType: str
    appearanceEmbeddingRef: Optional[str] = None
    qualityScore: float
