from pydantic import BaseModel
from typing import List
from .epistemic import EpistemicState
from .reid import PaceCheckStatus

class PaceCheck(BaseModel):
    type: str
    status: PaceCheckStatus
    reason: str = ""

class Hypothesis(BaseModel):
    hypothesisId: str
    description: str
    epistemicState: EpistemicState
    score: float
    supportingEventIds: List[str]
    supportingObservationIds: List[str]
    route: List[str]
    checks: List[PaceCheck]
