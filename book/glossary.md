# Glossary

*Every term in this book, in plain language. You never need to know a word before you read it — just come here.*

← [Back to Contents](README.md)

---

### AITL — AI In The Loop
A setup where an **AI** sits inside the try → check → adjust cycle, doing the checking and adjusting itself, with humans only watching from outside. The opposite of HITL. → [Chapter 1](01-what-is-a-loop.md)

### AEOS — Autonomous Empirical Optimization System
The name of the actual software test-bench used in this research. You give it a dataset and a goal; it writes its own machine-learning code, runs it, scores itself, and decides whether to keep going or stop. It's the "loop" from Chapter 2, grown up. → [Chapter 3](03-the-stopping-problem.md)

### Agent
An AI given a job and some freedom to act on its own — write code, run it, decide the next step. In this book, "agent," "model," and "AI" are used loosely for the same thing.

### Asymmetric loop
A team loop where the members have **deliberately different jobs** — e.g. one only writes code (the Coder), another only supervises and holds the stop button (the Reviewer). The opposite would be two identical copies doing the same thing. → [Chapter 4](04-fixing-it-with-teams.md)

### Blinding (Blind NAS)
Hiding what a dataset actually *is* — stripping its name and labels so the AI sees only raw shape ("54 features, 7 classes"). This stops the AI from reciting a memorized answer, so any improvement must come from the loop genuinely learning. "NAS" = Neural Architecture Search (searching for a good network design). → [Chapter 2](02-build-your-first-loop.md)

### CADS — Cognitive Agentic Diversity Score
A simple count of **how many genuinely different model families** are on a team. Two copies of the same model = CADS 1 (no diversity). A Qwen paired with a Llama = CADS 2. Higher CADS means more different blind spots get covered. → [Chapter 4](04-fixing-it-with-teams.md)

### Coder
In a team loop, the agent whose only job is to **write the machine-learning code** it's told to write. It doesn't decide strategy or when to stop. → [Chapter 4](04-fixing-it-with-teams.md)

### Convergence
When a loop settles down — the score stops improving because it's found its ceiling. Recognizing convergence (and then *stopping*) is the hard part this whole book is about.

### Epoch
One full pass of a model over its training data. "Train for 5 epochs" means show it all the data 5 times. A small detail from Chapter 2 — just know it's a unit of "how much training."

### Frontier model
The biggest, most capable (and most expensive) AI models — think GPT-5, Claude. Surprisingly, Chapter 3 found these were often the *worst* at stopping. → [Chapter 3](03-the-stopping-problem.md)

### HITL — Human In The Loop
The traditional setup where a **human** sits inside the loop, checking the AI's work and deciding the next step. Safe and accountable, but slow, costly, and impossible to scale. → [Chapter 1](01-what-is-a-loop.md)

### Iteration (round / lap)
One trip around the loop: the AI makes one attempt, gets one score, and adjusts. This book says "round" or "lap" for the same thing.

### LLM — Large Language Model
The kind of AI behind ChatGPT, Claude, and the models in this book. It reads and writes text (including code). "Model," "LLM," and "AI" are used interchangeably here.

### Loss
A number measuring how *wrong* a model is — lower is better. The mirror image of accuracy. When the loss curve trends **down** over a run, the loop is learning. → [Chapter 2](02-build-your-first-loop.md)

### Modality
The **kind of data** a problem involves — tables of numbers (tabular), images (vision), or words (text). A central finding (the *Modality Paradox*) is that the best autonomous behavior *changes depending on the modality*. → [Chapter 4](04-fixing-it-with-teams.md)

### Modality Paradox
The surprising discovery that a trait can be a **flaw in one modality and a superpower in another** — e.g. a stubborn reviewer is a disaster on easy table data (won't stop) but the best choice on hard image data (pushes through false dead-ends). → [Chapter 4](04-fixing-it-with-teams.md)

### Omega (Ω) / Cognitive Yield
A single **number the AI computes about its own recent results** — blending quality, progress, and wasted (crashed) attempts — that decides whether to continue, stop, pivot, or escalate. The "proof beats talk" fix: a number the AI can't argue its way past. Published in Paper 3 under the name **Cognitive Yield**; the code computes it as the score **Ω (Omega)**. → [Chapter 5](05-fixing-it-with-math.md)

### The four Omega actions
- **CONTINUE** — still improving, keep going.
- **STOP** — not improving but quality is good → you've won, quit.
- **PIVOT** — not improving and quality is poor → dead end, try something totally different.
- **ESCALATE** — too many crashes → something's broken, get help / a stronger model.
→ [Chapter 5](05-fixing-it-with-math.md)

### Path dependency
The odd tendency of an AI, once you feed it its own history, to act as if its earlier choices "matter" simply because they were its own — even though each AI call is technically a blank slate. The root of the sunk-cost trap. → [Chapter 3](03-the-stopping-problem.md)

### Reviewer
In a team loop, the agent that **never writes code** — it watches the whole history, sets strategy, and **holds the STOP key**. Because it isn't "invested" in the failing work, it can call time when the Coder can't. → [Chapter 4](04-fixing-it-with-teams.md)

### RLHF / instruction-tuning
The modern training step that teaches a model to follow instructions well and avoid pointless, circular behavior. Chapter 3's biggest clue: the ability to *stop gracefully* comes from this, **not** from a model's size or coding skill. → [Chapter 3](03-the-stopping-problem.md)

### Sunk-cost fallacy
The human bias of continuing to invest in something *because of what you've already spent*, even when quitting is smarter. ("We've come too far to stop now.") → [Chapter 3](03-the-stopping-problem.md)

### Autonomous Sunk-Cost Fallacy
The same bias, observed in AI agents: left alone in a loop, they keep grinding on a plateaued or failing strategy instead of stopping — the central discovery of this research. → [Chapter 3](03-the-stopping-problem.md)

### SCE — Sunk-Cost Episode
A countable unit of the trap: a stretch of **5+ rounds** where the score doesn't improve, the AI doesn't genuinely change approach, and it still won't stop. Counting SCEs turns "how stuck did it get?" into a hard number. → [Chapter 3](03-the-stopping-problem.md)

### Self-Generating / Self-Evaluating / Self-Improving / Human-Observed
The **four properties** that define an AITL system: the AI makes its own attempts, scores its own results, improves from those scores, and a human watches without operating each round. → [Chapter 1](01-what-is-a-loop.md)

### Validation accuracy
The model's score on data it has **never seen before** — the honest test of whether it truly learned rather than memorized. When it rises over many rounds, the loop is genuinely improving. → [Chapter 2](02-build-your-first-loop.md)

---

*Missing a term? The chapter links above take you to where each idea is explained in full. → [Back to Contents](README.md)*
