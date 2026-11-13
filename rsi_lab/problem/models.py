from pydantic import BaseModel, Field


class SceneBrief(BaseModel):
    text: str
    mood: str = "tense"
    required_beats: list[str] = Field(default_factory=lambda: ["establish", "detail", "reaction", "resolution"])
    max_seconds: int = 45

class Shot(BaseModel):
    beat: str
    size: str
    lens_mm: int
    movement: str
    seconds: int

class ShotPlan(BaseModel):
    shots: list[Shot]
    policy_version: str = "baseline"

class Candidate(BaseModel):
    name: str
    description: str
    score: float = 0.0
    plan: ShotPlan | None = None
    parent: str | None = None
    metadata: dict = Field(default_factory=dict)
