from .models import SceneBrief, ShotPlan


def score_plan(scene: SceneBrief, plan: ShotPlan) -> dict:
    beats = {s.beat for s in plan.shots}; coverage = len(beats & set(scene.required_beats)) / max(1, len(scene.required_beats))
    lens_steps = sum(abs(a.lens_mm-b.lens_mm) <= 50 for a,b in zip(plan.shots, plan.shots[1:])) / max(1, len(plan.shots)-1)
    movement_fit = sum((s.movement != "handheld") if scene.mood in ("quiet", "mysterious") else True for s in plan.shots) / max(1, len(plan.shots))
    diversity = len({s.size for s in plan.shots}) / max(1, len(plan.shots))
    budget = min(1.0, scene.max_seconds / max(1, sum(s.seconds for s in plan.shots)))
    total = round(0.35*coverage + 0.2*lens_steps + 0.2*movement_fit + 0.15*diversity + 0.1*budget, 4)
    return {"total": total, "coverage": round(coverage,4), "lens_continuity":round(lens_steps,4), "movement_fit":round(movement_fit,4), "diversity":round(diversity,4), "budget":round(budget,4)}

def train_scenes() -> list[SceneBrief]:
    return [SceneBrief(text="A detective enters a diner", mood="tense"), SceneBrief(text="A child discovers a glowing garden", mood="quiet")]

def hidden_scenes() -> list[SceneBrief]:
    return [SceneBrief(text="Two astronauts reconcile before launch", mood="mysterious"), SceneBrief(text="A chef races to save dinner service", mood="tense")]
