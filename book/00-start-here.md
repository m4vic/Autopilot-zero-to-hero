# Chapter 0 — Start Here

*The whole story in one sitting. ~5 minutes.*

---

## An experiment you can imagine right now

Hand a person a pencil and say:

> "Draw an apple. Keep going until you're satisfied, then stop."

What happens? They sketch. It's rough. They try again. Better. A third time, a fifth, maybe a tenth. Then something clicks — *"yeah, that's good enough"* — and **they put the pencil down.**

Now replace the person with an AI. Give it a task, the ability to try again and again, and the exact same instruction: *"keep improving until you're satisfied, then stop."*

Here's the strange part, and it's the reason this book exists:

> **The AI doesn't put the pencil down.**

It keeps going. And going. In one real experiment, an AI found an excellent solution — **99%+** accuracy — and then spent dozens more attempts grinding away, trying to claw back a final fraction of a percent it could never reach. Nobody told it to stop, so it didn't. It had to be switched off from the outside.

That's not a bug in one model. As you'll see, it happens across cheap models and expensive ones, small models and frontier giants. It points at something deeper:

> **An AI in a loop is not naturally autonomous. It doesn't know when it's done.**

## Why you should care

"Autonomous AI" is everywhere right now — agents that write code, run experiments, test other software, hunt for security holes, do research. The dream is simple: **set a goal, walk away, come back to a finished result.**

But if you actually build one of these loops (and by [Chapter 2](02-build-your-first-loop.md), you will), you smack straight into the wall above. The AI is happy to *start*. It's great at *trying things*. It just won't *finish on its own*. And a loop that never finishes is:

- **Expensive** — every extra try costs money (API calls) or electricity (your GPU).
- **Slow** — you're waiting on work that's already done.
- **Unsafe** — an autonomous system you can't trust to stop is one you have to babysit, which defeats the point.

This is the gap between "AI that does things" and "AI that runs itself." This book is about crossing it.

## The big idea

> **Autonomy is something you *engineer*. It is not something the AI gives you for free.**

The whole journey — the three published experiments this book is built on — is really the story of *trying to build a working "stop button" into an autonomous AI*, and discovering that this one small-sounding thing is surprisingly deep.

We solve it in three escalating ways, and that's the shape of the whole book:

```mermaid
    flowchart LR
    A["One Model<br/>alone in a loop"] -->|"can't stop —<br/>the problem"| B["A Team of Models<br/>one holds the STOP key"]
    B -->|"better, but the<br/>judge is still guessing"| C["A Math Score<br/>the AI grades itself"]
    C -->|"the number decides,<br/>not the talk"| D["Knows when<br/>to stop"]

    style A fill:#7f1d1d,stroke:#b91c1c,color:#fff
    style B fill:#1e3a8a,stroke:#1d4ed8,color:#fff
    style C fill:#064e3b,stroke:#047857,color:#fff
    style D fill:#374151,stroke:#6b7280,color:#fff
```

1. **One lonely model** ([Ch 3](03-the-stopping-problem.md)) — We put a single AI in charge of the whole loop and watch it fail to stop. This failure even has a human name: the **sunk-cost fallacy** — the same reason people keep pouring money into a losing bet because they've "already invested so much."

2. **A team of models** ([Ch 4](04-fixing-it-with-teams.md)) — We split the job. One AI does the work; a *different* AI watches over it and holds the power to call time. Why a *different* one? Because of an idea you already know from real life: **a committee of specialists often beats one lone genius.** Two minds that are "differently wrong" catch each other's blind spots.

3. **A math score** ([Ch 5](05-fixing-it-with-math.md)) — Finally, the cleanest fix. Instead of *asking* the AI "are you satisfied?" (which it will always talk itself out of), we make it **compute a number** from its own results. Because — as any stubborn arguer knows — **people trust proof over talk.** It's much harder to argue with your own math than with a sentence someone hands you. That number is called **Omega (Ω)**.

## What makes this guide different

Most explanations of "autonomous agents" are either hand-wavy hype or dense research papers. This one is neither:

- **It's honest.** These experiments have real wins *and* real failures. One entire result (Chapter 4) is a technique that **didn't work** on text — and we keep it in, because a map that only shows the roads that worked is a bad map.
- **It's grounded.** Every number traces back to a real run you can inspect in this repository.
- **It admits what it doesn't know.** The final chapter has a genuine open question — a bet the author believes but *hasn't been able to prove yet* — and hands you the exact experiment to go settle it.

## The map

| You are here | Where you're going |
|---|---|
| **Ch 0 · Start Here** ← *you are here* | The apple story and the big idea |
| [Ch 1 · What Is a Loop?](01-what-is-a-loop.md) | The core concept, from zero |
| [Ch 2 · Build Your First Loop](02-build-your-first-loop.md) | The four parts, hands-on |
| [Ch 3 · The Stopping Problem](03-the-stopping-problem.md) | Why one model can't stop |
| [Ch 4 · Fixing It With Teams](04-fixing-it-with-teams.md) | The committee of specialists |
| [Ch 5 · Fixing It With Math](05-fixing-it-with-math.md) | Proof beats talk: Omega |
| [Ch 6 · What's Next](06-whats-next.md) | The open frontier |

Every term that looks like jargon is defined in plain words in the **[Glossary](glossary.md)**. You never need to already know a word to keep reading.

Ready? **[→ Chapter 1: What Is a Loop?](01-what-is-a-loop.md)**
