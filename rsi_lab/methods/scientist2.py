from dataclasses import asdict

from ..evals.runner import evaluate_hidden, evaluate_policy, write_artifact
from ..problem.policies import Policy


def run(budget=12) -> dict:
    root=Policy(); frontier=[(evaluate_policy(root)['mean'],root)]; archive=[]; knobs=[("duration",6),("duration",10),("lens_bias",(24,35,50,70)),("movement_bias",("locked","pan","push-in","track")),("size_bias",("wide","medium","close-up","extreme-close-up"))]
    for step in range(budget):
        _, parent=max(frontier,key=lambda x:x[0]); knob,value=knobs[step%len(knobs)]; child=parent.mutate(knob,value); score=evaluate_policy(child)['mean']; archive.append({"step":step,"parent":parent.name,"change":knob,"score":round(score,4)})
        frontier.append((score,child)); frontier=sorted(frontier,key=lambda x:x[0],reverse=True)[:4]
    _,winner=max(frontier,key=lambda x:x[0]); result={"method":"AI-Scientist-v2-style","policy":asdict(winner),"tree":archive,"train":evaluate_policy(winner),"hidden":evaluate_hidden(winner)}
    result["artifact"] = write_artifact("scientist2", result); return result
