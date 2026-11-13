from dataclasses import asdict

from ..evals.runner import evaluate_hidden, evaluate_policy, write_artifact
from ..problem.policies import Policy


def run(generations=3) -> dict:
    current = Policy(); log=[]
    knobs = [("duration",6),("duration",10),("lens_bias",(24,35,50,70)),("movement_bias",("locked","pan","push-in","track"))]
    for generation in range(generations):
        baseline = evaluate_policy(current); proposals=[]
        for knob, value in knobs:
            candidate = current.mutate(knob, value); proposals.append((evaluate_policy(candidate)['mean'], candidate))
        best_score, best = max(proposals, key=lambda x:x[0]); accepted = best_score > baseline['mean']
        if accepted: current = best
        log.append({"generation":generation,"inner_baseline":baseline["mean"],"outer_proposal":round(best_score,4),"accepted":accepted,"harness":asdict(current)})
    result={"method":"AIDE2-style","policy":asdict(current),"generations":log,"train":evaluate_policy(current),"hidden":evaluate_hidden(current)}
    result["artifact"] = write_artifact("aide2", result); return result
