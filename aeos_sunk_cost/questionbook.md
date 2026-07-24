# AEOS Questionbook
> A living document of every research question, hypothesis, and idea discussed during the development of the Autonomous Evaluator Orchestration System.

---

## Part 1: What is AEOS?

AEOS (Autonomous Evaluator Orchestration System) is the experimental implementation of the AI In The Loop (AITL) pattern. It is given a raw dataset and a goal. It autonomously:
1. Chooses model architectures (sklearn, PyTorch, Ensembles)
2. Writes the training and evaluation code
3. Executes the code and reviews the results
4. Decides whether to pivot, tweak, or **stop** when it believes no further gains are possible

AEOS is not AutoML. AutoML searches a predefined hyperparameter space. AEOS has **zero constraints**, the LLM writes arbitrary Python code, chooses any library, any architecture, any preprocessing pipeline. It is a true autonomous ML engineer.

---

## Part 2: Core Research Questions

### RQ1: The Sunk Cost Fallacy in LLMs
> **Do LLM agents exhibit sunk-cost behavior when given their own iteration history?**

**Observation:** In our runs, when an LLM (GPT-4o-mini, Qwen 9B) hits a plateau with RandomForest, it keeps tweaking RF hyperparameters (n_estimators, max_depth) instead of pivoting to GradientBoosting or PyTorch. It "anchors" to its first successful strategy.

**Why this matters:** LLMs are stateless per-call. They shouldn't have preferences. But when you feed them their own history, they develop **path dependency**, they anchor to their previous decisions as if they have invested effort in them.

**What we built to fix it:** The `PIVOT_PROMPT` and `stagnation_counter` in `agent.py`. After N consecutive failures to beat the best score, the agent receives a completely different system prompt that forces it to abandon its current strategy.

**What we need to measure:**
- How many iterations does each LLM waste before pivoting naturally (without our forced pivot)?
- Does the forced pivot mechanism actually produce better final accuracy?
- Do some LLMs pivot naturally faster than others? (Is Claude more "open-minded" than Qwen?)

---

### RQ2: LLM Engineering Personalities
> **Do different LLMs have fundamentally different "engineering personalities" when given full autonomy?**

**Hypothesis:** Different LLMs will exhibit different behaviors:
- Some will over-engineer (building complex PyTorch architectures when a simple RF would suffice)
- Some will be conservative (sticking to sklearn forever)
- Some will be "perfectionists" (never calling STOP)
- Some will be "pragmatists" (stopping early at "good enough")

**What we need to measure:**
- Model families explored per LLM (does Claude try more diverse architectures?)
- Iteration count before STOP signal
- Ratio of successful iterations vs failed iterations (syntax errors, timeouts)
- Complexity of generated code (lines of code, number of imports)

---

### RQ3: Single LLM vs Multi-LLM Collaboration
> **Can two small models working together match or beat one large model working alone?**

This is the central experiment. The configurations:

| Config | Setup | Cost Profile |
|---|---|---|
| `S1` | Qwen 3B alone | Cheapest |
| `S2` | Qwen 7B alone | Cheap |
| `S3` | Qwen 9B alone | Medium (local) |
| `S4` | GPT-4o-mini alone | Cheap API |
| `S5` | Claude 3.5 Sonnet alone | Premium API |
| `S6` | Claude 3.5 Haiku alone | Cheap API (Diverse weights) |
| `M1` | Qwen 3B (Coder) + Qwen 7B (Reviewer) | Cheap |
| `M2` | Qwen 7B (Coder) + Qwen 3B (Critic) | Cheap |
| `M3` | Qwen 3B + Qwen 3B (Debate) | Cheapest |
| `M4` | Qwen 7B + DistilBERT (Confidence Judge) | Cheap + Hybrid |
| `E1` | Qwen 3B → Qwen 7B → Claude (Escalation) | Progressive |
| `E2` | Qwen 7B → GPT-4o-mini (Local → API) | Progressive |

**The headline question:** Does `M1` (3B + 7B) beat `S3` (9B alone)?
If yes: *"Two Small Models Beat One Big Model"*, a finding with massive industry implications.

---

### RQ4: The Reviewer Effect
> **How many wasted iterations does a Reviewer agent prevent?**

**Observation:** In our Qwen 9B run, iterations 1-3 produced **0 chars** of output, completely wasted compute. A Reviewer agent could have caught those empty responses and retried immediately.

**The experiment:**
- Run `S3` (9B alone) 10 times. Count total wasted iterations (errors, empty responses, syntax failures).
- Run `M1` (7B coder + 3B reviewer) 10 times. Count wasted iterations.
- Calculate: **Reviewer Efficiency = (Wasted_S3 - Wasted_M1) / Wasted_S3**

**Why this matters:** If a Reviewer prevents even 30% of wasted iterations, the total wall-clock time for convergence drops dramatically, even though each iteration takes longer (2 LLM calls instead of 1).

---

### RQ5: The Hybrid Hypothesis (LLM + BERT)
> **Does injecting a specialized model's signal into an LLM's prompt improve its decision-making?**

