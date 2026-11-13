from dataclasses import asdict

from ..evals.runner import evaluate_hidden, evaluate_policy, write_artifact
from ..problem.policies import Policy


def run(rounds=3) -> dict:
    current = Policy(); history = []; replay_worlds = []
    mutations = [
        lambda p: p.mutate("size_bias", ("wide","medium","close-up","extreme-close-up")),
        lambda p: p.mutate("lens_bias", (24,35,50,70)),
        lambda p: p.mutate("movement_bias", ("locked","pan","push-in","track")),
        lambda p: p.mutate("duration", 6),
    ]
    for round_id in range(rounds):
        live = evaluate_policy(current); replay_worlds.append({"round":round_id,"policy":current.name,"score":live["mean"]})
        dreamed = []
        for i, mutate in enumerate(mutations):
            candidate = mutate(current); score = sum(evaluate_policy(candidate, [s])['mean'] for s in __import__('rsi_lab.problem.benchmark',fromlist=['train_scenes']).train_scenes())/2
            dreamed.append((score, candidate))
        score, winner = max(dreamed, key=lambda x:x[0])
        if score > live['mean']: current = winner; accepted = True
        else: accepted = False
        history.append({"round":round_id,"live":live,"dreamed_best":round(score,4),"accepted":accepted,"policy":current.name})
    result = {"method":"Dream-RSI","policy":asdict(current),"history":history,"replay_worlds":replay_worlds,"train":evaluate_policy(current),"hidden":evaluate_hidden(current)}
    result["artifact"] = write_artifact("dream_rsi", result); return result
