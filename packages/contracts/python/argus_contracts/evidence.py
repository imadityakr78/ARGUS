from pydantic import BaseModel

class EvidenceCoverage(BaseModel):
    observedFraction: float
    inferredFraction: float
    unknownFraction: float
