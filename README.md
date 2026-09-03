<img src="docs/spec-review-agent-banner.svg" alt="Spec Review Agent — Multi-Agent Requirements Quality" width="100%" />

# Spec Review Agent

### *Parallel pre-build review across ambiguity, feasibility, privacy, completeness, and ownership*

<div align="center">

[![Python 3.9+](https://img.shields.io/badge/Python_3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Claude](https://img.shields.io/badge/Powered_by-Claude-D97757?style=for-the-badge&logo=anthropic&logoColor=white)](https://www.anthropic.com/)
[![5 Critic Lenses](https://img.shields.io/badge/Review_lenses-5_independent-1baf7a?style=for-the-badge)](critics.py)
[![Tests](https://img.shields.io/badge/Unit_tests-6_passing-2a78d6?style=for-the-badge)](tests/)

</div>

Five independent critic lenses review a spec/PRD before it goes to
engineering — ambiguity, completeness, technical feasibility, security/
privacy, and ownership — each a separate Claude call with a narrow system
prompt, not one call asked to review everything at once.

**Why this exists:** every other agent in this portfolio reads *live
operational data* (Slack, Jira) and summarizes or scores it. This one
reviews a *document a human wrote*, before it ever reaches engineering —
the same rigor code review applies to a diff, applied to a spec instead.
Zero new API setup: it reads a local markdown file, so it's also the
fastest thing in this series to demo live with a real spec on the spot.

> **The competency this is really practicing:** running independent,
> narrow-scoped critic agents in parallel and merging their findings
> deterministically, rather than one do-everything prompt. AI code
> review has real, named, funded incumbents (CodeRabbit, Graphite, and
> others); AI *spec/PRD* review specifically as a standalone, multi-lens
> tool didn't turn up an equally obvious set of dedicated competitors in
> a broader market pass — though that's a hunch worth testing further,
> not a dedicated search of this exact niche.

> **Related work in this portfolio:** not a connected pipeline with
> anything else here — this is the only agent in the series reviewing a
> static document instead of live operational data. The real link is a
> shared bug, not a shared pipeline:
> [incident-postmortem-agent](https://github.com/PlainJane20/incident-postmortem-agent)
> hit the exact same "a forced tool-call schema doesn't guarantee the
> model actually populates every required field" failure described below
> — the 4th time it's shown up in this portfolio, after this repo and
> [exec-status-rollup](https://github.com/PlainJane20/exec-status-rollup)
> and [slack-daily-brief](https://github.com/PlainJane20/slack-daily-brief).
> [agent-control-tower](https://github.com/PlainJane20/agent-control-tower)'s
> cost/audit hook in the architecture diagram below is a real, optional
> integration point, not vaporware — but the two agents it's actually
> retrofitted onto live are exec-status-rollup and slack-daily-brief, not
> this one.

## At a glance

| | |
|---|---|
| **Problem** | Ambiguous ownership, missing controls, and infeasible assumptions often reach engineering before they are challenged |
| **Approach** | Five independent, narrow critic passes run in parallel and merge into a deterministic report |
| **Proof** | Reviewed a real intake specification and preserved a clean result when one lens found no issue |
| **Output** | Severity-ranked findings with evidence, remediation, ownership, and clean-lens reporting |

## Competencies demonstrated

| Competency | Observable evidence |
|---|---|
| Requirements quality | Tests ambiguity and completeness before implementation begins |
| Architecture partnership | Surfaces feasibility and interface concerns without pretending to replace architects |
| Security and privacy | Provides a dedicated data/control lens rather than a generic catch-all prompt |
| Ownership design | Converts vague follow-ups into named accountability gaps |
| Multi-agent orchestration | Parallel isolated calls are validated, normalized, sorted, and rendered deterministically |

## Why five separate calls, not one

A single prompt asked to "review this spec for everything" tends to skim
every category shallowly instead of going deep on any one. Each critic here
gets a narrow, single-purpose system prompt and is explicitly told to
ignore everything outside its lens — the ambiguity critic is told not to
comment on missing sections, the completeness critic is told not to
critique the quality of sections that already exist. Five focused passes,
run in parallel via `ThreadPoolExecutor`, catch more real issues than one
generalist pass over the same document.

## Real output, against a real document

Ran against [`pm-automation-system`](https://github.com/PlainJane20/pm-automation-system)'s
actual `IT_Project_Intake_Form_MVP.md` — both files are in
[`sample_specs/`](sample_specs/) as evidence, not illustration. The Technical
Feasibility lens correctly returned *zero* findings (reported as "clean" in
the summary) rather than inventing something to say — the other four lenses
found real issues: a generic contact placeholder instead of a named owner,
undefined domain-restriction on form access, and personal/budget data
being copied into a more widely-visible Jira project with no redaction
guidance.

## A real bug found building this

The same failure mode caught twice already elsewhere in this portfolio
(`exec-status-rollup`'s judge output, `slack-daily-agent`'s grader): a
forced tool-call schema marking a field `required` does **not** guarantee
the model actually populates it. One critic here — the one with genuinely
nothing to report — omitted the `findings` key from its tool call entirely
instead of returning an empty array, which crashed a `dict["findings"]`
lookup with a `KeyError`. Fixed with `.get("findings", [])` plus a type
check, and it now correctly renders as "clean" instead of crashing. Three
data points is a pattern: **never trust a forced-schema field to be present
just because the schema said it must be** — validate it every time.

## Architecture

```mermaid
flowchart LR
    Spec[("spec.md")] --> R["reviewer.py<br/>ThreadPoolExecutor: 5 parallel calls"]
    R --> C1["Ambiguity"]
    R --> C2["Completeness"]
    R --> C3["Feasibility"]
    R --> C4["Security & Privacy"]
    R --> C5["Ownership"]
    C1 & C2 & C3 & C4 & C5 --> Report["report.py<br/>deterministic sort + render"]
    Report --> Out[("Markdown report")]
    R -.->|cost + audit, optional| GCT["agent-control-tower"]
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # or leave blank to reuse ../slack-daily-agent's key
python -m pytest tests/ -v
```

## Usage

```bash
python run_review.py path/to/spec.md
python run_review.py path/to/spec.md --out review.md
python run_review.py path/to/spec.md --daily-budget 1.00   # via agent-control-tower if present
```

## Contact

<div align="center">

### **Navi Sohi**
*Technical Program Manager & Automation Engineer*

<br>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/navisohi/)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/PlainJane20)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](https://mail.google.com/mail/?view=cm&fs=1&to=nks.ai.dev@gmail.com)

<br>

</div>
