# Member Handoffs

This document defines what each member produces and consumes.

## Member 1 (Vision)
**Produces:**
- `Observation[]`
- `Track[]`
- `Event[]`
- `ReIdCandidate[]`

## Member 2 (Intelligence)
**Consumes:** Outputs from Member 1.
**Produces:**
- `EventGraph`
- `CameraMobilityGraph`
- `PaceCheck[]`
- `Hypothesis[]`
- `EvidenceCoverage`
- Reconstruction results

## Member 3 (Agent / Backend)
**Consumes:** Structured intelligence from Member 2.
**Produces:**
- `InvestigationResponse` (served via FastAPI)

## Member 4 (Frontend)
**Consumes:** `InvestigationResponse`, `Camera[]`, `Event[]` from Member 3.
**Produces:**
- Final UI Investigation Dashboard
