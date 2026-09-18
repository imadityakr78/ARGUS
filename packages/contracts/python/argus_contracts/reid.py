from enum import Enum
from pydantic import BaseModel
from typing import Optional

class PaceCheckStatus(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    UNKNOWN = "UNKNOWN"

class PhysicalConsistency(BaseModel):
    status: PaceCheckStatus
    requiredTravelSeconds: Optional[float] = None
    availableTravelSeconds: Optional[float] = None
    distanceMeters: Optional[float] = None
    reason: Optional[str] = None

class ReIdCandidate(BaseModel):
    sourceTrackId: str
    candidateTrackId: str
    appearanceSimilarity: float
    physicalConsistency: PhysicalConsistency
    transitionLikelihood: float
    directionScore: float
    finalScore: float
