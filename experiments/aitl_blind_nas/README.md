# Blind NAS Tuner

> **New here?** This is the code behind **[Chapter 2 · Build Your First Loop](../../book/02-build-your-first-loop.md)** of the beginner field guide. Read that first for the plain-language walkthrough, then come back here to run it.

This directory contains the Proof-of-Concept (PoC) for the Artificial Intelligence In The Loop (AITL) paper.

**Goal**: Prove the AITL self-improving property mathematically by forcing an LLM to optimize a neural network via empirical feedback loops, negating its ability to guess the answer via pre-training bias.

Please read [`concept.md`](concept.md) first to understand the methodology and necessity of this architecture.

## Structure

* `concept.md`: Detailed explanation of the blinding methodology.
* `agent.py`: The LLM agent logic that generates PyTorch configurations (the Self-Generating part).
* `trainer.py`: The local runner that builds, trains, and evaluates the generated PyTorch models (the Self-Evaluating part).
* `data_loader.py`: Loads the obscured ("blinded") dataset.
* `runner.py`: The orchestrator linking the agent and the trainer, and spinning the loop.

## Run it

```bash
cd experiments/aitl_blind_nas
python runner.py
```

By default this drives the loop with OpenAI's `gpt-4o-mini` (set `OPENAI_API_KEY` first). To run a **free, fully-local** model instead, see the configuration block at the top of [`runner.py`](runner.py). Watch `results/` for the loss curve trending **downward**, that falling line is the self-improving property made visible.
