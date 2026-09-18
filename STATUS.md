# ARGUS Current Status

Last audited: 2026-09-19 03:08+05:30
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
| Vision Pipeline | PLANNED | NO | — | End-to-end runner missing |
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

==================================================
# CROSS-MEMBER OWNERSHIP BOUNDARIES
==================================================

Explicitly state:

**MEMBER 1:**
Answers: "What did the cameras detect?"
Produces: `Observation`, `Track`, visual `ReIdCandidate`, `Event`

**MEMBER 2:**
Answers: "What does the physical/spatio-temporal evidence support?"
Produces: `CameraGraph`, `MobilityGraph`, `EventGraph`, PACE results, `Hypothesis[]`, `EvidenceCoverage`

**MEMBER 3:**
Answers: "How do we investigate and explain the evidence safely?"
Produces: `InvestigationResponse`, verified claims, API, storage, AWS deployment

**MEMBER 4:**
Answers: "How does the user understand and interact with the investigation?"
Produces: UI, visualizations, question workflow, real API frontend integration

==================================================
# RE-ID / PACE OWNERSHIP MUST BE CRYSTAL CLEAR
==================================================

Member 1 owns appearance similarity.
Example:
`sourceTrackId`
`candidateTrackId`
`appearanceSimilarity = 0.91`

Member 2 owns physical validation.
Example:
`distance`
`availableTravelSeconds`
`minimumTravelSeconds`
`reachability`
`PASS / FAIL / UNKNOWN`

**Member 1 must NOT mark a candidate physically valid.**
**Member 2 must NOT run the neural appearance model.**

==================================================
# MOCK HANDOFF MATRIX
==================================================

**Member 1 → Member 2:**
`Observation[]`
`Track[]`
`ReIdCandidate[]`
`Event[]`
*Until real Vision is available: Member 2 uses mocks.*

**Member 2 → Member 3:**
`EventGraph`
`CameraTransition[]`
`PaceCheck[]`
`Hypothesis[]`
`EvidenceCoverage`
*Until real Intelligence is available: Member 3 uses mocks.*

**Member 3 → Member 4:**
`InvestigationResponse`
*Until real Agent is available: Member 4 uses mock API.*

==================================================
# FINAL GOLDEN DEMO RESPONSIBILITIES
==================================================

Scenario: Missing laptop.

**Member 1:**
Processes actual video and produces detections/tracks/events/Re-ID visual candidates.

**Member 2:**
Receives visual candidate with:
appearance similarity 0.91
then sees:
distance = 140 m
available time = 16 sec
minimum required = 100 sec
PACE returns FAIL.
The impossible candidate becomes REJECTED.

**Member 3:**
Investigator retrieves relevant evidence.
Verifier refuses to describe rejected candidate as true.
Produces grounded `InvestigationResponse`.

**Member 4:**
Shows:
OBSERVED evidence
INFERRED plausible route
UNKNOWN blind spot
REJECTED impossible route
Evidence coverage
Supporting evidence
Video/timeline
Investigation question/answer

==================================================
# TASK COMPLETION DEFINITION
==================================================

Every member task should require:
- code implemented
- unit tests
- existing tests still passing
- canonical contracts respected
- mock mode preserved
- no secrets
- no heavy assets in Git
- member-owned folder only unless approved
- documentation updated where appropriate
- handoff documented

==================================================
# MEMBER 1 — FINAL VISION TODOs
==================================================

**AGENT STOP RULE:** The AI agent must NOT automatically continue into another member's responsibilities. When all assigned TODOs are complete: run `.\scripts\validate.ps1`. If validation fails: fix only failures caused by that member's changes. If failure belongs to another member: report it as an integration blocker instead of modifying their code.

Member 1 owns: `vision/`
Member 1 MUST NOT implement: PACE, CameraGraph, MobilityGraph, EventGraph, hypothesis ranking, Bedrock, frontend, AWS.

### M1-005 — Video Ingestion
**Owner:** Member 1
**Primary folder/files:** `vision/ingestion/`
**Purpose:** Read local demo video and produce timestamped frames.
**Inputs:** Video file path, camera metadata.
**Outputs:** Timestamped frames (bytes/arrays).
**Dependencies:** None.
**Detailed implementation requirements:**
- MP4 support for demo
- configurable frame sampling
- preserve deterministic timestamp mapping
- cameraId supplied externally/config
- handle unreadable video
- release file resources properly
- no RTSP production complexity required yet
**Edge cases:** Empty/corrupt file, non-monotonic timestamps.
**Required tests:** valid small video, invalid path, empty/corrupt file, timestamp monotonicity, frame count/sample behavior.
**Acceptance criteria:** A demo MP4 can be iterated as timestamped frames.
**What NOT to implement:** Real-time RTSP streams, object detection.
**Handoff produced for next member:** Frame iterator for Detector.
**Difficulty:** MEDIUM
**State:** SCAFFOLDED

