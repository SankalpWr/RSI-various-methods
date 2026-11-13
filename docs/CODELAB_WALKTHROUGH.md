# Section 10 RSI codelab walkthrough

## Problem selection

We improve a video-previsualization shot-planning agent. This is a useful RSI target because the agent's output is structured, the evaluator can be deterministic, and a policy improvement can be inspected by a filmmaker. The system optimizes coverage of story beats, lens continuity, movement fit, shot-size diversity, and total duration.

## Codelab 1 — Baseline and evaluator

```bash
python -m rsi_lab.cli baseline --scene "A detective enters a rain-soaked diner"
```

`SceneBrief`, `Shot`, and `ShotPlan` define the task. `Policy.plan()` converts a policy into a plan. `score_plan()` scores five interpretable dimensions and produces a single weighted objective. Run this before any RSI method. The important lesson is that self-improvement is meaningless without a stable evaluator and held-out scenes.

## Codelab 2 — Dream-RSI

```bash
python -m rsi_lab.cli dream-rsi --rounds 3
```

The online policy first creates a discovery record. That record is treated as a replay world. Candidate mutations are evaluated against the replay/training scenes without repeatedly deploying them. The best candidate is accepted only if it beats the live score. The implementation logs replay worlds, dreamed candidates, acceptance decisions, and a hidden score in `artifacts/dream_rsi.json`.

The code walkthrough is `rsi_lab/methods/dream_rsi.py`: current policy → replay snapshot → candidate mutations → offline scoring → gated deployment → next round. This captures the central idea of using history as a simulator rather than blindly executing every candidate.

## Codelab 3 — AIDE²-style nested RSI

```bash
python -m rsi_lab.cli aide2 --generations 3
```

The inner loop is the shot researcher that produces plans. The outer loop proposes changes to the inner harness/policy, benchmarks each change, and retains only measured improvements. `aide2.py` records the generation, baseline, proposal score, acceptance decision, and resulting harness. This demonstrates recursive scope: the object being optimized is the mechanism that performs the task.

## Codelab 4 — AI Scientist-v2-style tree search

```bash
python -m rsi_lab.cli scientist2 --budget 12
```

An experiment manager keeps a frontier of promising hypotheses, expands one parent at a time, evaluates the child, and prunes to the top four candidates. The archive is the experiment tree. Unlike simple hill climbing, the frontier preserves multiple branches so a temporarily weaker branch can remain available. The result is saved to `artifacts/scientist2.json`.

## Codelab 5 — Comparison and transfer

```bash
python -m rsi_lab.cli compare
```

Compare train and hidden means. Do not claim RSI success from training score alone. Inspect whether the change transfers to hidden scenes, whether the accepted policy remains interpretable, and whether the improvement is worth its evaluation budget.

## Safety and reproducibility

The repository never executes generated code. Policy mutations are typed data. The evaluator is allowlisted and versioned by the repository commit. Artifacts include the method, policy, history/tree, training score, and hidden score. For a real model-backed experiment, run the agent in a container with network and filesystem permissions restricted, pin dependencies, record model/version/cost, and require human approval before changing production harness code.

## What is and is not reproduced

These codelabs reproduce the core teaching patterns of Dream-RSI, AIDE², and AI Scientist-v2 on a small local benchmark. They do not reproduce the papers' frontier models, task suites, compute budgets, or published numbers. The repository's results are classroom measurements only.
