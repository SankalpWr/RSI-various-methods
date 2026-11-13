from rsi_lab.evals.runner import evaluate_policy
from rsi_lab.methods import aide2, dream_rsi, scientist2
from rsi_lab.problem.models import SceneBrief
from rsi_lab.problem.policies import Policy


def test_baseline_is_deterministic():
    scene=SceneBrief(text='test'); assert Policy().plan(scene)==Policy().plan(scene)

def test_score_is_bounded():
    assert 0 <= evaluate_policy(Policy())['mean'] <= 1

def test_three_methods_return_hidden_eval():
    assert dream_rsi.run(1)['hidden']['mean'] >= 0
    assert aide2.run(1)['hidden']['mean'] >= 0
    assert scientist2.run(2)['hidden']['mean'] >= 0
