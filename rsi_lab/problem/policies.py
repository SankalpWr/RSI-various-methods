from dataclasses import dataclass, replace

from .models import SceneBrief, Shot, ShotPlan

SIZES = ["wide", "medium", "close-up", "extreme-close-up"]
MOVES = ["locked", "pan", "push-in", "handheld", "track"]

@dataclass(frozen=True)
class Policy:
    name: str = "baseline"
    size_bias: tuple[str, ...] = ("wide", "medium", "close-up", "medium")
    lens_bias: tuple[int, ...] = (24, 35, 50, 85)
    movement_bias: tuple[str, ...] = ("locked", "pan", "push-in", "locked")
    duration: int = 8

    def mutate(self, knob: str, value):
        return replace(self, **{knob: value}, name=f"{self.name}+{knob}")

    def plan(self, scene: SceneBrief) -> ShotPlan:
        shots = []
        for i, beat in enumerate(scene.required_beats):
            shots.append(Shot(beat=beat, size=self.size_bias[i % len(self.size_bias)], lens_mm=self.lens_bias[i % len(self.lens_bias)], movement=self.movement_bias[i % len(self.movement_bias)], seconds=self.duration))
        return ShotPlan(shots=shots, policy_version=self.name)
