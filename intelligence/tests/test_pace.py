import pytest
from intelligence.pace.travel_time import (
    check_travel_time,
    check_reachability,
    check_candidate_journey,
)
from argus_contracts.reid import PaceCheckStatus


def test_check_travel_time_fail_impossible_journey():
    """Canonical demo: Person travels 140m in 16 seconds (min time 100s)."""
    result = check_travel_time(
        distance_meters=140.0,
        available_seconds=16.0,
        min_travel_seconds=100.0,
    )
    assert result.status == PaceCheckStatus.FAIL
    assert result.availableTravelSeconds == 16.0
    assert result.requiredTravelSeconds == 100.0
    assert "could not plausibly travel 140.0 metres in 16.0 seconds" in result.reason


def test_check_travel_time_pass_plausible_journey():
    result = check_travel_time(
        distance_meters=20.0,
        available_seconds=30.0,
        min_travel_seconds=15.0,
    )
    assert result.status == PaceCheckStatus.PASS


def test_check_reachability_returns_unknown():
    """Stub check must return UNKNOWN until Member 2 implements it."""
    result = check_reachability("CAM_01", "CAM_02")
    assert result.status == PaceCheckStatus.UNKNOWN


def test_check_candidate_journey_delegates_to_travel_time():
    result = check_candidate_journey(
        appearance_similarity=0.91,
        distance_meters=140.0,
        available_seconds=16.0,
        min_travel_seconds=100.0,
    )
    assert result.status == PaceCheckStatus.FAIL
