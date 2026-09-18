# ARGUS Current Status

Last audited: 2026-09-19 02:45+05:30
Validation: **24/24 pytest PASSED, frontend build PASSED**

## Overall Status

| Area | Status | Verified | Tests | Notes |
|---|---|---|---|---|
| Contracts (Python) | IMPLEMENTED | YES | 11 contract tests | Pydantic v2 models |
| Contracts (TypeScript) | IMPLEMENTED | YES | tsc build passes | Matches Python |
| Contracts (JSON Schema) | IMPLEMENTED | YES | Auto-generated | `scripts/generate_schemas.py` |
| Frontend | MOCK WORKING | YES | tsc build passes | Service layer + typed components |
| FastAPI | MOCK WORKING | YES | 9 API tests | 10 routes, typed errors |
| Detector Adapter | SCAFFOLDED | NO | — | Protocol + MockDetector defined |
| Tracker Adapter | SCAFFOLDED | NO | — | Protocol + MockTracker defined |
| Re-ID Adapter | SCAFFOLDED | NO | — | Protocol + MockReId defined |
| Event Extractor | SCAFFOLDED | NO | — | Empty directory |
| Camera Graph | SCAFFOLDED | NO | — | Interface defined |
| Mobility Graph | SCAFFOLDED | NO | — | Interface defined |
| Event Graph | SCAFFOLDED | NO | — | Interface defined |
| PACE | PARTIAL | YES | 4 PACE tests | `check_travel_time` real; 5 stubs return UNKNOWN |
| Reconstruction | SCAFFOLDED | NO | — | Interface defined |
| Hypotheses Ranker | SCAFFOLDED | NO | — | Interface defined |
| Evidence Coverage | SCAFFOLDED | NO | — | Interface defined |
| Investigator | SCAFFOLDED | NO | — | Interface defined |
| Verifier | SCAFFOLDED | NO | — | Interface defined |
| LLM Client | SCAFFOLDED | NO | — | FakeLLMClient returns canned string |
| AWS / CDK | SCAFFOLDED | NO | — | Empty directory |
| CI | IMPLEMENTED | NO | — | GitHub Actions workflow defined |

## Member 1 — Vision Pipeline

### Owned Files/Folders
- `vision/adapters/protocols.py` — Adapter interfaces (IMPLEMENTED)
- `vision/detector/` — Empty
- `vision/tracker/` — Empty
- `vision/reid/` — Empty
- `vision/event_extractor/` — Empty
- `vision/ingestion/` — Empty
- `vision/tests/` — Empty

### TODO

| ID | Description | File | Dependency | Acceptance | Difficulty |
|---|---|---|---|---|---|
| M1-001 | Implement a real DetectorAdapter (YOLO or RT-DETR) | `vision/detector/` | Video frames | Outputs `Observation[]` matching contract | HIGH |
| M1-002 | Implement a real TrackerAdapter (ByteTrack or BoT-SORT) | `vision/tracker/` | M1-001 | Outputs `Track[]` matching contract | HIGH |
| M1-003 | Implement a real ReIdAdapter (OSNet or YoutuReID) | `vision/reid/` | M1-002 | `compare()` returns calibrated similarity | HIGH |
| M1-004 | Event extraction from tracks | `vision/event_extractor/` | M1-002 | Outputs `Event[]` (e.g. PERSON_APPROACHED_OBJECT) | MEDIUM |
| M1-005 | Video ingestion pipeline | `vision/ingestion/` | None | Reads MP4/demo files, yields frames | MEDIUM |

### Expected Handoff
`Observation[]`, `Track[]`, `ReIdCandidate[]`, `Event[]` — conforming to canonical contracts.

---

## Member 2 — Spatio-Temporal Intelligence

### Owned Files/Folders
- `intelligence/interfaces.py` — All graph/engine interfaces (IMPLEMENTED)
- `intelligence/pace/travel_time.py` — PACE engine (PARTIAL)
- `intelligence/tests/test_pace.py` — 4 tests (PASSING)
- `intelligence/camera_graph/` — Empty
- `intelligence/mobility_graph/` — Empty
- `intelligence/event_graph/` — Empty
- `intelligence/reconstruction/` — Empty
- `intelligence/hypotheses/` — Empty
- `intelligence/evidence/` — Empty

### TODO

| ID | Description | File | Dependency | Acceptance | Difficulty |
|---|---|---|---|---|---|
| M2-001 | Implement CameraGraph (in-memory) | `intelligence/camera_graph/` | None (use mock cameras) | `neighbors()`, `is_reachable()` work | LOW |
| M2-002 | Implement MobilityGraph | `intelligence/mobility_graph/` | M2-001 | `get_transition()`, `estimate_travel_window()` work | MEDIUM |
| M2-003 | Implement EventGraph | `intelligence/event_graph/` | M1 events (use mocks) | `add_event()`, `get_related_events()` work | MEDIUM |
| M2-004 | Expand PACE checks | `intelligence/pace/travel_time.py` | M2-001, M2-002 | `check_reachability()`, `check_temporal_overlap()` return real results | MEDIUM |
| M2-005 | Blind-spot reconstruction | `intelligence/reconstruction/` | M2-003 | `reconstruct_gap()` returns plausible routes | HIGH |
| M2-006 | Hypothesis ranking | `intelligence/hypotheses/` | M2-005 | `rank()` sorts by composite score | HIGH |
| M2-007 | Evidence coverage calculation | `intelligence/evidence/` | M2-006 | `calculate()` returns valid fractions summing to ~1.0 | LOW |

### Expected Handoff
`EventGraph`, `Hypothesis[]`, `PaceCheck[]`, `EvidenceCoverage`

---

## Member 3 — Agent & Backend