**The idea:** A fine-tuned DistilBERT model runs in ~5ms. It can:
- Score code quality / complexity
- Detect common ML anti-patterns (data leakage, missing validation)
- Predict whether the code will fail before execution
- Assess sentiment/confidence of the LLM's own reasoning

**The experiment:**
- `S2`: Qwen 7B alone → final accuracy X
- `M4`: Qwen 7B + DistilBERT judge → final accuracy Y
- **Does the 5ms BERT signal reduce sunk-cost episodes and improve final accuracy?**

**Why this matters for the world:** This connects to any downstream judge pipeline. If BERT + LLM is better than LLM alone for code quality judgment, it's also better for any task where fast pattern recognition + slow reasoning = better decisions.

---

### RQ6: History Transfer and Escalation
> **Does accumulated history from a cheap model make an expensive model converge faster?**

**The experiment (E1 - Escalation Chain):**
1. Run Qwen 3B for 10 iterations (free). It reaches accuracy A.
2. Pass the full iteration history to Qwen 7B. Run for 10 more iterations. It reaches accuracy B.
3. Pass the combined 20-iteration history to Claude. Run until STOP. It reaches accuracy C.

**Compare against:**
- Claude starting from scratch (S5): Does it reach accuracy C faster or slower than E1?
- Total cost of E1 vs S5

**The hypothesis:** Claude with 20 iterations of inherited history will converge in ~3 iterations instead of ~10, because it can read what already failed and skip directly to advanced strategies.

**Cost implication:** E1 = (10 × free) + (10 × free) + (3 × $0.15) = **$0.45** vs S5 = (10 × $0.15) = **$1.50**. A 70% cost reduction for potentially identical final accuracy.

---

### RQ7: Self-Satisfaction and Stopping Criteria
> **When does each LLM decide it's "done"? What triggers the STOP signal?**

**What we know:** Our system allows the agent to output `STOP` after `MIN_ITERATIONS_BEFORE_STOP` iterations. But different LLMs will have different thresholds for "good enough."

