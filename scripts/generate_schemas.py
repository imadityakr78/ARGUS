import json
from pathlib import Path
from argus_contracts import (
    Camera, Observation, Track, ReIdCandidate, Event, 
    CameraTransition, Hypothesis, InvestigationRequest, 
    InvestigationResponse
)

def main():
    schemas_dir = Path(__file__).parent.parent / "packages" / "contracts" / "schemas"
    schemas_dir.mkdir(parents=True, exist_ok=True)
    
    models = {
        "Camera": Camera,
        "Observation": Observation,
        "Track": Track,
        "ReIdCandidate": ReIdCandidate,
        "Event": Event,
        "CameraTransition": CameraTransition,
        "Hypothesis": Hypothesis,
        "InvestigationRequest": InvestigationRequest,
        "InvestigationResponse": InvestigationResponse,
    }
    
    for name, model in models.items():
        schema_path = schemas_dir / f"{name}.json"
        with open(schema_path, "w") as f:
            json.dump(model.model_json_schema(), f, indent=2)
            
    print(f"Generated {len(models)} schemas in {schemas_dir}")

if __name__ == "__main__":
    main()
