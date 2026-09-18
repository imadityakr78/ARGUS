"""
PACE — Physical & Causal Evidence Engine

Deterministic verification of physical constraints on candidate journeys.
PACE is NEVER probabilistic. It returns PASS, FAIL, or NOT_IMPLEMENTED.
No LLM may override a PACE decision.

Owner: Member 2
"""
from argus_contracts.reid import PaceCheckStatus, PhysicalConsistency


def check_travel_time(
    distance_meters: float,
    available_seconds: float,
    min_travel_seconds: float,
) -> PhysicalConsistency:
    """
    Checks if a candidate journey is physically possible based on distance and time.
    IMPLEMENTED — verified by tests.
    """
    if available_seconds < min_travel_seconds:
        return PhysicalConsistency(
            status=PaceCheckStatus.FAIL,
            requiredTravelSeconds=min_travel_seconds,
            availableTravelSeconds=available_seconds,
            distanceMeters=distance_meters,
            reason=(
                f"The subject could not plausibly travel "
                f"{distance_meters} metres in {available_seconds} seconds."
            ),
        )

    return PhysicalConsistency(
        status=PaceCheckStatus.PASS,
        requiredTravelSeconds=min_travel_seconds,
        availableTravelSeconds=available_seconds,
        distanceMeters=distance_meters,
    )


def check_reachability(
    from_camera_id: str,
    to_camera_id: str,
) -> PhysicalConsistency:
    """
    Checks if a physical path exists between two cameras.
    TODO(member2): Implement using CameraGraph.
    """
    return PhysicalConsistency(
        status=PaceCheckStatus.UNKNOWN,
        reason="check_reachability is not yet implemented.",
    )


def check_temporal_overlap(
    track_a_start_ms: int,
    track_a_end_ms: int,
    track_b_start_ms: int,
    track_b_end_ms: int,
) -> PhysicalConsistency:
    """
    Rejects candidates that appear on two distant cameras simultaneously.
    TODO(member2): Implement overlap detection.
    """
    return PhysicalConsistency(
        status=PaceCheckStatus.UNKNOWN,
        reason="check_temporal_overlap is not yet implemented.",
    )


def check_direction_consistency() -> PhysicalConsistency:
    """
    Validates entry/exit vectors are consistent with camera topology.
    TODO(member2): Implement using camera FOV metadata.
    """
    return PhysicalConsistency(
        status=PaceCheckStatus.UNKNOWN,
        reason="check_direction_consistency is not yet implemented.",
    )


def check_contradictions() -> PhysicalConsistency:
    """
    Checks for mutually exclusive observations (e.g. same entity in two places).
    TODO(member2): Implement contradiction detection.
    """
    return PhysicalConsistency(
        status=PaceCheckStatus.UNKNOWN,
        reason="check_contradictions is not yet implemented.",
    )


def check_candidate_journey(
    appearance_similarity: float,
    distance_meters: float,
    available_seconds: float,
    min_travel_seconds: float,
) -> PhysicalConsistency:
    """
    Composite check: runs travel_time and future checks on a Re-ID candidate.
    Currently delegates to check_travel_time only.
    TODO(member2): Add reachability, direction, contradiction checks.
    """
    return check_travel_time(distance_meters, available_seconds, min_travel_seconds)
