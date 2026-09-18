from pydantic import BaseModel
from typing import List, Optional
from .epistemic import EpistemicState

class Participant(BaseModel):
    entityType: str
    entityId: str

class Event(BaseModel):
    eventId: str
    type: str
    cameraId: str
    startTimestampMs: int
    endTimestampMs: int
    participants: List[Participant]
    supportingObservationIds: List[str]
    epistemicState: EpistemicState
    confidence: float
    description: str