### M1-001 — Real Detector Adapter
**Owner:** Member 1
**Primary folder/files:** `vision/detector/`
**Purpose:** Convert decoded frames into canonical `Observation[]`.
**Inputs:** Decoded frames, cameraId, timestampMs.
**Outputs:** Canonical `Observation[]`.
**Dependencies:** M1-005.
**Detailed implementation requirements:**
- implement the existing `DetectorAdapter` protocol
- model remains swappable
- support at least one selected real detector
- preserve possibility of YOLO / RT-DETR replacement
- configurable confidence threshold
- normalized bounding boxes if canonical contract expects normalized values
- correct camera ID
- correct timestamp
- local track ID must NOT be invented by detector if tracker owns tracking
- confidence in valid range
- outputs validate against Observation contract
**Edge cases:** Empty frame, invalid input format.
**Required tests:** empty frame / invalid input handling, zero detections, one detection, multiple detections, confidence boundaries, canonical schema validation.
**Acceptance criteria:** A decoded frame can produce valid `Observation[]` objects.
**What NOT to implement:** Tracking across frames, model training.
**Handoff produced for next member:** `Observation[]` for Tracker.
**Difficulty:** HIGH
**State:** SCAFFOLDED

### M1-002 — Real Tracker Adapter
**Owner:** Member 1
**Primary folder/files:** `vision/tracker/`
**Purpose:** Associate observations across sequential frames.
**Inputs:** `Observation[]` per frame.
**Outputs:** Updated active `Track[]`.
**Dependencies:** M1-001.
**Detailed implementation requirements:**
- implement `TrackerAdapter` protocol
- use selected tracker such as ByteTrack or BoT-SORT through adapter
- stable localTrackId
- track start/end timestamps
- observation IDs associated with track
- avoid exposing tracker-specific classes outside adapter
- handle temporary missed detections gracefully where supported
**Edge cases:** Track lost and found, multiple overlapping subjects.
**Required tests:** one subject across frames, two subjects, missed frame, track termination, contract validation.
**Acceptance criteria:** `Observation[]` sequence produces canonical `Track[]`.
**What NOT to implement:** Re-ID across cameras, intelligence graph.
**Handoff produced for next member:** `Track[]` for Re-ID/Event Extractor.
**Difficulty:** HIGH
**State:** SCAFFOLDED

### M1-003 — Real Re-ID Adapter
**Owner:** Member 1
**Primary folder/files:** `vision/reid/`
**Purpose:** Compare appearance of tracks across cameras.
**Inputs:** `Track` pairs, crops.
**Outputs:** Visual `ReIdCandidate` data.
**Dependencies:** M1-002.
**Detailed implementation requirements:**
- implement existing `ReIdAdapter`
- model remains replaceable
- embedding storage/reference separated from canonical JSON fixtures
- similarity returned within documented range
- do NOT claim calibrated probability
- do NOT perform PACE logic here
- do NOT reject a match because of travel time
**Edge cases:** Low quality crops, missing embeddings.
**Required tests:** same/similar subject fixture, dissimilar subject fixture, similarity range, missing crop, contract validation.
**Acceptance criteria:** Track pairs produce canonical `ReIdCandidate`-compatible visual evidence.
**What NOT to implement:** Physical feasibility, PACE checks, travel time math.
**Handoff produced for next member:** Visual similarity scores for Intelligence.
**Difficulty:** HIGH
**State:** SCAFFOLDED

### M1-004 — Event Extraction
**Owner:** Member 1
**Primary folder/files:** `vision/event_extractor/`
**Purpose:** Convert tracks/observations into semantic camera events.
**Inputs:** `Track[]`, `Observation[]`.
**Outputs:** Canonical `Event[]`.
**Dependencies:** M1-002.
**Detailed implementation requirements:**
- deterministic rules where possible
- every OBSERVED event must reference supporting observation IDs
- no high-level guilt or criminal interpretation
- event timestamps derived from observation evidence
- event confidence traceable to underlying observations
- extract events like PERSON_PRESENT, PERSON_ENTER, PERSON_EXIT, PERSON_APPROACHED_OBJECT, OBJECT_PRESENT, OBJECT_ABSENT
**Edge cases:** Track fragmentation causing duplicate enter/exit.
**Required tests:** person present, entry/exit, object interaction fixture, event with supporting observations, invalid event rejected by schema.
**Acceptance criteria:** Tracks and observations generate `Event[]` conforming to canonical contracts.
**What NOT to implement:** Multi-camera event linking (that is EventGraph).
**Handoff produced for next member:** `Event[]` for Intelligence.
**Difficulty:** MEDIUM
**State:** SCAFFOLDED

### M1-006 — END-TO-END VISION PIPELINE RUNNER
**Owner:** Member 1
**Primary folder/files:** `vision/pipeline/`
**Purpose:** Connect all vision components into a runnable multi-camera pipeline.
**Inputs:** One or more video files + per-camera metadata/config.
**Outputs:** `Observation[]`, `Track[]`, `ReIdCandidate[]`, `Event[]`.
**Dependencies:** M1-005, M1-001, M1-002, M1-003, M1-004.
**Detailed implementation requirements:**
- **Per-camera pipeline:** video → frames → detection → tracking → event extraction (runs independently per camera)
- **Cross-camera stage:** tracks from multiple cameras → visual Re-ID candidates (M1-003)
- Uses adapters, never hardcodes model implementation in domain layer
- Accepts one or more video files with per-camera metadata/config
- Produces canonical: `Observation[]`, `Track[]`, visual `ReIdCandidate[]`, `Event[]`
- Supports local execution
- Does not require AWS
- Preserves mock mode
- Clear logging/error reporting
- No direct dependency on Member 2
- Member 1 still must NOT perform PACE or physical validation on Re-ID candidates
**Edge cases:** Pipeline failure mid-stream on one camera, single-camera input (produces events but no cross-camera Re-ID candidates), mismatched camera configs.
**Required tests:**
- Single-camera MP4 → produces `Observation[]`, `Track[]`, `Event[]` (no Re-ID candidates expected)
- **Two-camera Re-ID integration fixture:** two camera inputs → produces cross-camera `ReIdCandidate[]` with appearance similarity scores
- Contract validation on all outputs
**Acceptance criteria:** One or more demo MP4s can pass through the entire Vision layer and generate structured multi-camera output consumable by Member 2. Cross-camera Re-ID candidates are produced when two or more camera inputs are provided.
**What NOT to implement:** Physical feasibility evaluation, PACE checks, route validation, hypothesis ranking.
**Handoff produced for next member:** Full structured multi-camera visual evidence dataset.
**Difficulty:** HIGH
**State:** PLANNED

