"""
ARGUS API — FastAPI backend
Owner: Member 3

Routes serve mock data when ARGUS_USE_MOCKS=true (default).
When mocks are disabled, unimplemented routes return 501.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
from pathlib import Path

# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="ARGUS API",
    description="Evidence-Aware Event Reconstruction API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.environ.get("API_CORS_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MOCKS_DIR = Path(__file__).parent.parent.parent.parent / "mocks"


class ArgusError(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None


def _use_mocks() -> bool:
    return os.environ.get("ARGUS_USE_MOCKS", "true").lower() == "true"


def _load_mock(relpath: str):
    mock_file = MOCKS_DIR / relpath
    if mock_file.exists():
        with open(mock_file, "r") as f:
            return json.load(f)
    return None


def _not_implemented(resource: str):
    raise HTTPException(
        status_code=501,
        detail=ArgusError(
            code="NOT_IMPLEMENTED",
            message=f"{resource} is not implemented outside mock mode.",
        ).model_dump(),
    )


def _not_found(resource: str, id: str):
    raise HTTPException(
        status_code=404,
        detail=ArgusError(
            code="NOT_FOUND",
            message=f"{resource} '{id}' not found.",
        ).model_dump(),
    )


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.get("/api/health", tags=["system"])
def health_check():
    """System health check."""
    return {"status": "ok", "mock_mode": _use_mocks()}


@app.get("/api/cameras", tags=["cameras"])
def get_cameras():
    """List all cameras. Mock: returns mocks/cameras/cameras.json."""
    if _use_mocks():
        data = _load_mock("cameras/cameras.json")
        return data if data else []
    _not_implemented("Cameras")


@app.get("/api/events", tags=["events"])
def get_events():
    """List all events. Mock: returns mocks/events/events.json."""
    if _use_mocks():
        data = _load_mock("events/events.json")
        return data if data else []
    _not_implemented("Events")


@app.get("/api/events/{event_id}", tags=["events"])
def get_event(event_id: str):
    """Get a single event by ID. Mock: searches events.json."""
    if _use_mocks():
        data = _load_mock("events/events.json")
        if data:
            for evt in data:
                if evt.get("eventId") == event_id:
                    return evt
        _not_found("Event", event_id)
    _not_implemented("Event lookup")


@app.get("/api/camera-graph", tags=["intelligence"])
def get_camera_graph():
    """Get camera adjacency graph. TODO(member2): implement real graph."""
    if _use_mocks():
        cameras = _load_mock("cameras/cameras.json") or []
        return {
            "cameras": cameras,
            "edges": [],  # TODO(member2): populate from CameraGraph
        }
    _not_implemented("Camera graph")


@app.get("/api/event-graph", tags=["intelligence"])
def get_event_graph():
    """Get event relationship graph. TODO(member2): implement real graph."""
    if _use_mocks():
        return {"nodes": [], "edges": []}  # TODO(member2)
    _not_implemented("Event graph")


@app.post("/api/investigations", tags=["investigations"])
def create_investigation(request: dict):
    """
    Create an investigation from a question.
    Mock: returns the golden demo investigation.
    TODO(member3): implement real agent orchestration.
    """
    if _use_mocks():
        data = _load_mock("investigations/inv_001.json")
        if data:
            return data
        _not_found("Investigation", "inv_001")
    _not_implemented("Investigation creation")


@app.get("/api/investigations/{investigation_id}", tags=["investigations"])
def get_investigation(investigation_id: str):
    """Get a completed investigation by ID."""
    if _use_mocks():
        data = _load_mock(f"investigations/{investigation_id}.json")
        if data:
            return data
        _not_found("Investigation", investigation_id)
    _not_implemented("Investigation lookup")


@app.get("/api/evidence/{evidence_id}", tags=["evidence"])
def get_evidence(evidence_id: str):
    """Get a single evidence item. TODO(member3): implement."""
    _not_implemented("Evidence lookup")


@app.get("/api/hypotheses/{investigation_id}", tags=["hypotheses"])
def get_hypotheses(investigation_id: str):
    """Get hypotheses for an investigation. Mock: returns hypotheses.json."""
    if _use_mocks():
        data = _load_mock("hypotheses/hypotheses.json")
        return data if data else []
    _not_implemented("Hypotheses lookup")
