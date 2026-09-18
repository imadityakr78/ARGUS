from typing import Optional
from pydantic import BaseModel, Field

class Position(BaseModel):
    x: float
    y: float
    z: float

class Camera(BaseModel):
    cameraId: str
    name: str
    zone: Optional[str] = None
    floor: Optional[int] = None
    position: Optional[Position] = None
    metadata: dict = Field(default_factory=dict)