**MEMBER 1 RECOMMENDED EXECUTION ORDER:**
M1-005 → M1-001 → M1-002 → M1-003 → M1-004 → M1-006
*Why this order makes sense:* You need frames (M1-005) to detect objects (M1-001). You need detections to track (M1-002). You need tracks to extract embeddings (M1-003) and define semantic events (M1-004). Finally, the orchestrator (M1-006) ties it all together.

==================================================
# MEMBER 2 — FINAL INTELLIGENCE TODOs
==================================================

**AGENT STOP RULE:** The AI agent must NOT automatically continue into another member's responsibilities. When all assigned TODOs are complete: run `.\scripts\validate.ps1`. If validation fails: fix only failures caused by that member's changes. If failure belongs to another member: report it as an integration blocker instead of modifying their code.

Member 2 owns: `intelligence/`
Member 2 MUST NOT implement: real detector, real tracker, real Re-ID neural model, Bedrock, React UI, AWS infrastructure.
Member 2 consumes Member 1 contracts or mock equivalents.

### M2-001 — CameraGraph
**Owner:** Member 2
**Primary folder/files:** `intelligence/camera_graph/`
**Purpose:** Represent physical/topological connectivity between cameras/zones.
**Inputs:** Camera list, connectivity config.
**Outputs:** Graph topology.
**Dependencies:** None (uses mock cameras).
**Detailed implementation requirements:**
- in-memory initially
- deterministic
- load from mock/config data
- support directed or explicitly bidirectional edges
- no graph database required
- graceful unknown camera handling
- implement `add_camera()`, `add_connection()`, `neighbors()`, `is_reachable()`
**Edge cases:** Disconnected graph components, missing camera IDs.
**Required tests:** connected cameras, disconnected cameras, unknown camera, path reachability.
**Acceptance criteria:** Camera topology can be queried deterministically.
**What NOT to implement:** Neo4j or external graph DB.
**Handoff produced for next member:** Graph structure for MobilityGraph/PACE.
**Difficulty:** LOW
**State:** SCAFFOLDED

### M2-002 — MobilityGraph
**Owner:** Member 2
**Primary folder/files:** `intelligence/mobility_graph/`
**Purpose:** Represent observed/configured camera-to-camera movement statistics.
**Inputs:** `CameraTransition[]`.
**Outputs:** Travel constraints.
**Dependencies:** M2-001.
**Detailed implementation requirements:**
- implement `get_transition()`, `estimate_travel_window()`, `get_neighbors()`
- use CameraTransition contract
- minimum time, median, p10/p90 if available
- transition score/likelihood if supplied
- do not call arbitrary scores calibrated probabilities
- allow manually seeded transitions
- future learning can replace current implementation
**Edge cases:** Missing transition data, zero minimum time.
**Required tests:** known transition, unknown transition, impossible/unreachable transition, travel window retrieval.
**Acceptance criteria:** PACE can query travel constraints between cameras.
**What NOT to implement:** Machine learning path models.
**Handoff produced for next member:** Travel time estimates for PACE.
**Difficulty:** MEDIUM
**State:** SCAFFOLDED

### M2-003 — EventGraph
**Owner:** Member 2
**Primary folder/files:** `intelligence/event_graph/`
**Purpose:** Represent relationships among events/entities/evidence.
**Inputs:** Canonical `Event[]`.
**Outputs:** Event relationship graph.
**Dependencies:** M1 events (use mocks).
**Detailed implementation requirements:**
- in-memory
- canonical Event inputs
- deterministic relation storage/query
- no Neo4j dependency
- `get_related_events()`, `add_relation()`, query by entity/time/camera
- support relationships: OBSERVED_AT, PRECEDES, SUPPORTS, CONTRADICTS, POSSIBLY_CONTINUES_AS, ENTERED, LEFT, NEAR
**Edge cases:** Circular relationships, orphaned events.
**Required tests:** add event, add relation, retrieve related event, no relation, duplicate handling.
**Acceptance criteria:** Events can form a traversable evidence relationship graph.
**What NOT to implement:** External graph DB, LLM reasoning to build graph.
**Handoff produced for next member:** `EventGraph` for Reconstruction.
**Difficulty:** MEDIUM
**State:** SCAFFOLDED

