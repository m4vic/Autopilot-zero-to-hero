<div align="center">

# Autopilot: Zero to Hero

### Research on why autonomous AI agents don't know when to stop, and three engineered fixes.

[![Paper 1: AITL Taxonomy](https://img.shields.io/badge/Paper_1-AITL_Taxonomy-red?logo=read-the-docs&logoColor=white)](https://zenodo.org/records/21535728)
[![Paper 2: Sunk-Cost Fallacy](https://img.shields.io/badge/Paper_2-Sunk_Cost_Fallacy-green?logo=read-the-docs&logoColor=white)](https://zenodo.org/records/21535645)
[![Paper 3: Modality Paradox](https://img.shields.io/badge/Paper_3-Modality_Paradox-blue?logo=read-the-docs&logoColor=white)](https://zenodo.org/records/21534310)
[![artifact: Page](https://img.shields.io/badge/artifact-yellow?logo=read-the-docs&logoColor=white)](https://claude.ai/code/artifact/4413a456-27c6-4791-9a14-199675072d76)

</div>

---

## Repository map

```text
Autopilot-Zero-to-Hero/
|
|-- paper/                         THE SCIENTIFIC MANUSCRIPTS
|   |-- paper1_taxonomy/               Paper 1 source, PDF, figures
|   |-- paper2_sunk_cost/              Paper 2 source, PDF, figures
|   `-- paper3_modality_paradox/       Paper 3 source, PDF, figures
|
|-- experiments/                   RUNNABLE LOOP CODE
|   |-- aitl_blind_nas/                Paper 1's proof of concept (agent, trainer, runner)
|   `-- modality_paradox/              Paper 3's team-loop experiment design and results
|
|-- aeos_sunk_cost/                RUNNABLE LOOP CODE
|   |-- runner.py                      the single-agent baseline (Paper 2)
|   |-- runner_critic.py               the two-agent reviewer/coder loop (Paper 3)
|   |-- runner_boundless.py            the extended-horizon sunk-cost study
|   `-- questionbook.md                every research question behind the experiments
|
|-- docs/                          FORMAL DEFINITIONS
|   |-- AITL-DEFINITION.md
|   |-- AITL-VS-HITL.md
|   `-- DESIGN-PRINCIPLES.md
|
|-- book/                          THE NARRATIVE FIELD GUIDE (same research, plain language)
|   |-- 00-start-here.md
|   |-- 01-what-is-a-loop.md
|   |-- 02-build-your-first-loop.md
|   |-- 03-the-stopping-problem.md
|   |-- 04-fixing-it-with-teams.md
|   |-- 05-fixing-it-with-math.md
|   |-- 06-whats-next.md
|   `-- glossary.md
|
|-- CITATION.cff                   how to cite this work
`-- LICENSE
```

*(An `archive/` folder with legacy drafts is kept locally only, it's excluded from GitHub via `.gitignore`.)*

## What this is

A three-paper research series on **autonomous agent stopping behavior**: what happens when you strip an AI agent of every hardcoded exit condition, give it nothing but its own results, and ask whether it can decide, on its own, that a task is finished.

Across 13 models and 132 runs, the finding holds up: almost none of them can. Left alone in a loop, an agent will grind past its own best result indefinitely, a failure mode we formalize as the **Autonomous Sunk-Cost Fallacy**. The three papers here build, test, and measure two working fixes for it: an asymmetric Reviewer/Coder architecture, and a self-scoring stop function (Cognitive Yield, Ω).

| | |
|---|---|
| **Paper 1** | AITL Taxonomy, the framework and the first proof of concept ([Zenodo](https://zenodo.org/records/19551173)) |
| **Paper 2** | AI In The Loop: The Autonomous Sunk-Cost Fallacy, the stopping problem measured across 13 models ([Zenodo](https://zenodo.org/records/19846960)) |
| **Paper 3** | AI In The Loop: The Modality Paradox, the Reviewer/Coder fix, its cross-modality twist, and the Cognitive Yield stopping function ([Zenodo](https://zenodo.org/records/20364204)) |

All experimental code, datasets, and figures are in this repository. See [`CITATION.cff`](CITATION.cff) for formal citation records.

## Read the full story

The research is also written up as a narrative field guide, no PhD required, that walks through the same findings from first principles: what an autonomous loop is, why it breaks, and how each fix works, with the real numbers from the papers throughout.

**[Read it here](https://claude.ai/code/artifact/4413a456-27c6-4791-9a14-199675072d76)**, one page, built to share directly, nothing to install or clone.

The same content also exists as Markdown chapters in this repo under [`book/`](book/00-start-here.md). Use that version if you'd rather read it natively on GitHub, edit it, or keep it offline with a clone; the linked page above is the same story, just formatted for sharing outside GitHub.

## Run it yourself

Copy `.env.example` to `.env` in a code folder and add your LLM API keys, or point it at a free local model, see the file headers.

```bash
# Paper 1's proof of concept: a single blind autonomous loop
cd experiments/aitl_blind_nas && python runner.py

# Paper 2: the single-agent sunk-cost study
cd aeos_sunk_cost && python runner.py

# Paper 3: the two-agent (reviewer + coder) fix
cd aeos_sunk_cost && python runner_critic.py
```

## The core finding, in one line

> Autonomy is not the default state of an AI in a loop. Left alone, an agent cannot decide it's "done", and knowing when to stop turns out to be the hardest part of making it autonomous.

The math-based fix (Cognitive Yield, Ω) from Paper 3 is being built into a full self-running meta-orchestrator in the sibling `aeos-lab` project, the active, unpublished frontier past these three papers.

> **Where things live:** GitHub hosts the runnable code, data, and the field guide. Zenodo hosts the permanent, citable preprint PDFs. Use the records in [`CITATION.cff`](CITATION.cff) for formal citations.

---

<div align="center">

*Neuralchemy Labs Research Series*

**New here? [Read the field guide](https://claude.ai/code/artifact/4413a456-27c6-4791-9a14-199675072d76)**

</div>