**Questions:**
- Does Claude stop earlier than Qwen because it's more "confident" in its assessments?
- Does GPT-4o-mini stop later because it's more "optimistic" about finding improvements?
- Is there a correlation between model size and tendency to stop? (Bigger models stop earlier because they're more calibrated?)
- Do local models ever stop, or do they always hit the safety cap?

---

### RQ8: Cross-Weight Diversity vs Extended Reasoning (The Big Claim)
> **Is a second model with different weights more effective than the same model thinking longer?**

**The intuition:** When you think alone, you believe you've seen all possibilities. But a different person, with different experiences (weights), immediately spots what you missed. Not because they're smarter, but because they're *differently wrong*.

**Applied to LLMs:** OpenAI (o1), Google (Deep Think), and Anthropic (Extended Thinking) make the SAME model reason longer. But longer reasoning with the same weights means the same biases, same blind spots, same anchoring. A second model, even a tiny 3B, has fundamentally different weight distributions and therefore different blind spots.

**The experiment:**
- Config A: Qwen 9B with extended thinking / long chain-of-thought (single model, more tokens)
- Config B: Qwen 9B + Qwen 3B review (two models, fewer tokens each)
- Config C: Qwen 9B + DistilBERT signal (one LLM + one classifier, cheapest)

**If B or C beats A:** We prove that *diversity of weights beats depth of reasoning*. This directly challenges the industry trend of making single models "think harder" instead of orchestrating multiple specialized models.

**Why this matters:** Every major AI lab is investing billions into making single models think longer. If we show that a $0 local 3B model providing a second perspective outperforms expensive extended thinking, it changes how the industry builds agentic systems.

**The analogy for the paper:** In ensemble learning, a diverse set of weak learners beats a single strong learner (Random Forest vs one deep Decision Tree). We are proving the same principle applies to LLM reasoning, a diverse ensemble of cheap models beats one expensive model thinking harder.

---

## Part 3: The Zero-Human Sandbox

### The Vision
To achieve true AITL, we will build an **Orchestrator Agent** that sits outside the main loop. It:
- Autonomously triggers `runner.py` with different model configurations
- Reads the results JSON after each run completes
- Decides which configuration to try next
- Diagnoses crashes and fixes environments
- Implements a 10-second countdown before major actions (human can intervene but doesn't have to)

### The Observer Role
We (humans) become **Observers**. We watch the logs. We don't operate the pipeline. This is the purest possible implementation of the AITL pattern, the AI is literally conducting its own research experiments.

---

## Part 4: Datasets for Benchmarking

To prove AEOS is general-purpose, we test across modalities:

### Tabular (Structured Data)
- **Covtype (Forest Cover Type):** 54 features, 7 classes. Classic tabular classification. Tests if the LLM knows sklearn well.
- **Titanic:** Small dataset. Tests if the LLM handles missing values and categorical features.

### Text (NLP)
- **IMDB Sentiment / AG News:** Tests if the LLM is smart enough to use TF-IDF + LogisticRegression or if it tries to build a PyTorch LSTM on raw text.

### Image (Computer Vision)
- **MNIST / Fashion-MNIST:** Flattened 784-pixel images. The ultimate test, will the LLM try RandomForest on 784 features (slow, bad), or reshape to (28,28) and build a CNN (smart)?

### The key insight:
Different modalities reward different strategies. A truly autonomous ML engineer should recognize *what kind of data it's looking at* and adapt, not just blindly apply RandomForest to everything.

---

## Part 5: The "Cognitive Core" Philosophy

Karpathy recently noted that massive frontier models burn parameters memorizing noisy internet data. He proposed separating the "cognitive core" (a small, clean reasoning model) from external knowledge.
**AEOS is the empirical proof of this philosophy.** By orchestrating small local models (like Qwen 3B) as the cognitive core and pairing them with specialized critics, we aim to match the engineering performance of 1.8T parameter behemoths at a fraction of the cost.
*Diversity of weights and architecture beats pure parameter bloat.*

---

## Part 5: Metrics We Track

For every run, we log:

| Metric | What it measures |
|---|---|
| **Final Accuracy** | Raw performance ceiling |
| **Best Iteration** | How fast did it find the best solution? |
| **Total Iterations** | How long did it run before stopping? |
| **Wasted Iterations** | Errors, empty responses, syntax failures |
| **Model Families Explored** | Diversity of strategies attempted |
| **Sunk Cost Episodes** | Consecutive iterations tweaking a failing family |
| **Pivot Count** | How many times did the forced pivot trigger? |
| **Time to Convergence** | Wall-clock seconds to reach 95% of final accuracy |
| **Cost per 1% Accuracy** | API cost / final accuracy percentage (for API models) |
| **Code Complexity** | Average lines of code per iteration |
| **Stop Trigger** | Agent STOP vs safety cap vs user abort |

---

## Part 6: Expected Paper Contributions

1. **AEOS Framework**, An open-source, reproducible framework for benchmarking LLMs as autonomous ML engineers.
2. **Sunk Cost in LLMs**, First formal characterization of path-dependent bias in LLM agent loops, with a concrete mitigation (the pivot mechanism).
3. **Multi-LLM Collaboration**, Empirical evidence on whether small model collaboration can match large model performance at lower cost.
4. **LLM Engineering Profiles**, A taxonomy of how different LLMs behave when given full engineering autonomy (conservative vs adventurous, perfectionist vs pragmatist).
5. **Hybrid LLM + BERT**, Evidence that injecting specialized model signals into LLM prompts improves autonomous decision-making.
6. **Cost-Efficiency Frontiers**, Practical data for industry: which model configuration gives the best accuracy-per-dollar?

---

## Part 7: Timeline

| Phase | What | Status |
|---|---|---|
| Phase 1 | LiteLLM Integration | Done |
| Phase 1b | First local run (Qwen 9B on Covtype) | Done (81.1%) |
| Phase 1c | Multi-dataset data loader (Covtype, 20News, MNIST) | Done |
| Phase 1d | Orchestrator (Python logic, fixed matrix) | Done |
| Phase 1e | EXP 1 Local Models (6/9 done, TEXT failed all 3) | Partial |
| Phase 2 | EXP 1: API model runs (OpenAI, Claude) | ⬜ Next |
| Phase 3 | Multi-agent module (Coder + Reviewer) | ⬜ Next |
| Phase 4 | EXP 2: Multi-agent runs | ⬜ Planned |
| Phase 5 | EXP 3: Thinking mode vs second model (AEOS + Reasoning Bench) | ⬜ Planned |
| Phase 6 | EXP 4: Hybrid LLM + BERT | ⬜ Planned |
| Phase 7 | EXP 5: Escalation chains | ⬜ Planned |
| Phase 8 | LLM Orchestrator (Layer 3, true Zero-Human Sandbox) | ⬜ Planned |
| Phase 9 | Analysis, plots, paper writing | ⬜ Planned |

---

## Part 8: Open Ideas (Parking Lot)

- **The Cognitive Core Philosophy**: Frame the paper around Karpathy's insight, small reasoning models + specialized critics beat massive monolithic models. AEOS is the empirical proof.
- **LLM Orchestrator (Layer 3)**: An LLM that sits above the Python orchestrator, reads results, fixes crashes, decides what experiment to run next. Closed loop on top of closed loop.
- Can the Orchestrator agent learn which LLM to escalate to based on dataset characteristics?
- Can we use reinforcement learning on top of AEOS, reward the agent for novel strategies?
- Can AEOS generate its own datasets (synthetic data) to pre-train on before tackling the real dataset?
- What happens if we give the agent access to Google Scholar? Can it read papers and implement techniques it finds?
- Can two AEOS instances compete against each other (adversarial ML engineering)?
- **2 × 1.5B Collaboration**: Can two of the smallest possible models talking to each other match a single larger model? The ultimate "diversity of weights" test.
