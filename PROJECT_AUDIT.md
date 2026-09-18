# ARGUS Project Audit

*For external review. This document describes the exact state of the repository.*

## Project Identity
- **Name**: ARGUS — Evidence-Aware Event Reconstruction
- **Repository**: Fresh clean-room implementation (no code from CU-DrAgon)
- **Team**: 4 parallel developers using AI coding agents
- **Platform**: Windows PowerShell first-class

## Current Goal
Deliver a frozen skeleton repository with canonical contracts, mock data, typed interfaces, and passing tests — so four developers can begin real feature implementation in parallel without blocking each other.

## What Actually Runs Today
- `.\scripts\validate.ps1` → 24 Python tests pass + frontend TypeScript build passes
- `.\scripts\run_mock_demo.ps1` → FastAPI on :8000 + React on :5173 rendering the missing-laptop investigation

## What Is Real (Contains Working Logic)
| Item | File | Evidence |
|---|---|---|
| PACE travel-time check | `intelligence/pace/travel_time.py` | Correctly rejects 140m/16s journey — 4 tests pass |
| FastAPI mock server | `services/api/app/main.py` | 10 routes serving mock JSON — 9 tests pass |
| React dashboard | `apps/web/src/App.tsx` | Renders claims, PACE checks, coverage, unknowns |
| Frontend service layer | `apps/web/src/services/api.ts` | Typed API client with mock fallback |
| Contract invariant tests | `tests/contract/test_contracts.py` | 11 tests validating mock data against schemas |
| Pydantic contracts | `packages/contracts/python/argus_contracts/` | 12 models defining the entire data schema |

## What Is Mocked
| Item | Mock Source |
|---|---|
| Investigation response | `mocks/investigations/inv_001.json` |
| Camera list | `mocks/cameras/cameras.json` |
| Events | `mocks/events/events.json` |
| Camera transitions | `mocks/transitions/transitions.json` |
| Hypotheses | `mocks/hypotheses/hypotheses.json` |
| Re-ID candidates | `mocks/hypotheses/reid_candidates.json` |
| LLM client | `agent/interfaces.py` → `FakeLLMClient` returns canned string |
| Vision adapters | `vision/adapters/protocols.py` → `MockDetector`, `MockTracker`, `MockReId` |

## What Is Only An Interface (No Logic)
| Interface | File |
|---|---|
| DetectorAdapter, TrackerAdapter, ReIdAdapter | `vision/adapters/protocols.py` |
| CameraGraphInterface | `intelligence/interfaces.py` |
| MobilityGraphInterface | `intelligence/interfaces.py` |
| EventGraphInterface | `intelligence/interfaces.py` |
| ReconstructionEngineInterface | `intelligence/interfaces.py` |
| HypothesisRankerInterface | `intelligence/interfaces.py` |
| EvidenceCoverageCalculatorInterface | `intelligence/interfaces.py` |
| InvestigatorInterface | `agent/interfaces.py` |
| VerifierInterface | `agent/interfaces.py` |
| PACE stubs (reachability, overlap, etc.) | `intelligence/pace/travel_time.py` |

## What Is Empty (Directory Only)
- `vision/detector/`, `vision/tracker/`, `vision/reid/`, `vision/event_extractor/`, `vision/ingestion/`
- `intelligence/camera_graph/`, `intelligence/mobility_graph/`, `intelligence/event_graph/`, `intelligence/reconstruction/`, `intelligence/hypotheses/`, `intelligence/evidence/`
- `agent/orchestration/`, `agent/tools/`, `agent/verifier/`, `agent/clients/`, `agent/prompts/`
- `storage/`, `infra/aws/`

## Member Work Summary

### Member 1 (Vision)
- **Has**: Adapter protocols (`DetectorAdapter`, `TrackerAdapter`, `ReIdAdapter`) + mock implementations
- **Must build first**: M1-005 — Video Ingestion, then M1-001 — Real `DetectorAdapter`
- **Key output**: `Observation[]`, `Track[]`, `ReIdCandidate[]`, `Event[]` from M1-006 (End-to-End Runner)

