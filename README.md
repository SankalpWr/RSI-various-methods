# RSI Lecture Suite: Self-Improving Shot Planning

This repository progressively implements three recursive self-improvement methods on one unique problem: improving an AI video-previsualization agent's cinematography shot plans.

Given a scene brief, the agent proposes a shot plan with shot size, lens, movement, and duration. A deterministic evaluator scores coverage, lens continuity, movement fit, diversity, and budget. The agent then improves the policy or search process—not the underlying model weights.

Implemented methods:

1. **Dream-RSI** — builds replay worlds from prior discovery trees and evaluates candidate exploration policies offline before deployment.
2. **AIDE²-style nested RSI** — an inner research agent solves shot-planning tasks while an outer loop modifies the inner harness/policy and retains only measured improvements.
3. **AI Scientist-v2-style progressive tree search** — an experiment manager expands, evaluates, and prunes a tree of cinematography hypotheses.

The code is fully local and deterministic by default. No API key is required. The implementation is pedagogical and method-inspired; it is not a reproduction of the original research codebases.

## Quick start

```bash
cd rsi-lecture-suite
python3 -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest -q
python -m rsi_lab.cli baseline --scene "A detective enters a rain-soaked diner to confront an old ally"
python -m rsi_lab.cli dream-rsi --rounds 3
python -m rsi_lab.cli aide2 --generations 3
python -m rsi_lab.cli scientist2 --budget 12
python -m rsi_lab.cli compare
```

See `docs/CODELAB_WALKTHROUGH.md` for the complete lecture walkthrough and `docs/YOUTUBE_SCRIPTS.md` for one recording script per part.

## Safety and evaluation

All candidate policies are data objects and are evaluated by allowlisted Python functions. The lab never executes model-written code. Every accepted change records a parent version, score, evaluator version, random seed, and artifact path. Hidden validation scenes are separate from training scenes to expose overfitting.

## GitHub and YouTube

This is GitHub-ready with CI and reproducible commands. The scripts are recording-ready, but this environment cannot publish to GitHub or YouTube without account authentication.
