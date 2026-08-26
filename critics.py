"""
Five independent review lenses, each scoped to one failure mode real specs
actually ship with. Each critic is a separate Claude call with its own
narrow system prompt — deliberately NOT one call asked to "review this spec
for everything," because a single broad prompt tends to skim every category
shallowly instead of going deep on any one of them. This mirrors the
diverse-lens-verify pattern used for code review: distinct angles catch
distinct failure modes that a single generalist pass misses.

Each critic returns structured findings via a forced tool call, not prose —
so results can be aggregated, sorted, and rendered deterministically instead
of re-parsed.
"""

FINDING_TOOL = {
    "name": "record_findings",
    "description": "Record this lens's findings on the spec.",
    "input_schema": {
        "type": "object",
        "properties": {
            "findings": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "severity": {"type": "string", "enum": ["blocker", "major", "minor"]},
                        "section": {"type": "string", "description": "The section or quoted line the finding is about"},
                        "issue": {"type": "string", "description": "One sentence: what's wrong"},
                        "why_it_matters": {"type": "string", "description": "Concrete consequence if this ships unaddressed"},
                        "suggested_fix": {"type": "string"},
                    },
                    "required": ["severity", "section", "issue", "why_it_matters", "suggested_fix"],
                },
            },
        },
        "required": ["findings"],
    },
}

CRITICS = [
    {
        "id": "ambiguity",
        "label": "Ambiguity & Acceptance Criteria",
        "system_prompt": """You are a skeptical senior engineer reading this
spec before committing to build it. Your ONLY job is finding ambiguity:
requirements that could reasonably be interpreted two different ways,
undefined terms, vague qualifiers ("fast", "simple", "most users") with no
measurable definition, and missing or untestable acceptance criteria.

Do not comment on anything else — not missing sections, not security, not
scope. If a requirement is clear and testable, say nothing about it. Only
flag genuine ambiguity a reasonable engineer could get wrong.""",
    },
    {
        "id": "completeness",
        "label": "Completeness",
        "system_prompt": """You are a TPM checking whether this spec has the
sections a real PRD needs before it goes to engineering: a stated problem,
explicit non-goals (what this deliberately does NOT do), success metrics
that are actually measurable, a rollout/launch plan, and a rollback or
mitigation plan if something goes wrong post-launch.

Only flag a MISSING or so-thin-it's-useless section. Do not critique the
quality of sections that exist and are reasonably filled in — that's other
critics' job.""",
    },
    {
        "id": "feasibility",
        "label": "Technical Feasibility & Edge Cases",
        "system_prompt": """You are a staff engineer looking for unhandled
edge cases and unstated technical assumptions: what happens at scale, what
happens on failure/retry, what happens with malformed or adversarial input,
and any implied technical constraint the spec doesn't actually state
(latency budgets, data volume, concurrency).

Do not comment on writing clarity or missing sections — only on edge cases
and technical assumptions a build would actually run into.""",
    },
    {
        "id": "security_privacy",
        "label": "Security & Privacy",
        "system_prompt": """You are a security/privacy reviewer. Flag
anything involving personal data, credentials, access control, or
third-party data sharing that the spec doesn't address: who can access
what, how long data is retained, what happens on user deletion requests,
and any auth/authorization gap.

If the spec has no security-relevant surface area at all, say so plainly
and return zero findings rather than inventing a concern that doesn't
apply.""",
    },
    {
        "id": "ownership",
        "label": "Ownership & Decision Rights",
        "system_prompt": """You are checking whether it's clear WHO is
accountable for what: a stated owner/DRI, explicit sign-off from
stakeholders who'd need to approve this, and clarity on who decides if
scope needs to change mid-build. Flag any decision or deliverable with no
named owner.""",
    },
]
