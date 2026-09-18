# ARGUS Architecture

## System Overview
ARGUS is an epistemic reasoning system layered on top of a vision pipeline. It ingests fragmented camera observations, constructs spatio-temporal graphs, and uses AI agents to form and verify hypotheses about incidents. The architecture separates evidence from inference at every layer.

## End-to-End Data Flow

| Stage | Input | Output | Module | Owner | Status |
|---|---|---|---|---|---|
| Frame Decode | Video file | Raw frames | `vision/ingestion` | Member 1 | SCAFFOLDED |
| Detection | Frame bytes | `Observation[]` | `vision/detector` via `DetectorAdapter` | Member 1 | SCAFFOLDED |
| Tracking | `Observation[]` | `Track[]` | `vision/tracker` via `TrackerAdapter` | Member 1 | SCAFFOLDED |
| Re-ID | `Track[]` pairs | `ReIdCandidate[]` | `vision/reid` via `ReIdAdapter` | Member 1 | SCAFFOLDED |
| Event Extraction | `Track[]` | `Event[]` | `vision/event_extractor` | Member 1 | SCAFFOLDED |
| Camera Graph | `Camera[]` | Adjacency graph | `intelligence/camera_graph` | Member 2 | SCAFFOLDED (interface defined) |
| Mobility Graph | `CameraTransition[]` | Travel-time estimates | `intelligence/mobility_graph` | Member 2 | SCAFFOLDED (interface defined) |
| Event Graph | `Event[]` | Relationship graph | `intelligence/event_graph` | Member 2 | SCAFFOLDED (interface defined) |
| PACE | Distance, time | `PhysicalConsistency` | `intelligence/pace/travel_time.py` | Member 2 | PARTIAL (`check_travel_time` real; 5 stubs) |
| Reconstruction | Gap intervals | `Hypothesis[]` | `intelligence/reconstruction` | Member 2 | SCAFFOLDED (interface defined) |
| Investigation | `InvestigationRequest` | `InvestigationResponse` | `agent/orchestration` | Member 3 | SCAFFOLDED (interface defined) |
| Verification | `InvestigationResponse` | Verified response | `agent/verifier` | Member 3 | SCAFFOLDED (interface defined) |
| API Serving | HTTP request | JSON response | `services/api/app/main.py` | Member 3 | MOCK WORKING (10 routes) |
| Dashboard | JSON response | Interactive UI | `apps/web/src/App.tsx` | Member 4 | MOCK WORKING |

## Vision Architecture (Model-Agnostic)

Adapter protocols are defined in `vision/adapters/protocols.py`:
- **`DetectorAdapter.detect(frame_bytes, camera_id, timestamp_ms) → Observation[]`**
- **`TrackerAdapter.update(observations) → Track[]`**
- **`ReIdAdapter.embed(frame_bytes, bbox) → str`**
- **`ReIdAdapter.compare(ref_a, ref_b) → float`**

Mock implementations (`MockDetector`, `MockTracker`, `MockReId`) exist for testing.

No specific model is chosen. Candidate implementations:
| Role | Candidates | License Concern |
|---|---|---|
| Detector | YOLO, RT-DETR | YOLOv8 is AGPLv3 |
| Tracker | ByteTrack, BoT-SORT | Typically MIT |
| Re-ID | OSNet, YoutuReID | Verify before use |

## Intelligence Architecture

All interfaces defined in `intelligence/interfaces.py`:

- **CameraGraphInterface**: `add_camera()`, `add_connection()`, `neighbors()`, `is_reachable()`
- **MobilityGraphInterface**: `get_transition()`, `estimate_travel_window()`, `get_neighbors()`
- **EventGraphInterface**: `add_event()`, `add_relation()`, `get_related_events()`
- **ReconstructionEngineInterface**: `reconstruct_gap(last_cam, last_ts, next_cam, next_ts) → Hypothesis[]`
- **HypothesisRankerInterface**: `rank(hypotheses) → sorted hypotheses`
- **EvidenceCoverageCalculatorInterface**: `calculate(events, hypotheses) → EvidenceCoverage`

## PACE — Physical & Causal Evidence Engine

| Check | Function | Status |
|---|---|---|
| Travel Time | `check_travel_time(distance, available, minimum)` | **IMPLEMENTED** — tested |
| Reachability | `check_reachability(from_cam, to_cam)` | Stub → returns UNKNOWN |
| Temporal Overlap | `check_temporal_overlap(a_start, a_end, b_start, b_end)` | Stub → returns UNKNOWN |
| Direction Consistency | `check_direction_consistency()` | Stub → returns UNKNOWN |
| Contradictions | `check_contradictions()` | Stub → returns UNKNOWN |
| Composite Journey | `check_candidate_journey(similarity, distance, available, minimum)` | Delegates to `check_travel_time` |

