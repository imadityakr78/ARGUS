# ARGUS File Map

| Path | Purpose | Owner | Status | Input | Output | Depends On | Safe To Modify? |
|---|---|---|---|---|---|---|---|
| **Root Config** |
| `.env.example` | Environment variable template | Team | IMPLEMENTED | — | — | — | Team |
| `pytest.ini` | Test configuration | Team | IMPLEMENTED | — | — | — | Team |
| `.github/workflows/ci.yml` | CI pipeline | Team | IMPLEMENTED | — | — | — | Team |
| `.github/CODEOWNERS` | PR review routing | Team | IMPLEMENTED | — | — | — | Team |
| `.github/pull_request_template.md` | PR checklist | Team | IMPLEMENTED | — | — | — | Team |
| **Contracts** |
| `packages/contracts/python/argus_contracts/*.py` | Pydantic source of truth | Team | IMPLEMENTED | — | All typed data | — | **TEAM ONLY** |
| `packages/contracts/typescript/index.ts` | TypeScript types | Team | IMPLEMENTED | — | Frontend types | Python contracts | **TEAM ONLY** |
| `packages/contracts/schemas/*.json` | JSON Schemas | Team | IMPLEMENTED | — | Validation schemas | Python contracts | Auto-generated |
| **Vision** |
| `vision/adapters/protocols.py` | DetectorAdapter, TrackerAdapter, ReIdAdapter | Member 1 | IMPLEMENTED (interfaces) | — | Protocol definitions | Contracts | Member 1 |
| `vision/detector/` | Model-specific detector | Member 1 | SCAFFOLDED | Frames | Observations | protocols.py | Member 1 |
| `vision/tracker/` | Model-specific tracker | Member 1 | SCAFFOLDED | Observations | Tracks | protocols.py | Member 1 |
| `vision/reid/` | Model-specific Re-ID | Member 1 | SCAFFOLDED | Tracks | ReIdCandidates | protocols.py | Member 1 |
| `vision/event_extractor/` | Track-to-Event conversion | Member 1 | SCAFFOLDED | Tracks | Events | Contracts | Member 1 |
| **Intelligence** |
| `intelligence/interfaces.py` | All graph/engine interfaces | Member 2 | IMPLEMENTED (interfaces) | — | Protocol definitions | Contracts | Member 2 |
| `intelligence/pace/travel_time.py` | PACE engine + stubs | Member 2 | PARTIAL | Distance, time | PhysicalConsistency | Contracts | Member 2 |
| `intelligence/tests/test_pace.py` | PACE unit tests | Member 2 | IMPLEMENTED | — | — | travel_time.py | Member 2 |
| `intelligence/camera_graph/` | Camera topology | Member 2 | SCAFFOLDED | Cameras | Graph | interfaces.py | Member 2 |
| `intelligence/mobility_graph/` | Travel-time estimation | Member 2 | SCAFFOLDED | Transitions | Graph | interfaces.py | Member 2 |
| `intelligence/event_graph/` | Event relationships | Member 2 | SCAFFOLDED | Events | Graph | interfaces.py | Member 2 |
| `intelligence/reconstruction/` | Blind-spot routing | Member 2 | SCAFFOLDED | Gap | Hypotheses | interfaces.py | Member 2 |
| **Agent** |
| `agent/interfaces.py` | LLMClient, Investigator, Verifier | Member 3 | IMPLEMENTED (interfaces) | — | Protocol definitions | Contracts | Member 3 |
| `agent/orchestration/` | Investigation loop | Member 3 | SCAFFOLDED | Request | Response | interfaces.py | Member 3 |
| `agent/tools/` | LLM-callable tools | Member 3 | SCAFFOLDED | — | — | Intelligence | Member 3 |
| `agent/verifier/` | PACE enforcement on LLM | Member 3 | SCAFFOLDED | Response | Verified response | PACE | Member 3 |
| `agent/clients/` | Bedrock client | Member 3 | SCAFFOLDED | — | — | AWS | Member 3 |
| **API** |
| `services/api/app/main.py` | FastAPI server (10 routes) | Member 3 | MOCK WORKING | HTTP | JSON | Mocks | Member 3 |
| `services/api/tests/test_api.py` | API tests (9 tests) | Member 3 | IMPLEMENTED | — | — | main.py | Member 3 |
| **Frontend** |
| `apps/web/src/App.tsx` | Dashboard component | Member 4 | MOCK WORKING | API data | UI | services/api.ts | Member 4 |
| `apps/web/src/services/api.ts` | API client + mock fallback | Member 4 | IMPLEMENTED | — | Typed data | types.ts | Member 4 |
| `apps/web/src/services/types.ts` | Frontend type definitions | Member 4 | IMPLEMENTED | — | Types | Contracts | Member 4 |
| `apps/web/src/services/mockData.ts` | Static fallback data | Member 4 | IMPLEMENTED | — | Mock data | types.ts | Member 4 |
| `apps/web/src/index.css` | Epistemic color system | Member 4 | IMPLEMENTED | — | Styles | — | Member 4 |
| **Mock Data** |
| `mocks/cameras/cameras.json` | 4 cameras | Team | IMPLEMENTED | — | — | Contracts | **TEAM ONLY** |
| `mocks/events/events.json` | 3 events | Team | IMPLEMENTED | — | — | Contracts | **TEAM ONLY** |
| `mocks/transitions/transitions.json` | 3 transitions | Team | IMPLEMENTED | — | — | Contracts | **TEAM ONLY** |
| `mocks/hypotheses/hypotheses.json` | 2 hypotheses | Team | IMPLEMENTED | — | — | Contracts | **TEAM ONLY** |
| `mocks/hypotheses/reid_candidates.json` | 2 Re-ID candidates | Team | IMPLEMENTED | — | — | Contracts | **TEAM ONLY** |
| `mocks/investigations/inv_001.json` | Golden demo response | Team | IMPLEMENTED | — | — | Contracts | **TEAM ONLY** |
| **Tests** |
| `tests/contract/test_contracts.py` | Contract invariant tests (11) | Team | IMPLEMENTED | Mocks | — | Contracts | Team |
| **Scripts** |
| `scripts/setup.ps1` | Environment setup | Team | IMPLEMENTED | — | — | — | Team |
| `scripts/validate.ps1` | 5-stage validation | Team | IMPLEMENTED | — | — | — | Team |
| `scripts/run_mock_demo.ps1` | Launch demo | Team | IMPLEMENTED | — | — | — | Team |
| `scripts/doctor.ps1` | Environment health check | Team | IMPLEMENTED | — | — | — | Team |
| `scripts/seed_demo.py` | Generate mock JSON | Team | IMPLEMENTED | — | mocks/*.json | Contracts | Team |
| `scripts/generate_schemas.py` | Generate JSON Schemas | Team | IMPLEMENTED | — | schemas/*.json | Contracts | Team |
