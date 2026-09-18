# Team Workflow

ARGUS is built by a four-person team operating in parallel using mocks.

## Branches

| Branch | Owner |
|---|---|
| `main` | Locked — no direct pushes |
| `member1/vision-pipeline` | Member 1 |
| `member2/intelligence` | Member 2 |
| `member3/agent-backend` | Member 3 |
| `member4/frontend` | Member 4 |

## Folder Ownership

| Folder | Owner | Notes |
|---|---|---|
| `vision/` | Member 1 | Adapter protocols + model integration |
| `intelligence/` | Member 2 | Graph algorithms + PACE |
| `agent/`, `services/`, `infra/`, `storage/` | Member 3 | LLM agent + API + AWS |
| `apps/web/` | Member 4 | React frontend |
| `packages/contracts/`, `mocks/` | **TEAM** | Requires team approval |

## Cross-Member Ownership Boundaries

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

## Files Requiring Team Approval

- `packages/contracts/python/argus_contracts/*.py` — Canonical data models
- `packages/contracts/typescript/index.ts` — Must stay synchronized with Python
- `mocks/investigations/inv_001.json` — Golden demo fixture
- `pytest.ini` — Test configuration

If you change a contract, you must:
1. Get team sign-off
2. Run `python scripts/generate_schemas.py`
3. Update `packages/contracts/typescript/index.ts`

## Before Starting Work

```powershell
git checkout main
git pull origin main
git checkout <your-branch>
git merge main
```

## During Work

- **Stay in your owned folders.** Do not edit other members' code.
- **Use mocks** if you need data from another member.
- **No secrets**: Never commit AWS credentials, API keys, or `.env` files.
- **No heavy files**: Never commit model weights (`.pt`, `.onnx`), videos (`.mp4`), or embeddings.
- **No independent architecture redesigns**: Follow `ARCHITECTURE.md`.
- **Use TODO IDs from `STATUS.md`** (e.g. M1-001, M2-003).

## Before Push

```powershell
git status
.\scripts\validate.ps1
git add .
git commit -m "feat(module): description — M?-???"
git push origin <your-branch>
```

## Pull Request Process

1. Push your branch to GitHub.
2. Open PR against `main` using the template in `.github/pull_request_template.md`.
3. Require at least one approval from another member.
4. CI must pass (Python tests + frontend build).

## Merge Process

- Use Squash and Merge.
- After merge, all members sync:
```powershell
git checkout main
git pull origin main
git checkout <your-branch>
git merge main
```

## Merge Conflict Rules

- Conflicts in `packages/contracts/` → **STOP**. Notify the team. Shared contracts must be reconciled manually by the conflicting feature owners.
- Conflicts in your own folder → resolve yourself.

## AI Agent Instructions

If you are using an AI coding agent, start your session with:

> "I am Member X. Read `README.md`, `TEAM_WORKFLOW.md`, `STATUS.md`, `ARCHITECTURE.md`, and `FILE_MAP.md` before editing code. My TODO IDs start with MX-."

The agent MUST:
1. Inspect existing implementation before writing code
2. Not redesign the architecture
3. Not alter contracts without team approval
4. Stay within the member's owned folders
5. Address TODO IDs from `STATUS.md`
6. Run `.\scripts\validate.ps1` before stopping
7. Provide a summary of changed files

## Handoff Format

When your module is complete, post:

1. **Tasks completed** (e.g. M2-001, M2-002)
2. **Files changed** (list paths)
3. **Tests passed** (count + names)
4. **Environment requirements** (e.g. "requires YOLOv8 weights in `.local/models/`")
5. **Remaining TODOs** (list what's left)
6. **Integration instructions** (how to connect to next module)
7. **Branch pushed** (confirm)
