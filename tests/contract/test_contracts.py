"""
Contract invariant tests — validates mock fixture data against canonical schemas.
"""
import json
from pathlib import Path
import pytest
from argus_contracts import (
    Camera, Event, Hypothesis, InvestigationResponse, EpistemicState,
    ReIdCandidate, EvidenceCoverage, PaceCheckStatus,
)

MOCKS_DIR = Path(__file__).parent.parent.parent / "mocks"


def _load_json(relpath: str):
    with open(MOCKS_DIR / relpath, "r") as f:
        return json.load(f)


class TestCameraContract:
    def test_cameras_parse(self):
        raw = _load_json("cameras/cameras.json")
        cameras = [Camera(**c) for c in raw]
        assert len(cameras) >= 3

    def test_camera_has_required_fields(self):
        raw = _load_json("cameras/cameras.json")
        for c in raw:
            cam = Camera(**c)
            assert cam.cameraId
            assert cam.name


class TestEventContract:
    def test_events_parse(self):
        raw = _load_json("events/events.json")
        events = [Event(**e) for e in raw]
        assert len(events) >= 1

    def test_observed_event_has_supporting_observations(self):
        raw = _load_json("events/events.json")
        for e in raw:
            evt = Event(**e)
            if evt.epistemicState == EpistemicState.OBSERVED:
                assert len(evt.supportingObservationIds) > 0, (
                    f"OBSERVED event {evt.eventId} must have supporting observations"
                )


class TestHypothesisContract:
    def test_hypotheses_parse(self):
        raw = _load_json("hypotheses/hypotheses.json")
        hypotheses = [Hypothesis(**h) for h in raw]
        assert len(hypotheses) >= 2

    def test_rejected_hypothesis_has_failed_check(self):
        raw = _load_json("hypotheses/hypotheses.json")
        for h in raw:
            hyp = Hypothesis(**h)
            if hyp.epistemicState == EpistemicState.REJECTED:
                failed = [c for c in hyp.checks if c.status == PaceCheckStatus.FAIL]
                assert len(failed) >= 1, (
                    f"REJECTED hypothesis {hyp.hypothesisId} must have at least one FAIL check"
                )


class TestReIdCandidateContract:
    def test_reid_candidates_parse(self):
        raw = _load_json("hypotheses/reid_candidates.json")
        candidates = [ReIdCandidate(**c) for c in raw]
        assert len(candidates) >= 1

    def test_scores_in_valid_range(self):
        raw = _load_json("hypotheses/reid_candidates.json")
        for c in raw:
            cand = ReIdCandidate(**c)
            assert 0.0 <= cand.appearanceSimilarity <= 1.0
            assert 0.0 <= cand.finalScore <= 1.0


class TestInvestigationResponseContract:
    def test_investigation_response_parses(self):
        raw = _load_json("investigations/inv_001.json")
        resp = InvestigationResponse(**raw)
        assert resp.investigationId == "inv_001"

    def test_coverage_fractions_valid(self):
        raw = _load_json("investigations/inv_001.json")
        resp = InvestigationResponse(**raw)
        cov = resp.coverage
        assert 0.0 <= cov.observedFraction <= 1.0
        assert 0.0 <= cov.inferredFraction <= 1.0
        assert 0.0 <= cov.unknownFraction <= 1.0
        total = cov.observedFraction + cov.inferredFraction + cov.unknownFraction
        assert abs(total - 1.0) < 0.01, f"Coverage fractions must sum to ~1.0, got {total}"

    def test_inferred_claims_have_supporting_events(self):
        raw = _load_json("investigations/inv_001.json")
        resp = InvestigationResponse(**raw)
        for claim in resp.claims:
            if claim.epistemicState == EpistemicState.INFERRED:
                assert len(claim.supportingEventIds) > 0, (
                    f"INFERRED claim {claim.claimId} must have supporting events"
                )
