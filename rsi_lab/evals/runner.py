import json
from pathlib import Path

from ..problem.benchmark import hidden_scenes, score_plan, train_scenes
from ..problem.policies import Policy


def evaluate_policy(policy: Policy, scenes=None) -> dict:
    scenes = scenes or train_scenes()
    rows = [score_plan(scene, policy.plan(scene)) for scene in scenes]
    return {"mean": round(sum(r["total"] for r in rows)/len(rows),4), "rows": rows}

def evaluate_hidden(policy: Policy) -> dict: return evaluate_policy(policy, hidden_scenes())

def write_artifact(name: str, payload: dict, directory="artifacts") -> str:
    path = Path(directory); path.mkdir(exist_ok=True); target = path / f"{name}.json"; target.write_text(json.dumps(payload, indent=2)); return str(target)