### M2-004 — COMPLETE PACE EXPANSION
**Owner:** Member 2
**Primary folder/files:** `intelligence/pace/travel_time.py`
**Purpose:** Deterministic validation of physical constraints.
**Inputs:** ReIdCandidates, distances, times, geometry.
**Outputs:** `PhysicalConsistency` (PASS/FAIL/UNKNOWN).
**Dependencies:** M2-001, M2-002.
**Detailed implementation requirements:**
- expand existing logic to implement: `check_travel_time()`, `check_reachability()`, `check_temporal_overlap()`, `check_direction_consistency()`, `check_contradictions()`, `check_candidate_journey()`
- ALL checks are deterministic
- UNKNOWN must be used when evidence required for a decision is absent
- Golden test: appearanceSimilarity=0.91, distance=140m, availableTravelSeconds=16, minimumTravelSeconds=100 -> Expected: TRAVEL_TIME=FAIL, Candidate physical consistency=FAIL. Resulting hypothesis can be REJECTED.
**Edge cases:** Missing topology (UNKNOWN), insufficient direction data (UNKNOWN).
**Required tests:** feasible travel, unreachable cameras, simultaneous distant observations, missing topology, insufficient direction data, contradiction detection, composite journey with one failing sub-check.
**Acceptance criteria:** PACE can deterministically accept, reject, or mark unknown candidate journeys.
**What NOT to implement:** LLM calls, Bedrock, inventing distances/topology, turning Re-ID similarity into physical truth.
**Handoff produced for next member:** Validated `PaceCheck[]` for Hypotheses.
**Difficulty:** MEDIUM
**State:** PARTIAL

### M2-005 — Blind-Spot Reconstruction
**Owner:** Member 2
**Primary folder/files:** `intelligence/reconstruction/`
**Purpose:** Bridge gaps between last observation and next observation.
**Inputs:** Gap intervals, CameraGraph, MobilityGraph, PACE.
**Outputs:** Candidate `Hypothesis[]`.
**Dependencies:** M2-003, M2-004.
**Detailed implementation requirements:**
- produce multiple possible routes/hypotheses
- preserve gaps as UNKNOWN when evidence is insufficient
- no single authoritative story by default
- physically impossible routes removed/rejected
- supporting event/observation IDs attached
- route reasoning explainable
**Edge cases:** No path exists, all paths rejected by PACE.
**Required tests:** one plausible route, multiple routes, no route, impossible route, unknown route.
**Acceptance criteria:** `reconstruct_gap()` returns structured `Hypothesis[]`.
**What NOT to implement:** Inventing events inside the blind spot.
**Handoff produced for next member:** Plausible and Rejected `Hypothesis[]`.
**Difficulty:** HIGH
**State:** SCAFFOLDED

### M2-006 — Hypothesis Ranking
**Owner:** Member 2
**Primary folder/files:** `intelligence/hypotheses/`
**Purpose:** Rank competing hypotheses.
**Inputs:** `Hypothesis[]`.
**Outputs:** Sorted `Hypothesis[]`.
**Dependencies:** M2-005.
**Detailed implementation requirements:**
- deterministic scoring function
- document weights (appearance similarity, PACE results, route support, temporal continuity, supporting evidence count, transition score)
- do not call score probability unless calibrated
- rejected hypotheses remain available for explainability
- UNKNOWN supported
**Edge cases:** Ties, hypotheses with missing evidence.
**Required tests:** plausible > weak candidate, REJECTED never outranks valid hypothesis, tie handling, missing evidence.
**Acceptance criteria:** `rank()` returns stable ordered hypotheses.
**What NOT to implement:** LLM ranking.
**Handoff produced for next member:** Ranked Hypotheses.
**Difficulty:** HIGH
**State:** SCAFFOLDED

### M2-007 — Evidence Coverage
**Owner:** Member 2
**Primary folder/files:** `intelligence/evidence/`
**Purpose:** Show how much of reconstruction is directly observed vs inferred vs unknown.
**Inputs:** `Event[]`, `Hypothesis[]`.
**Outputs:** `EvidenceCoverage`.
**Dependencies:** M2-006.
**Detailed implementation requirements:**
- produce: `observedFraction`, `inferredFraction`, `unknownFraction`
- all in [0,1], usually sum approximately to 1.0
- normalization documented
- clearly labeled product transparency metric
- NOT described as scientific forensic certainty
**Edge cases:** Zero total time, overlapping events.
**Required tests:** fully observed, mixed, fully unknown, normalization.
**Acceptance criteria:** Valid `EvidenceCoverage` is produced for investigation.
**What NOT to implement:** Arbitrary confidence metrics.
**Handoff produced for next member:** `EvidenceCoverage` object.
**Difficulty:** LOW
**State:** SCAFFOLDED

**MEMBER 2 RECOMMENDED ORDER:**
M2-001 → M2-002 → M2-003 → M2-004 → M2-005 → M2-006 → M2-007

==================================================
# MEMBER 3 — FINAL AGENT / BACKEND / AWS TODOs
==================================================

**AGENT STOP RULE:** The AI agent must NOT automatically continue into another member's responsibilities. When all assigned TODOs are complete: run `.\scripts\validate.ps1`. If validation fails: fix only failures caused by that member's changes. If failure belongs to another member: report it as an integration blocker instead of modifying their code.

Member 3 owns: `agent/`, `services/api/`, `storage/`, `infra/aws/`
Member 3 MUST NOT implement: computer vision, graph algorithms, PACE physics logic, frontend rendering.

### M3-002 — Agent Tools Using Mocks
**Owner:** Member 3
**Primary folder/files:** `agent/tools/`
**Purpose:** Implement structured tools for the LLM.
**Inputs:** Tool arguments.
**Outputs:** Structured data.
**Dependencies:** M2 interfaces (use mocks).
**Detailed implementation requirements:**
- tools: `search_events()`, `get_event()`, `get_track()`, `get_camera_transition()`, `get_camera_neighbors()`, `check_physical_consistency()`, `get_hypotheses()`, `get_evidence()`, `verify_claim_support()`
- structured data in/out
- no raw free-form invented evidence
- operate against mocks first
- later replace mock repository without changing tool contract
**Edge cases:** Missing resources, invalid arguments.
**Required tests:** known event, missing event, PACE tool, evidence retrieval, invalid request.
**Acceptance criteria:** Fake agent can call structured ARGUS tools.
**What NOT to implement:** Intelligence logic inside tools.
**Handoff produced for next member:** Tool registry for Investigator.
**Difficulty:** MEDIUM
**State:** SCAFFOLDED

