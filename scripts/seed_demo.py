"""
Seed the golden demo mock fixtures.

Reads no external data — generates canonical JSON from Pydantic models.
All output goes to mocks/ using pathlib (no absolute paths).

Run: python scripts/seed_demo.py
"""
import json
from pathlib import Path

from argus_contracts import (
    Camera, Position, InvestigationResponse,
    Claim, EpistemicState, Event, Participant, Hypothesis, PaceCheck,
    PaceCheckStatus, EvidenceCoverage, ReIdCandidate, PhysicalConsistency,
    CameraTransition, TravelTimeStats,
)


def seed_demo():
    mocks_dir = Path(__file__).parent.parent / "mocks"

    # --- Cameras ---
    cameras = [
        Camera(cameraId="CAM_01", name="Library Desk Area", zone="Library", floor=1, position=Position(x=12.4, y=8.1, z=3.2)),
        Camera(cameraId="CAM_02", name="Corridor", zone="Hallway", floor=1, position=Position(x=30.0, y=8.0, z=3.0)),
        Camera(cameraId="CAM_03", name="Exit", zone="Lobby", floor=1, position=Position(x=50.0, y=10.0, z=3.0)),
        Camera(cameraId="CAM_04", name="South Annex", zone="Annex", floor=1, position=Position(x=150.0, y=10.0, z=3.0)),
    ]
    _write(mocks_dir / "cameras" / "cameras.json", [c.model_dump() for c in cameras])

    # --- Camera Transitions ---
    transitions = [
        CameraTransition(
            fromCameraId="CAM_01", toCameraId="CAM_02", reachable=True,
            sampleCount=683, transitionProbability=0.74,
            travelTime=TravelTimeStats(medianSeconds=31, p10Seconds=24, p90Seconds=48, minimumSeconds=20),
        ),
        CameraTransition(
            fromCameraId="CAM_02", toCameraId="CAM_03", reachable=True,
            sampleCount=412, transitionProbability=0.62,
            travelTime=TravelTimeStats(medianSeconds=45, p10Seconds=35, p90Seconds=70, minimumSeconds=28),
        ),
        CameraTransition(
            fromCameraId="CAM_01", toCameraId="CAM_04", reachable=True,
            sampleCount=15, transitionProbability=0.08,
            travelTime=TravelTimeStats(medianSeconds=120, p10Seconds=100, p90Seconds=180, minimumSeconds=100),
        ),
    ]
    _write(mocks_dir / "transitions" / "transitions.json", [t.model_dump() for t in transitions])

    # --- Events ---
    events = [
        Event(
            eventId="evt_01", type="PERSON_APPROACHED_OBJECT", cameraId="CAM_01",
            startTimestampMs=1726659125000, endTimestampMs=1726659132000,
            participants=[Participant(entityType="person", entityId="track_17"), Participant(entityType="object", entityId="laptop_02")],
            supportingObservationIds=["obs_01", "obs_02"], epistemicState=EpistemicState.OBSERVED,
            confidence=0.92, description="A person approached the desk containing Laptop_02.",
        ),
        Event(
            eventId="evt_02", type="OBJECT_DISAPPEARED", cameraId="CAM_01",
            startTimestampMs=1726659135000, endTimestampMs=1726659145000,
            participants=[Participant(entityType="object", entityId="laptop_02")],
            supportingObservationIds=["obs_03"], epistemicState=EpistemicState.OBSERVED,
            confidence=0.95, description="The laptop was no longer visible.",
        ),
        Event(
            eventId="evt_03", type="PERSON_APPEARED", cameraId="CAM_02",
            startTimestampMs=1726659185000, endTimestampMs=1726659200000,
            participants=[Participant(entityType="person", entityId="track_18")],
            supportingObservationIds=["obs_04"], epistemicState=EpistemicState.OBSERVED,
            confidence=0.88, description="A visually similar person appeared on CAM_02.",
        ),
    ]
    _write(mocks_dir / "events" / "events.json", [e.model_dump() for e in events])

    # --- Re-ID Candidates ---
    candidates = [
        ReIdCandidate(
            sourceTrackId="track_17", candidateTrackId="track_18",
            appearanceSimilarity=0.87,
            physicalConsistency=PhysicalConsistency(status=PaceCheckStatus.PASS, requiredTravelSeconds=20.0, availableTravelSeconds=53.0, distanceMeters=18.0),
            transitionLikelihood=0.74, directionScore=0.80, finalScore=0.84,
        ),
        ReIdCandidate(
            sourceTrackId="track_17", candidateTrackId="track_99",
            appearanceSimilarity=0.91,
            physicalConsistency=PhysicalConsistency(
                status=PaceCheckStatus.FAIL, requiredTravelSeconds=100.0, availableTravelSeconds=16.0,
                distanceMeters=140.0, reason="The subject could not plausibly travel 140 metres in 16 seconds.",
            ),
            transitionLikelihood=0.01, directionScore=0.5, finalScore=0.10,
        ),
    ]
    _write(mocks_dir / "hypotheses" / "reid_candidates.json", [c.model_dump() for c in candidates])

    # --- Hypotheses ---
    hyp1 = Hypothesis(
        hypothesisId="hyp_001", description="The subject moved from CAM_01 to CAM_02 through the Corridor.",
        epistemicState=EpistemicState.INFERRED, score=0.84,
        supportingEventIds=["evt_01", "evt_03"], supportingObservationIds=["obs_01", "obs_04"],
        route=["CAM_01", "CORRIDOR", "CAM_02"],
        checks=[PaceCheck(type="PHYSICAL_TIME", status=PaceCheckStatus.PASS), PaceCheck(type="REID", status=PaceCheckStatus.PASS)],
    )
    hyp2 = Hypothesis(
        hypothesisId="hyp_002", description="The subject moved from CAM_01 to CAM_04.",
        epistemicState=EpistemicState.REJECTED, score=0.10,
        supportingEventIds=["evt_01"], supportingObservationIds=["obs_01"],
        route=["CAM_01", "UNKNOWN", "CAM_04"],
        checks=[PaceCheck(type="PHYSICAL_TIME", status=PaceCheckStatus.FAIL, reason="Impossible travel time (140m in 16s)")],
    )
    _write(mocks_dir / "hypotheses" / "hypotheses.json", [h.model_dump() for h in [hyp1, hyp2]])

    # --- Investigation Response ---
    response = InvestigationResponse(
        investigationId="inv_001",
        summary="Investigation into the missing laptop on Desk 4.",
        claims=[
            Claim(claimId="claim_01", description="A person approached Desk 4.", epistemicState=EpistemicState.OBSERVED, supportingEventIds=["evt_01"]),
            Claim(claimId="claim_02", description="The laptop was not visible afterward.", epistemicState=EpistemicState.OBSERVED, supportingEventIds=["evt_02"]),
            Claim(claimId="claim_03", description="A candidate trajectory connects CAM_01 and CAM_02.", epistemicState=EpistemicState.INFERRED, supportingEventIds=["evt_01", "evt_03"]),
        ],
        events=events,
        hypotheses=[hyp1],
        rejectedHypotheses=[hyp2],
        coverage=EvidenceCoverage(observedFraction=0.68, inferredFraction=0.16, unknownFraction=0.16),
        unknowns=["No camera covered the corridor section for 53 seconds."],
        evidence=[],
        warnings=["This is an evidence reconstruction, not a determination of guilt. Human review is required."],
    )
    _write(mocks_dir / "investigations" / "inv_001.json", response.model_dump())

    print("Successfully seeded mock data!")


def _write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    seed_demo()
