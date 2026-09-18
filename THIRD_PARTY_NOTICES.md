# Third-Party Notices

ARGUS is a fresh, clean-room implementation.

**No source code from `CU-DrAgon/rocm-cctv-analysis` or any other existing CCTV repository has been or should be copied into ARGUS.**

## Currently Installed Libraries

### Python Backend (`services/api/requirements.txt`)

| Library | Version | Purpose | Where Used | License |
|---|---|---|---|---|
| FastAPI | 0.111.0 | API framework | `services/api/` | MIT |
| Uvicorn | 0.30.1 | ASGI server | `services/api/` | BSD-3-Clause |
| Pydantic | 2.8.2 | Data validation / contracts | `packages/contracts/python/` | MIT |
| Pytest | 8.2.2 | Test framework | `*/tests/` | MIT |
| HTTPX | 0.27.0 | Async HTTP test client | `services/api/tests/` | BSD-3-Clause |

### Node.js / React Frontend (`apps/web/package.json`)

| Library | Version | Purpose | Where Used | License |
|---|---|---|---|---|
| React | ^18.3.1 | UI framework | `apps/web/` | MIT |
| React DOM | ^18.3.1 | DOM rendering | `apps/web/` | MIT |
| Lucide React | ^0.435.0 | Icon library | `apps/web/` | ISC |
| Vite | ^5.4.1 | Build tool | `apps/web/` (dev) | MIT |
| TypeScript | ^5.5.3 | Type checker | `apps/web/` (dev) | Apache-2.0 |
| @vitejs/plugin-react | ^4.3.1 | Vite React plugin | `apps/web/` (dev) | MIT |

## Model Dependencies

### CURRENTLY INCLUDED
None. The repository uses `mocks/` data and does not ship or load any model weights.

### PLANNED / OPTIONAL (Member 1 will choose)

| Model | Role | Potential License | Notes |
|---|---|---|---|
| YOLOv8 / YOLO11 | Object Detection | AGPLv3 | **Caution**: AGPLv3 may impose distribution requirements |
| RT-DETR | Object Detection | Apache-2.0 | More permissive alternative |
| ByteTrack | Multi-object Tracking | MIT | VERIFY LICENSE BEFORE RELEASE |
| BoT-SORT | Multi-object Tracking | VERIFY LICENSE BEFORE RELEASE | |
| OSNet | Re-identification | VERIFY LICENSE BEFORE RELEASE | |
| YoutuReID | Re-identification | VERIFY LICENSE BEFORE RELEASE | |

## Large-Asset Policy

**Never commit to the repository:**
- Model weights (`.pt`, `.pth`, `.onnx`, `.engine`, `.safetensors`)
- Raw video files (`.mp4`, `.avi`, `.mov`)
- Generated frame images
- Large embedding databases

Place local development assets in:
- `.local/` — Personal local files (gitignored)
- `models/` — Downloaded model weights (gitignored)
- `demo-data/videos/` — Demo video files (gitignored)