### M3-003 — Investigator Loop with FakeLLMClient
**Owner:** Member 3
**Primary folder/files:** `agent/orchestration/`
**Purpose:** Build full local orchestration BEFORE Bedrock.
**Inputs:** `InvestigationRequest`.
**Outputs:** `InvestigationResponse`.
**Dependencies:** M3-002, `VerifierInterface` (interface only — NOT the completed M3-004 implementation).
**Detailed implementation requirements:**
- Flow: InvestigationRequest → parse question → select tools → retrieve structured evidence → construct candidate claims → call verifier → InvestigationResponse
- FakeLLMClient initially
- During M3-003 development, use a **pass-through/mock verifier** that implements `VerifierInterface` but returns the response unchanged. This allows the orchestration loop to be built and tested without the real PACE-enforcing verifier.
- M3-004 later provides the real evidence/PACE verifier implementation that replaces the pass-through.
- structured response
- supporting event IDs required
- UNKNOWN allowed
- no fabricated OBSERVED claim
- no AWS required
**Edge cases:** LLM fails to output valid JSON, insufficient evidence.
**Required tests:** normal question, insufficient evidence, unknown event, multiple hypotheses, rejected candidate.
**Acceptance criteria:** Full local investigation works with mocks and a pass-through verifier.
**What NOT to implement:** Real AWS Bedrock calls, real PACE verification (that is M3-004).
**Handoff produced for next member:** Orchestration pipeline ready for real Verifier.
**Difficulty:** HIGH
**State:** SCAFFOLDED

### M3-004 — Verifier (Real PACE Enforcement)
**Owner:** Member 3
**Primary folder/files:** `agent/verifier/`
**Purpose:** Replace the pass-through verifier (from M3-003) with the real PACE-enforcing verifier.
**Inputs:** Raw LLM-generated `InvestigationResponse`.
**Outputs:** Verified `InvestigationResponse`.
**Dependencies:** PACE (M2-004 interfaces, use mocks until real), `VerifierInterface` (already defined). Does NOT depend on M3-003 completion — can be developed in parallel using the shared `VerifierInterface`.
**Detailed implementation requirements:**
- Implements `VerifierInterface`
- OBSERVED: must be directly backed by appropriate source evidence.
- INFERRED: must be backed by evidence and valid reasoning/PACE.
- UNKNOWN: used when evidence does not support conclusion.
- REJECTED: used for deterministically invalid hypothesis.
- cross-check all supportingEventIds
- invoke PACE where necessary
- reject nonexistent evidence references
- downgrade/remove unsupported claims
- never allow LLM to override PACE
**Edge cases:** Claim with partial support.
**Required tests:** fake event ID, unsupported OBSERVED claim, physically impossible claim, valid INFERRED claim, UNKNOWN case.
**Acceptance criteria:** No unsupported evidence claim can pass verifier. Replaces pass-through verifier in Investigator without changing orchestration code.
**What NOT to implement:** LLM self-verification loop.
**Handoff produced for next member:** Safe, verified `InvestigationResponse`.
**Difficulty:** HIGH
**State:** SCAFFOLDED

### M3-001 — BedrockLLMClient
**Owner:** Member 3
**Primary folder/files:** `agent/clients/bedrock.py`
**Purpose:** Replace FakeLLMClient through existing interface.
**Inputs:** Prompts, Tool specs.
**Outputs:** LLM responses.
**Dependencies:** AWS credentials.
**Detailed implementation requirements:**
- Amazon Bedrock client through boto3
- configurable model ID
- timeout/error handling
- tool-call support if chosen model supports it
- no hardcoded credentials
- no secrets in repo
- local fake mode remains supported
**Edge cases:** AWS throttling, context window exceeded.
**Required tests:** mocked Bedrock response, malformed output, AWS unavailable, timeout, config missing.
**Acceptance criteria:** Bedrock can replace FakeLLMClient without changing Investigator.
**What NOT to implement:** Agent loop logic (lives in Orchestrator).
**Handoff produced for next member:** Real intelligence capability.
**Difficulty:** MEDIUM
**State:** SCAFFOLDED

### M3-005 — Real API Wiring + Evidence Playback Endpoint
**Owner:** Member 3
**Primary folder/files:** `services/api/app/main.py`
**Purpose:** Replace mock-only behavior incrementally. Provide evidence playback metadata for frontend VideoPlayer.
**Inputs:** HTTP Requests.
**Outputs:** HTTP Responses (JSON).
**Dependencies:** M3-003.
**Detailed implementation requirements:**
- Endpoints must remain compatible with documented API.
- `POST /api/investigations` must invoke Investigator.
- `GET` endpoints must retrieve real repositories where implemented.
- **`GET /api/evidence/{evidence_id}` must return typed evidence playback metadata:**
  - `evidenceId`: string
  - `videoUrl`: playable local URL in local mode, OR presigned S3 URL in AWS mode
  - `cameraId`: source camera
  - `startTimestampMs`: clip start
  - `endTimestampMs`: clip end
  - `mimeType`: e.g. `video/mp4`
  - `expiresAt`: ISO timestamp (for presigned URLs; null for local)
  - Missing evidence → `NOT_FOUND` error response
  - This is the backend handoff required by Member 4 VideoPlayer (M4-001). **Member 4 must NOT construct storage URLs itself.**
