from pydantic import BaseModel
from typing import Optional

class TravelTimeStats(BaseModel):
    medianSeconds: float
    p10Seconds: float
    p90Seconds: float
    minimumSeconds: float

class CameraTransition(BaseModel):
    fromCameraId: str
    toCameraId: str
    reachable: bool
    sampleCount: int
    transitionProbability: float
    travelTime: Optional[TravelTimeStats] = None
