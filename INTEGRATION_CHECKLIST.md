# Integration Checklist

Integration follows a strict phase sequence. Development happens in parallel using mocks, but merging to `main` must follow this order.

## PHASE 0 — Contracts Frozen ✅ COMPLETED

- [x] Camera, Position
- [x] Observation, BoundingBox, VideoSource
- [x] Track
- [x] Event, Participant
- [x] ReIdCandidate, PhysicalConsistency, PaceCheckStatus
- [x] CameraTransition, TravelTimeStats
- [x] PaceCheck
- [x] Hypothesis
- [x] EvidenceCoverage
- [x] Claim
- [x] InvestigationRequest, InvestigationResponse
- [x] JSON Schemas generated
- [x] TypeScript interfaces synchronized

## PHASE 1 — Mock End-to-End ✅ COMPLETED

- [x] Mock cameras seeded (4 cameras)
- [x] Mock events seeded (3 events)
- [x] Mock transitions seeded (3 transitions)
- [x] Mock Re-ID candidates seeded (1 plausible + 1 impossible)
- [x] Mock hypotheses seeded (1 INFERRED + 1 REJECTED)
- [x] Mock investigation response seeded (`inv_001`)
- [x] PACE rejects impossible journey (140m in 16s) — **TESTED**
- [x] Frontend renders claims with epistemic badges — **TESTED**
- [x] Contract invariant tests pass (11 tests) — **TESTED**
- [x] API tests pass (9 tests) — **TESTED**

## PHASE 2 — Vision Integration

| Check | Owner | Dependency | Test | Expected Output |
|---|---|---|---|---|
| [ ] Detector outputs `Observation[]` from video | Member 1 | Video file | Parse against contract | Valid Observations |
| [ ] Tracker outputs `Track[]` from observations | Member 1 | Detector | Parse against contract | Valid Tracks |
| [ ] Re-ID outputs `ReIdCandidate[]` | Member 1 | Tracker | Similarity in [0,1] | Valid candidates |
| [ ] Event extractor outputs `Event[]` | Member 1 | Tracker | Parse against contract | Events with supporting observations |
| [ ] End-to-end Vision runner processes multiple demo MP4s | Member 1 | Extractor | E2E execution with 2+ cameras | `Observation[]`, `Track[]`, `ReIdCandidate[]`, `Event[]` |

## PHASE 3 — Intelligence Integration

| Check | Owner | Dependency | Test | Expected Output |
|---|---|---|---|---|
| [ ] CameraGraph loads topology | Member 2 | Mock cameras | `neighbors()` returns adjacency | Graph structure |
| [ ] MobilityGraph computes transitions | Member 2 | CameraGraph | `estimate_travel_window()` | Travel-time estimates |
| [ ] EventGraph ingests real events | Member 2 | Phase 2 events | `get_related_events()` | Connected events |
| [ ] PACE reachability | Member 2 | CameraGraph | Unreachable → FAIL/UNKNOWN | PhysicalConsistency |
| [ ] PACE temporal overlap | Member 2 | Tracker data | Simultaneous distant → FAIL | PhysicalConsistency |
| [ ] PACE direction consistency | Member 2 | CameraGraph | Invalid vectors → FAIL/UNKNOWN| PhysicalConsistency |
| [ ] PACE contradiction check | Member 2 | EventGraph | Mutually exclusive → FAIL | PhysicalConsistency |
| [ ] PACE candidate journey composite | Member 2 | All PACE | Impossible candidates → FAIL | PhysicalConsistency |
| [ ] Reconstruction bridges blind spots | Member 2 | EventGraph | `reconstruct_gap()` | Candidate hypotheses |
| [ ] HypothesisRanker orders candidates | Member 2 | Reconstruction | Highest-evidence first | Sorted hypotheses |

## PHASE 4 — Agent Integration

| Check | Owner | Dependency | Test | Expected Output |
|---|---|---|---|---|
| [ ] Agent tools | Member 3 | Phase 3 interfaces | Structured tool returns | Valid evidence JSON |
| [ ] FakeLLM local investigator | Member 3 | Tools | Complete orchestration loop | InvestigationResponse |
| [ ] Verifier | Member 3 | PACE | Strips hallucinated claims | Verified claims |
| [ ] Bedrock swap | Member 3 | FakeLLM loop | Call AWS Bedrock | Real LLM response |
| [ ] Real API orchestration | Member 3 | Investigator | HTTP POST invokes loop | JSON response to client |
| [ ] Evidence playback endpoint | Member 3 | Storage Layer | GET /api/evidence/{id} | Typed playback metadata with URL |

## PHASE 5 — Frontend Real API Integration

| Check | Owner | Dependency | Test | Expected Output |
|---|---|---|---|---|
| [ ] InvestigationQuery works | Member 4 | Phase 4 API | User input → API → UI | Investigation rendering |
| [ ] Multi-camera trajectory view works | Member 4 | Phase 4 Data | Visual route rendering | Clear evidence paths |
| [ ] `VITE_USE_MOCKS=false` works | Member 4 | Phase 4 | UI renders real response | No mock fallback |
| [ ] All visualization components render | Member 4 | Phase 4 | Visual inspection | Complete dashboard |

## PHASE 6 — AWS Integration

| Check | Owner | Dependency | Test | Expected Output |
|---|---|---|---|---|
| [ ] CDK stack synthesizes | Member 3 | None | `cdk synth` | Valid CloudFormation |
| [ ] Deployed API health = 200 | Member 3 | CDK | Health check endpoint | HTTP 200 OK |
| [ ] S3 works | Member 3 | Storage Layer | Upload/Download test | Persistent media |
| [ ] DynamoDB works | Member 3 | Storage Layer | CRUD test | Persistent events |
| [ ] Environment config works | Member 3 | Deployment | Lambda reads config | Correct behavior |
| [ ] Local mode remains functional | Member 3 | None | Local tests pass | Isolation maintained |

## PHASE 7 — Golden Demo Validation

### Missing-Laptop Investigation (End-to-End)

**Expected observations:**
- Person approaches Desk 4 (CAM_01)
- Laptop vanishes (CAM_01)
- Similar person appears in corridor (CAM_02)

**Expected impossible candidate:**
- Appearance similarity: 91%
- Distance: 140 metres
- Available time: 16 seconds
- Minimum required: 100 seconds
- **Expected: PACE → REJECTED**

**Expected investigation output:**
- 2 OBSERVED claims, 1 INFERRED claim
- 1 plausible hypothesis (CAM_01 → CAM_02), 1 REJECTED hypothesis (CAM_01 → CAM_04)
- Coverage: ~68% observed, ~16% inferred, ~16% unknown
- Warning: "Human review required"

### Final End-to-End Definition of Done
- [ ] Real video processed end-to-end without JSON mock files (Member 1)
- [ ] PACE correctly rejects the impossible journey (Member 2)
- [ ] Investigator retrieves relevant evidence, Verifier grounds it, produces InvestigationResponse (Member 3)
- [ ] Frontend displays OBSERVED / INFERRED / REJECTED correctly (Member 4)
- [ ] Dashboard shows evidence coverage and unknown gaps (Member 4)
- [ ] No hallucinated evidence passes the Verifier (Member 3)