- typed request/response
- standardized errors
- mock mode still works
- real mode must not silently fall back to fake data unless explicitly configured
**Edge cases:** Investigation timeout, malformed request body, expired presigned URL, evidence not found.
**Required tests:** investigation request, validation error, missing resource, real/mock switching, evidence playback metadata retrieval, missing evidence → NOT_FOUND.
**Acceptance criteria:** Frontend can use `VITE_USE_MOCKS=false` against real backend. `GET /api/evidence/{id}` returns typed playback metadata.
**What NOT to implement:** Business logic in routes, video transcoding.
**Handoff produced for next member:** Fully functional backend for Member 4, including evidence playback URLs.
**Difficulty:** MEDIUM
**State:** MOCK WORKING

### M3-006 — Storage Layer (Including Evidence Media)
**Owner:** Member 3
**Primary folder/files:** `storage/`
**Purpose:** Persist and retrieve data from DB/Object storage, including evidence media for playback.
**Inputs:** Domain objects, media files.
**Outputs:** Domain objects, playable media URLs.
**Dependencies:** None.
**Detailed implementation requirements:**
- Implement repository abstractions first.
- local repository implementation:
  - local file-based media storage returning local file URLs for evidence playback
- then AWS adapters: DynamoDB, S3
  - DynamoDB: events, tracks, investigations, structured evidence references
  - S3: videos, clips, evidence artifacts
  - S3 adapter must generate **presigned URLs** with configurable expiration for evidence playback
- **Evidence media retrieval interface** must support:
  - `get_evidence_media(evidence_id) → EvidencePlaybackMetadata` containing: `videoUrl`, `cameraId`, `startTimestampMs`, `endTimestampMs`, `mimeType`, `expiresAt`
  - Local implementation: returns `file:///` or local HTTP URL
  - AWS implementation: returns S3 presigned URL with expiration
  - Missing evidence → raise `NotFoundError`
- domain logic does not directly import boto3 everywhere
- local implementation for tests
- AWS implementation replaceable
- no secrets
**Edge cases:** DB connection failure, partial write, expired presigned URL, missing media file.
**Required tests:** Local CRUD tests, mocked DynamoDB/S3 tests, evidence media URL generation (local + presigned), missing media → NotFoundError.
**Acceptance criteria:** Agent/API can switch storage provider without rewriting business logic. Evidence playback URLs work in both local and AWS modes.
**What NOT to implement:** Graph database, video transcoding.
**Handoff produced for next member:** Persistence layer + evidence media URLs for M3-005 API.
**Difficulty:** MEDIUM
**State:** SCAFFOLDED

### M3-007 — AWS INFRASTRUCTURE & DEPLOYMENT
**Owner:** Member 3
**Primary folder/files:** `infra/aws/cdk/`
**Purpose:** Deploy ARGUS backend infrastructure after local system works.
**Inputs:** CDK code.
**Outputs:** Deployed AWS resources.
**Dependencies:** All prior M3 tasks.
**Detailed implementation requirements:**
- CDK application/stacks
- S3 bucket(s)
- DynamoDB table(s)
- API deployment
- Lambda and/or ECS/Fargate choice based on runtime requirements
- API Gateway if required
- IAM policies
- environment configuration
- logs/basic observability
- least privilege
- deployed health endpoint
**Edge cases:** Deployment rollback, missing permissions.
**Required tests:** Deploy success to test account.
**Acceptance criteria:** A deployed environment exists where `GET /api/health` returns HTTP 200, storage-backed API can access S3/DynamoDB, and mock/local development still works.
**What NOT to implement:** Deploy GPU infrastructure automatically, make AWS mandatory for local tests, couple domain code directly to AWS, put credentials in source.
**Handoff produced for next member:** Live API endpoint.
**Difficulty:** HIGH
**State:** PLANNED

**MEMBER 3 RECOMMENDED ORDER:**
M3-002 → M3-003 → M3-004 → M3-001 → M3-005 → M3-006 → M3-007

==================================================
# MEMBER 4 — FINAL FRONTEND TODOs
==================================================

**AGENT STOP RULE:** The AI agent must NOT automatically continue into another member's responsibilities. When all assigned TODOs are complete: run `.\scripts\validate.ps1`. If validation fails: fix only failures caused by that member's changes. If failure belongs to another member: report it as an integration blocker instead of modifying their code.

Member 4 owns: `apps/web/`
Member 4 MUST NOT: calculate PACE, calculate hypothesis scores, perform graph pathfinding, perform Re-ID, create agent reasoning, invent evidence.
Member 4 renders backend/intelligence outputs.