### Owned Files/Folders
- `agent/interfaces.py` — LLMClient, Investigator, Verifier (IMPLEMENTED)
- `services/api/app/main.py` — FastAPI mock server (MOCK WORKING)
- `services/api/tests/test_api.py` — 9 tests (PASSING)
- `agent/orchestration/` — Empty
- `agent/tools/` — Empty
- `agent/verifier/` — Empty
- `agent/clients/` — Empty
- `storage/` — Empty
- `infra/aws/` — Empty

### TODO

| ID | Description | File | Dependency | Acceptance | Difficulty |
|---|---|---|---|---|---|
| M3-002 | Agent tool functions (using mocks) | `agent/tools/` | M2 interfaces | `search_events()`, `check_physical_consistency()` etc. callable by LLM | MEDIUM |
| M3-003 | Investigator loop (with FakeLLMClient) | `agent/orchestration/` | M3-002 | Implements `InvestigatorInterface`, produces `InvestigationResponse` | HIGH |
| M3-004 | Verifier (PACE enforcement on LLM) | `agent/verifier/` | M3-003, PACE | Strips hallucinated claims, enforces PACE | HIGH |
| M3-001 | BedrockLLMClient | `agent/clients/bedrock.py` | AWS credentials | Implements `LLMClient` protocol, calls Bedrock | MEDIUM |
| M3-005 | Replace mock API routes with real logic | `services/api/app/main.py` | M3-003 | Routes invoke Investigator instead of loading JSON | MEDIUM |
| M3-006 | Storage layer (DynamoDB/S3) | `storage/aws/` | None | Implements repository interfaces | MEDIUM |

### Expected Handoff
`InvestigationResponse` served via `/api/investigations/{id}`

---

## Member 4 — Frontend & Investigation UI

### Owned Files/Folders
- `apps/web/src/App.tsx` — Dashboard (MOCK WORKING)
- `apps/web/src/services/api.ts` — API client (IMPLEMENTED)
- `apps/web/src/services/types.ts` — Types (IMPLEMENTED)
- `apps/web/src/services/mockData.ts` — Fallback data (IMPLEMENTED)
- `apps/web/src/index.css` — Epistemic styling (IMPLEMENTED)
- `apps/web/src/components/` — Empty
- `apps/web/src/features/` — Empty subdirectories

### TODO

| ID | Description | File | Dependency | Acceptance | Difficulty |
|---|---|---|---|---|---|
| M4-001 | VideoPlayer component | `apps/web/src/components/VideoPlayer.tsx` | None | Plays demo video with timestamp overlay | MEDIUM |
| M4-002 | CameraGraphView | `apps/web/src/features/cameras/CameraGraphView.tsx` | None (use mock) | Renders camera topology as interactive graph | HIGH |
| M4-003 | EvidenceCard component | `apps/web/src/features/evidence/EvidenceCard.tsx` | None | Displays single evidence item with provenance | LOW |
| M4-004 | EventTimeline component | `apps/web/src/features/timeline/EventTimeline.tsx` | None | Renders events on time axis with epistemic colors | MEDIUM |
| M4-005 | EvidenceCoverageView | `apps/web/src/features/evidence/EvidenceCoverageView.tsx` | None | Bar/ring chart of observed/inferred/unknown fractions | LOW |
| M4-006 | UnknownGap component | `apps/web/src/components/UnknownGap.tsx` | None | Visualizes blind-spot intervals | LOW |
| M4-007 | HypothesisComparison | `apps/web/src/features/hypotheses/HypothesisComparison.tsx` | None | Side-by-side hypothesis scores + PACE checks | MEDIUM |
| M4-008 | PaceCheckCard | `apps/web/src/components/PaceCheckCard.tsx` | None | Renders PASS/FAIL/UNKNOWN check with details | LOW |
| M4-009 | InvestigationReplay | `apps/web/src/features/investigation/InvestigationReplay.tsx` | None | Step-through of investigation stages | HIGH |
| M4-010 | EventGraphView | `apps/web/src/features/event-graph/EventGraphView.tsx` | None | Renders event relationship graph | HIGH |

**Important**: Member 4 only **renders** intelligence outputs. Member 2 **computes** them.

### Expected Handoff
Complete interactive UI consuming `InvestigationResponse`.

---

## Integration Status

| Connection | Status |
|---|---|
| Vision → Intelligence | REAL NOT CONNECTED (using `mocks/`) |
| Intelligence → Agent | REAL NOT CONNECTED |
| Agent → API | MOCK CONNECTED (API serves static JSON) |
| API → Frontend | MOCK CONNECTED (service layer with fallback) |

## Tests

| Path | Count | Status |
|---|---|---|
| `tests/contract/test_contracts.py` | 11 | PASSED |
| `intelligence/tests/test_pace.py` | 4 | PASSED |
| `services/api/tests/test_api.py` | 9 | PASSED |
| Frontend `tsc -b && vite build` | — | PASSED |
| **Total** | **24 + build** | **ALL PASSING** |

## Current Demo Capability
Run `.\scripts\run_mock_demo.ps1`. Dashboard renders the missing-laptop investigation with OBSERVED/INFERRED claims, REJECTED PACE hypothesis, evidence coverage percentages, unknown gaps, and warnings. No GPU or AWS required.

## What Cannot Be Demonstrated Yet
- Actual video file ingestion or model inference
- Dynamic investigation queries answered by LLM
- Graph pathfinding or blind-spot interpolation
- Any AWS integration

## Critical Path to Full Demo
1. M2-001: Camera graph from mock config
2. M1-001: Detector producing real observations
3. M3-003: Investigation orchestration loop
4. M3-005: API routes invoking real orchestrator
5. M4-002+: Frontend graph visualizations
