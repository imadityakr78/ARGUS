"""
Vision Pipeline Interfaces — Adapter Protocols

These define the contracts that Member 1 must implement.
The architecture is model-agnostic: any detector/tracker/Re-ID model
that conforms to these protocols can be plugged in.

Candidate implementations:
  Detector: YOLO, RT-DETR
  Tracker:  ByteTrack, BoT-SORT
  Re-ID:    OSNet, YoutuReID

Owner: Member 1
"""
from typing import Protocol, List
from argus_contracts import Observation, Track, BoundingBox


class DetectorAdapter(Protocol):
    """Produces bounding-box detections from a single video frame."""

    def detect(self, frame_bytes: bytes, camera_id: str, timestamp_ms: int) -> List[Observation]:
        """
        Args:
            frame_bytes: Raw image bytes (e.g. decoded JPEG/PNG).
            camera_id: Which camera captured this frame.
            timestamp_ms: Frame timestamp in epoch milliseconds.
        Returns:
            List of Observation objects with bounding boxes and confidence.
        """
        ...


class TrackerAdapter(Protocol):
    """Associates detections across frames into persistent tracks."""

    def update(self, observations: List[Observation]) -> List[Track]:
        """
        Args:
            observations: New detections for the current frame.
        Returns:
            Updated list of active tracks.
        """
        ...


class ReIdAdapter(Protocol):
    """Generates appearance embeddings for cross-camera matching."""

    def embed(self, frame_bytes: bytes, bbox: BoundingBox) -> str:
        """
        Args:
            frame_bytes: Full frame image.
            bbox: Crop region for the entity.
        Returns:
            Reference ID to the stored embedding (not the embedding itself).
        """
        ...

    def compare(self, embedding_ref_a: str, embedding_ref_b: str) -> float:
        """
        Returns:
            Similarity score between 0.0 and 1.0.
        """
        ...


# ---------------------------------------------------------------------------
# Mock implementations (for testing without GPU/models)
# ---------------------------------------------------------------------------

class MockDetector:
    """Returns empty detections. TODO(member1): replace with real model."""

    def detect(self, frame_bytes: bytes, camera_id: str, timestamp_ms: int) -> List[Observation]:
        return []


class MockTracker:
    """Returns empty tracks. TODO(member1): replace with real tracker."""

    def update(self, observations: List[Observation]) -> List[Track]:
        return []


class MockReId:
    """Returns dummy similarity. TODO(member1): replace with real Re-ID."""

    def embed(self, frame_bytes: bytes, bbox: BoundingBox) -> str:
        return "mock_embedding_ref"

    def compare(self, embedding_ref_a: str, embedding_ref_b: str) -> float:
        return 0.5