### M4-001 — VideoPlayer
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/components/VideoPlayer.tsx`
**Purpose:** Play evidence video synced with events.
**Inputs:** Evidence playback metadata from `GET /api/evidence/{id}` (provided by Member 3 M3-005). Contains `videoUrl`, `cameraId`, `startTimestampMs`, `endTimestampMs`, `mimeType`, `expiresAt`.
**Outputs:** Interactive video element.
**Dependencies:** M3-005 provides evidence playback URLs. **Member 4 must NOT construct storage/S3 URLs itself** — always consume the `videoUrl` returned by the backend.
**Detailed implementation requirements:**
- Plays demo video with timestamp overlay.
- Seekable by external state.
- Consume `videoUrl` from backend evidence playback metadata.
- In mock mode, use a placeholder or local demo video URL.
**Edge cases:** Video failed to load, missing codec, expired presigned URL, evidence not found (NOT_FOUND from API).
**Required tests:** Render test, prop update test, error state test (missing video).
**Acceptance criteria:** Video plays with timestamp matching data. Video URL is always sourced from backend, never constructed by frontend.
**What NOT to implement:** Video transcoding, URL construction/signing.
**Difficulty:** MEDIUM
**State:** PLANNED

### M4-004 — EventTimeline
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/timeline/EventTimeline.tsx`
**Purpose:** Renders events on time axis with epistemic colors.
**Inputs:** `Event[]`.
**Outputs:** Interactive timeline UI.
**Dependencies:** None.
**Detailed implementation requirements:**
- Render events sorted by time.
- **Render all four applicable epistemic states with canonical visual semantics:**
  - `OBSERVED` — Cyan/teal solid segments (directly camera-verified)
  - `INFERRED` — Purple/violet dashed or semi-transparent segments (deduced from evidence)
  - `UNKNOWN` — Gray dotted segments or gaps (no evidence available)
  - `REJECTED` — Red strikethrough or crossed-out segments (deterministically invalidated)
- Clickable to seek VideoPlayer.
- Legend or tooltip explaining each epistemic color.
**Edge cases:** Dense overlapping events, empty events, events with only UNKNOWN state, mixed states in dense timeframe.
**Required tests:** Render test for each of the 4 epistemic states, click handler test, empty state test, legend visibility test.
**Acceptance criteria:** Events visually track along a timeline. All four epistemic states (`OBSERVED`, `INFERRED`, `UNKNOWN`, `REJECTED`) are rendered with distinct, consistent, canonical visual styling.
**What NOT to implement:** Event deduplication logic, epistemic state calculation.
**Difficulty:** MEDIUM
**State:** PLANNED

### M4-003 — EvidenceCard
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/evidence/EvidenceCard.tsx`
**Purpose:** Displays single evidence item with provenance.
**Inputs:** `Event` or `Claim`.
**Outputs:** UI Card.
**Dependencies:** None.
**Detailed implementation requirements:**
- Show description, source camera, confidence.
- Display `EpistemicState` badge.
**Edge cases:** Missing descriptions.
**Required tests:** Render test.
**Acceptance criteria:** Clear rendering of a piece of evidence.
**What NOT to implement:** Evidence validation.
**Difficulty:** LOW
**State:** PLANNED

### M4-008 — PaceCheckCard
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/components/PaceCheckCard.tsx`
**Purpose:** Renders PASS/FAIL/UNKNOWN check with details.
**Inputs:** `PaceCheck`.
**Outputs:** UI Component.
**Dependencies:** None.
**Detailed implementation requirements:**
- Clearly show PASS (green), FAIL (red), UNKNOWN (gray).
- Display reasoning.
**Edge cases:** Missing reason string.
**Required tests:** Render all 3 states.
**Acceptance criteria:** PACE check result is unambiguously visible.
**What NOT to implement:** PACE math.
**Difficulty:** LOW
**State:** PLANNED

### M4-005 — EvidenceCoverageView
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/evidence/EvidenceCoverageView.tsx`
**Purpose:** Bar/ring chart of observed/inferred/unknown fractions.
**Inputs:** `EvidenceCoverage`.
**Outputs:** Visual chart.
**Dependencies:** None.
**Detailed implementation requirements:**
- Use simple CSS or lightweight library.
- Color code fractions.
**Edge cases:** Fractions don't perfectly sum to 100.
**Required tests:** Render correct proportions.
**Acceptance criteria:** Renders visual representation of coverage.
**What NOT to implement:** Coverage calculation math.
**Difficulty:** LOW
**State:** PLANNED

### M4-006 — UnknownGap
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/components/UnknownGap.tsx`
**Purpose:** Visualizes blind-spot intervals.
**Inputs:** Gap strings/intervals.
**Outputs:** UI Component.
**Dependencies:** None.
**Detailed implementation requirements:**
- Display explicitly as UNKNOWN (gray).
- Explain gap duration/context.
**Edge cases:** Extremely long gaps.
**Required tests:** Render test.
**Acceptance criteria:** Unknown gaps are explicitly visible, not hidden.
**What NOT to implement:** Gap inference.
**Difficulty:** LOW
**State:** PLANNED

### M4-007 — HypothesisComparison
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/hypotheses/HypothesisComparison.tsx`
**Purpose:** Side-by-side hypothesis scores + PACE checks.
**Inputs:** `Hypothesis[]`, `rejectedHypotheses[]`.
**Outputs:** Comparison UI.
**Dependencies:** None.
**Detailed implementation requirements:**
- List plausible vs rejected.
- Highlight PACE check failures on rejected ones.
- Show scores.
**Edge cases:** No rejected hypotheses, zero plausible hypotheses.
**Required tests:** Render with/without rejected, sort order test.
**Acceptance criteria:** User can compare why one hypothesis won over another.
**What NOT to implement:** Hypothesis ranking.
**Difficulty:** MEDIUM
**State:** PLANNED

### M4-002 — CameraGraphView
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/cameras/CameraGraphView.tsx`
**Purpose:** Renders camera topology as interactive graph.
**Inputs:** Camera list, edges.
**Outputs:** Visual graph.
**Dependencies:** None (use mock).
**Detailed implementation requirements:**
- Render nodes (cameras) and edges (transitions).
- Node highlighting.
**Edge cases:** Disconnected nodes.
**Required tests:** Render test.
**Acceptance criteria:** Topology is understandable visually.
**What NOT to implement:** Graph connectivity logic.
**Difficulty:** HIGH
**State:** PLANNED