**PACE is deterministic. No LLM may generate or override a PACE decision.**

## Agent Architecture

Interfaces defined in `agent/interfaces.py`:
- **`LLMClient`** protocol: `invoke(prompt, tools) → str`
  - `FakeLLMClient`: Returns canned response (IMPLEMENTED for testing)
  - `BedrockLLMClient`: TODO(member3)
- **`InvestigatorInterface`**: `investigate(request) → InvestigationResponse`
- **`VerifierInterface`**: `verify(response) → InvestigationResponse` — strips hallucinations, enforces PACE

Hallucination prevention: The Verifier runs every PACE check against LLM-proposed claims. Any claim that implies a physically impossible journey is downgraded from INFERRED to REJECTED.

## API Architecture

| Method | Path | Description | Status |
|---|---|---|---|
| GET | `/api/health` | System health | REAL |
| GET | `/api/cameras` | List cameras | MOCK |
| GET | `/api/events` | List events | MOCK |
| GET | `/api/events/{event_id}` | Single event | MOCK |
| GET | `/api/camera-graph` | Camera adjacency | MOCK (empty edges) |
| GET | `/api/event-graph` | Event relationships | MOCK (empty) |
| POST | `/api/investigations` | Create investigation | MOCK (returns golden demo) |
| GET | `/api/investigations/{id}` | Get investigation | MOCK |
| GET | `/api/evidence/{id}` | Get evidence item | 501 NOT_IMPLEMENTED |
| GET | `/api/hypotheses/{id}` | Get hypotheses | MOCK |

Standard error shape: `{"code": "...", "message": "...", "details": {...}}`
Codes: `NOT_FOUND`, `NOT_IMPLEMENTED`, `VALIDATION_ERROR`

## Frontend Architecture

- **Service layer** (`services/api.ts`): Typed API client with `VITE_USE_MOCKS` fallback
- **Types** (`services/types.ts`): Mirrors canonical contracts
- **Mock data** (`services/mockData.ts`): Static fallback when API unreachable
- **Dashboard** (`App.tsx`): Claims, PACE checks, coverage, unknowns, warnings
- **Loading/error/empty states**: All handled

Components consume typed `InvestigationResponse` — switching `VITE_USE_MOCKS=false` does not require rewriting UI.

## Storage Architecture
- **Local**: SCAFFOLDED (`storage/local/`)
- **DynamoDB**: PLANNED (`storage/aws/`)
- **S3**: PLANNED (`storage/aws/`)
- **OpenSearch**: Not planned

## AWS Architecture
- **CDK** (`infra/aws/cdk/`): SCAFFOLDED. No resources defined.

## Contract Architecture

All contracts live in `packages/contracts/python/argus_contracts/`:

| Contract | Producer | Consumer |
|---|---|---|
| Camera, Position | Config / Member 2 | All |
| Observation, BoundingBox, VideoSource | Member 1 | Member 1, 2 |
| Track | Member 1 | Member 1, 2 |
| ReIdCandidate, PhysicalConsistency | Member 1 + PACE | Member 2, 3 |
| Event, Participant | Member 1 | Member 2, 3, 4 |
| CameraTransition, TravelTimeStats | Member 2 | Member 2, 3 |
| Hypothesis, PaceCheck | Member 2 | Member 3, 4 |
| EvidenceCoverage | Member 2 | Member 3, 4 |
| Claim | Member 3 | Member 4 |
| InvestigationRequest, InvestigationResponse | Member 3 | Member 4 |

## Dependency Direction

```
contracts (no deps)
    ↑
vision (depends on contracts only)
    ↑
intelligence (depends on contracts only)
    ↑
agent (depends on contracts + intelligence interfaces)
    ↑
services/api (depends on contracts)
    ↑
apps/web (depends on API)
```

AWS/storage are adapters around domain logic — never embedded in core.

## Runtime Modes
- **Pure Mock**: Current. Reads JSON files. No GPU, no AWS.
- **Local Real**: Future. Runs vision + intelligence locally.
- **AWS**: Future. Lambda/ECS + DynamoDB + S3.

## Architecture Decisions
1. **LLM is not source of truth**: Hallucinations are expected. PACE enforces physical reality.
2. **PACE is deterministic**: Forensic integrity requires zero probabilistic override.
3. **Graph DB not required initially**: In-memory Python graphs suffice at demo scale.
4. **Large model files not in Git**: `.gitignore` blocks `.pt`, `.onnx`, `.safetensors`.
5. **Adapter protocols**: Vision implementations are swappable without touching other modules.

## Current Architectural Gaps
- Vision modules are empty — the pipeline produces no real observations.
- Intelligence graphs are interfaces only — no pathfinding exists.
- Agent has no real LLM interaction — `FakeLLMClient` returns a fixed string.
- API serves static JSON — no orchestration behind the routes.
- AWS has no resources defined.
