# YouTube scripts — one video per part

## Part 1 — Problem and baseline (4 minutes)

Show the shot-planning problem, run the baseline command, open `models.py`, `policies.py`, and `benchmark.py`, and explain why a deterministic held-out evaluator is required before recursive improvement.

## Part 2 — Dream-RSI (5 minutes)

Run `python -m rsi_lab.cli dream-rsi --rounds 3`. Show the replay worlds, candidate mutations, offline score, acceptance gate, and final hidden score. Explain why replay reduces repeated online experimentation.

## Part 3 — AIDE²-style nested loop (5 minutes)

Run `python -m rsi_lab.cli aide2 --generations 3`. Draw the inner loop that makes shot plans and the outer loop that changes the inner policy. Show a rejected proposal and explain that acceptance depends on measured evaluation, not the model's confidence.

## Part 4 — AI Scientist-v2-style search (5 minutes)

Run `python -m rsi_lab.cli scientist2 --budget 12`. Show the experiment archive and top-four frontier. Explain progressive tree search, branch preservation, and pruning.

## Part 5 — Comparison, transfer, and safety (4 minutes)

Run `python -m rsi_lab.cli compare`, then `pytest -q`. Compare train versus hidden results and explain why a higher training score can still be overfitting. Show that generated code is never executed.

## Closing statement

“This is recursive self-improvement at the harness/policy level: the target agent is measured, the improvement mechanism proposes a change to itself, and an independent evaluator decides whether the change survives.”
