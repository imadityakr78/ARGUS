from pydantic import BaseModel
from typing import Optional
from .epistemic import EpistemicState

class BoundingBox(BaseModel):
    x: float
    y: float
    width: float
    height: float

class VideoSource(BaseModel):
    videoId: str
    clipStartMs: int
    clipEndMs: int

class Observation(BaseModel):
    observationId: str
    cameraId: str
    timestampMs: int
    frameId: Optional[int] = None
    entityType: str
    localTrackId: str
    bbox: Optional[BoundingBox] = None
    confidence: float
    epistemicState: EpistemicState = EpistemicState.OBSERVED
    source: Optional[VideoSource] = None