### Member 2 (Intelligence)
- **Has**: PACE `check_travel_time` (real, tested), typed interfaces for all graphs, 5 PACE stubs
- **Must build first**: M2-001 — In-memory CameraGraph
- **Key output**: `EventGraph`, `Hypothesis[]`, `PaceCheck[]`, `EvidenceCoverage`

### Member 3 (Agent/Backend)
- **Has**: FastAPI mock server (10 routes, 9 tests), LLM/Investigator/Verifier interfaces, FakeLLMClient
- **Must build first**: M3-002 — Agent tool functions (using mocks)
- **Key output**: Real `InvestigationResponse` from orchestration loop, AWS deployment (M3-007)

### Member 4 (Frontend)
- **Has**: React dashboard with service layer, typed data, epistemic styling, mock fallback
- **Must build first**: M4-001 — VideoPlayer or M4-004 — EventTimeline
- **Key output**: Complete interactive investigation UI, InvestigationQuery (M4-011), Trajectory View (M4-012), Real API wiring (M4-013)

## Current Tests (All Passing)

| Suite | File | Count | Result |
|---|---|---|---|
| Contract invariants | `tests/contract/test_contracts.py` | 11 | PASSED |
| PACE engine | `intelligence/tests/test_pace.py` | 4 | PASSED |
| API routes | `services/api/tests/test_api.py` | 9 | PASSED |
| Frontend build | `apps/web/` `tsc -b && vite build` | — | PASSED |
| **Total** | | **24 + build** | **ALL PASSING** |

## Current Demo Capability
The missing-laptop investigation renders with OBSERVED/INFERRED/REJECTED epistemic badges, evidence coverage percentages, unknown gap intervals, and PACE rejection details. Zero external dependencies required.

## Current AWS Capability
None. Empty scaffolding only.

## What Prevents a Real Demo
1. No video ingestion or model inference code
2. No graph algorithms (Camera, Mobility, Event graphs are interfaces only)
3. No LLM interaction (FakeLLMClient returns a fixed string)
4. API serves static JSON instead of invoking real orchestration

## Files That Must Never Be Modified Independently
- `packages/contracts/python/argus_contracts/*.py` — Team approval required
- `packages/contracts/typescript/index.ts` — Must match Python
- `mocks/investigations/inv_001.json` — Golden demo fixture

## Major Risks
1. **Hallucination**: LLM will invent observations. Verifier must be rock-solid.
2. **Vision noise**: Real tracks will be noisy; Event extraction needs robust heuristics.
3. **YOLO license**: YOLOv8 is AGPLv3 — may impose distribution requirements.

## Known Technical Debt
- TypeScript contracts are manually synchronized (no codegen pipeline)
- API returns raw dicts, not typed Pydantic response models for serialization

## Decisions That Must NOT Change Without Team Discussion
1. OBSERVED / INFERRED / UNKNOWN / REJECTED semantics
2. PACE is deterministic
3. Adapter-based vision (model-agnostic)
4. Contracts are the single source of truth
5. Mock mode must remain operational

## Unresolved Questions
- ECS (Fargate) vs Lambda for production API?
- Which Re-ID model (OSNet vs YoutuReID) and its license?
- Will the team need a graph database at scale, or will in-memory suffice?

## Files an External Reviewer Should Inspect
1. `packages/contracts/python/argus_contracts/` — Data model
2. `intelligence/pace/travel_time.py` — PACE logic
3. `vision/adapters/protocols.py` — Adapter interfaces
4. `intelligence/interfaces.py` — Graph interfaces
5. `agent/interfaces.py` — Agent interfaces
6. `services/api/app/main.py` — API surface
7. `apps/web/src/App.tsx` — Current UI
8. `apps/web/src/services/api.ts` — Frontend service layer
9. `mocks/investigations/inv_001.json` — Expected output shape
10. `tests/contract/test_contracts.py` — Invariant checks
