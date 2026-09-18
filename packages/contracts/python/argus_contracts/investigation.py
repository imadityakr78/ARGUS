from pydantic import BaseModel
from typing import List, Optional
from .epistemic import EpistemicState
from .event import Event
from .hypothesis import Hypothesis
from .evidence import EvidenceCoverage

class Claim(BaseModel):
    claimId: str
    description: str
    epistemicState: EpistemicState
    supportingEventIds: List[str]

class InvestigationRequest(BaseModel):
    question: str
    cameraIds: List[str]
    fromTimestampMs: int
    toTimestampMs: int

class InvestigationResponse(BaseModel):
    investigationId: str
    summary: str
    claims: List[Claim]
    events: List[Event]
    hypotheses: List[Hypothesis]
    rejectedHypotheses: List[Hypothesis]
    coverage: EvidenceCoverage
    unknowns: List[str]
    evidence: List[dict] # For any generic evidence items
    warnings: List[str]
