from enum import Enum

class EpistemicState(str, Enum):
    OBSERVED = "OBSERVED"
    INFERRED = "INFERRED"
    UNKNOWN = "UNKNOWN"
    REJECTED = "REJECTED" # Typically used for hypotheses rejected by PACE