### M4-010 — EventGraphView
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/event-graph/EventGraphView.tsx`
**Purpose:** Renders event relationship graph.
**Inputs:** Event nodes, relation edges.
**Outputs:** Visual graph.
**Dependencies:** None.
**Detailed implementation requirements:**
- Visual nodes for events, labeled edges for relationships.
**Edge cases:** Complex dense graphs.
**Required tests:** Render test.
**Acceptance criteria:** Relationships between evidence pieces are visible.
**What NOT to implement:** Relationship calculation.
**Difficulty:** HIGH
**State:** PLANNED

### M4-012 — Multi-Camera / Trajectory View
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/trajectory/TrajectoryView.tsx`
**Purpose:** Visually show how evidence connects across cameras.
**Inputs:** Route array, evidence context.
**Outputs:** UI Component.
**Dependencies:** None.
**Detailed implementation requirements:**
- display relevant cameras
- observed camera segments clearly marked
- inferred route visually different
- unknown/blind spots visibly different
- REJECTED candidate route clearly shown if selected
- route geometry comes from backend/intelligence data
- frontend does NOT compute route feasibility
**Edge cases:** Route containing unknown segments.
**Required tests:** Render observed, inferred, and rejected states.
**Acceptance criteria:** Judge/user can understand where subject was observed, inferred, unknown, or rejected.
**What NOT to implement:** Feasibility computation.
**Difficulty:** HIGH
**State:** PLANNED

### M4-009 — InvestigationReplay
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/investigation/InvestigationReplay.tsx`
**Purpose:** Step-through of investigation stages.
**Inputs:** Explicit investigation stage/status events supplied by the backend (if available).
**Outputs:** Sequential UI or unavailable state.
**Dependencies:** Backend must supply explicit stage/trace data in the API response.
**Detailed implementation requirements:**
- **Must NEVER fabricate agent reasoning or chain-of-thought.** The component may only render explicit, safe investigation stages/status events supplied by the backend.
- If no replay/stage data exists in the API response, the component must show an "unavailable" state or remain hidden. It must not invent or guess intermediate steps.
- Show progression from evidence gathering → PACE check → Conclusion ONLY if the backend provides structured stage events.
**Edge cases:** No stage data available (show unavailable state), partial stage data.
**Required tests:** Render with stage data, render unavailable state when no data, verify no fabricated reasoning.
**Acceptance criteria:** Component renders backend-supplied stages faithfully, or shows unavailable state. Zero fabricated content.
**What NOT to implement:** Orchestration logic, chain-of-thought generation, reasoning invention.
**Difficulty:** HIGH
**State:** STRETCH / BLOCKED ON BACKEND DATA

> **NOTE:** The current canonical `InvestigationResponse` contract has no `stages` or `trace` field. This component cannot be fully implemented until Member 3 defines and provides explicit investigation stage data through the API. Do NOT modify `packages/contracts/` to add this field — report it as an integration discussion item when M3-003 orchestration is complete. Until then, this task remains STRETCH.

### M4-011 — InvestigationQuery
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/features/investigation/InvestigationQuery.tsx`
**Purpose:** Allow the user to ask the actual investigation question.
**Inputs:** User text input.
**Outputs:** API submission, Loading UI.
**Dependencies:** None.
**Detailed implementation requirements:**
- question input
- submit state
- optional camera/time context if API supports it
- POST /api/investigations
- loading state
- validation error
- API failure
- UNKNOWN response
- render InvestigationResponse
- no direct intelligence logic
**Edge cases:** API timeout, blank query.
**Required tests:** Submit handler, loading state, error display.
**Acceptance criteria:** User can submit an investigation question and see response.
**What NOT to implement:** LLM prompt building.
**Difficulty:** MEDIUM
**State:** PLANNED

### M4-013 — Real API Integration
**Owner:** Member 4
**Primary folder/files:** `apps/web/src/services/api.ts` (expansion)
**Purpose:** Move frontend from mock-only demo to real backend.
**Inputs:** Real HTTP responses.
**Outputs:** Typed data to UI.
**Dependencies:** M3-005.
**Detailed implementation requirements:**
- `VITE_USE_MOCKS=true` must continue working.
- `VITE_USE_MOCKS=false` must call real API.
- Handle loading, error, empty, UNKNOWN, INFERRED, REJECTED, network failure, invalid response.
- No component rewrite should be required when switching from mock to real data.
**Edge cases:** 500 Server Error, CORS error.
**Required tests:** mock client, real API client with mocked HTTP, error response, successful InvestigationResponse.
**Acceptance criteria:** Phase 5 of integration checklist passes: `VITE_USE_MOCKS=false` renders real investigation response.
**What NOT to implement:** Backend routing.
**Difficulty:** MEDIUM
**State:** PLANNED

**MEMBER 4 RECOMMENDED DEVELOPMENT ORDER:**
M4-001 → M4-004 → M4-003 → M4-008 → M4-005 → M4-006 → M4-007 → M4-002 → M4-010 → M4-012 → M4-009 → M4-011 → M4-013
