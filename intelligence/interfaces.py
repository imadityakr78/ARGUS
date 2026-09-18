"""
Intelligence Module Interfaces

Clean interfaces for Member 2 to implement.
These use canonical contracts and do NOT depend on Vision internals.

Owner: Member 2
"""
from typing import Protocol, List, Optional, Tuple
from argus_contracts import (
    Camera, CameraTransition, Event, Hypothesis, EvidenceCoverage,
)
from argus_contracts.reid import PhysicalConsistency


class CameraGraphInterface(Protocol):
    """Physical camera topology."""

    def add_camera(self, camera: Camera) -> None: ...
    def add_connection(self, from_id: str, to_id: str, transition: CameraTransition) -> None: ...
    def neighbors(self, camera_id: str) -> List[str]: ...
    def is_reachable(self, from_id: str, to_id: str) -> bool: ...


class MobilityGraphInterface(Protocol):
    """Travel-time estimation between cameras."""

    def get_transition(self, from_id: str, to_id: str) -> Optional[CameraTransition]: ...
    def estimate_travel_window(self, from_id: str, to_id: str) -> Optional[Tuple[float, float]]: ...
    def get_neighbors(self, camera_id: str) -> List[str]: ...


class EventGraphInterface(Protocol):
    """Relationship graph between entities, events, and observations."""

    def add_event(self, event: Event) -> None: ...
    def add_relation(self, from_id: str, to_id: str, relation_type: str) -> None: ...
    def get_related_events(self, event_id: str) -> List[Event]: ...


class ReconstructionEngineInterface(Protocol):
    """Blind-spot route interpolation."""

    def reconstruct_gap(
        self,
        last_camera_id: str,
        last_timestamp_ms: int,
        next_camera_id: str,
        next_timestamp_ms: int,
    ) -> List[Hypothesis]:
        """Returns possible routes through the blind spot."""
        ...


class HypothesisRankerInterface(Protocol):
    """Ranks and compares competing hypotheses."""

    def rank(self, hypotheses: List[Hypothesis]) -> List[Hypothesis]:
        """Returns hypotheses sorted by score descending."""
        ...


class EvidenceCoverageCalculatorInterface(Protocol):
    """Computes how much of an investigation is observed vs inferred vs unknown."""

    def calculate(self, events: List[Event], hypotheses: List[Hypothesis]) -> EvidenceCoverage: ...
