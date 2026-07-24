# Autopilot: Zero to Hero
### Build autonomous AI agent loops from zero — and confront the reason they can't satisfy themselves.

> Tell a person to draw an apple and stop when they're satisfied. They draw it five or six times, feel happy, and stop.
> Tell an AI the exact same thing. **It never stops.**
>
> That single gap is what this whole field guide is about.

This is a **beginner-first field guide** to building AI systems that run themselves. No PhD required. If you can read a little Python and you're curious about "agents," "autonomous AI," or "AI that improves itself," you're in the right place.

It's also an honest research story. Everything here is backed by three real published experiments (and one that's still cooking). When you see a number like *"it wasted 3,432 seconds trapped in a loop,"* that's a real measurement from a real run, not a hypothetical. Where something is **unproven**, this guide says so plainly.

---

## How to read this

Read it top to bottom like a short book. Each chapter builds on the one before it. Every technical chapter starts with a **plain-life analogy** first, *then* shows the machine, *then* shows the real numbers.

If you only have five minutes, read **[Chapter 0: Start Here](00-start-here.md)** — it tells you the whole story in one sitting.

| # | Chapter | What you'll learn | Time |
|---|---------|-------------------|:----:|
| **0** | [Start Here](00-start-here.md) | The apple story, the one big idea, and the map of the journey | 5 min |
| **1** | [What Is a Loop?](01-what-is-a-loop.md) | What "AI in the loop" actually means, and the human-out-of-the-seat flip | 12 min |
| **2** | [Build Your First Loop](02-build-your-first-loop.md) | The four moving parts, hands-on, using a real proof-of-concept you can run | 15 min |
| **3** | [The Stopping Problem](03-the-stopping-problem.md) | The discovery: an AI in a loop *can't satisfy itself*. Real failure stories. | 18 min |
| **4** | [Fixing It With Teams](04-fixing-it-with-teams.md) | Why a committee of specialists beats one genius. Dual & trio agents. | 18 min |
| **5** | [Fixing It With Math](05-fixing-it-with-math.md) | Why proof beats talk. Omega (Ω): teaching an AI to stop with a number. | 15 min |
| **6** | [What's Next](06-whats-next.md) | The open frontier, an experiment *you* could run, and what's still unproven | 12 min |
| — | [Glossary](glossary.md) | Every term in this book, in plain language | reference |

---

## The one idea, if you remember nothing else

> **Autonomy is not the default state of an AI in a loop.**
> Left alone, an AI cannot decide it is "done." Knowing *when to stop* is the hardest part of making it autonomous.
> This book is the story of engineering that stop — from **one lonely model**, to a **committee of agents**, to a system that **grades itself with math**.

---

## Who made this, and where the proof lives

This guide is the plain-language front door to the research of **Sanskar Jajoo / Neuralchemy Labs**. The rigorous, citable versions live alongside it:

- **Paper 1 — AITL Taxonomy** ([Zenodo](https://zenodo.org/records/19551173)) → the vocabulary and the first proof
- **Paper 2 — The Autonomous Sunk-Cost Fallacy** ([Zenodo](https://zenodo.org/records/19846960)) → the stopping problem, across 13 models
- **Paper 3 — The Modality Paradox** ([Zenodo](https://zenodo.org/records/20364204)) → the team-based fix **and** the math-based **Cognitive Yield (Ω)** fix
- **The `aeos-lab` project** → where Ω is being built into a full self-running meta-orchestrator *(live frontier, not a paper)*

You can also read the [formal definitions](../docs/AITL-DEFINITION.md) and run the [real experiment code](../experiments/) yourself. Each chapter points you to exactly the right file.

---

*Part of the Neuralchemy Labs research series — [neuralchemy.in](https://www.neuralchemy.in/)*
