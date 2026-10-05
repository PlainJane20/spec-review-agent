"""
Turns the critics' structured findings into a prioritized markdown report.
Plain Python, not another Claude call — the findings are already structured
data at this point; sorting and formatting them is a rendering problem, not
a language problem. Consistent with the same "deterministic where the task
is deterministic" discipline used in exec-status-rollup.
"""

SEVERITY_ORDER = {"blocker": 0, "major": 1, "minor": 2}
SEVERITY_EMOJI = {"blocker": "🔴", "major": "🟠", "minor": "🟡"}
UNKNOWN = "unknown"
UNKNOWN_EMOJI = "⚪"


def _sev(f: dict) -> str:
    """Normalize a finding's severity; anything outside the enum becomes 'unknown'."""
    sev = f.get("severity")
    sev = sev.strip().lower() if isinstance(sev, str) else None
    return sev if sev in SEVERITY_ORDER else UNKNOWN


def render_report(critic_results: list, spec_name: str) -> str:
    all_findings = []
    for cr in critic_results:
        for f in cr["findings"]:
            if not isinstance(f, dict):
                continue
            all_findings.append({**f, "severity": _sev(f), "lens": cr["label"]})

    counts = {"blocker": 0, "major": 0, "minor": 0, UNKNOWN: 0}
    for f in all_findings:
        counts[f["severity"]] += 1

    lines = [f"# Spec Review — {spec_name}", ""]
    lines.append(f"**{counts['blocker']} blocker(s) · {counts['major']} major · {counts['minor']} minor** "
                 f"across {len(critic_results)} independent review lenses"
                 + (f" ({counts[UNKNOWN]} with unrecognized severity)." if counts[UNKNOWN] else "."))
    lines.append("")

    if counts["blocker"] > 0:
        lines.append("⚠️ **This spec has blocking issues and should not move to engineering as-is.**")
        lines.append("")

    all_findings.sort(key=lambda f: SEVERITY_ORDER.get(f["severity"], len(SEVERITY_ORDER)))

    if not all_findings:
        lines.append("No findings from any lens — spec looks solid.")
        return "\n".join(lines)

    lines.append("## Findings (highest severity first)")
    lines.append("")
    for f in all_findings:
        emoji = SEVERITY_EMOJI.get(f["severity"], UNKNOWN_EMOJI)
        lines.append(f"### {emoji} [{f['severity'].upper()}] {f.get('issue', '(missing)')} — *{f['lens']}*")
        lines.append(f"- **Where:** {f.get('section', '(missing)')}")
        lines.append(f"- **Why it matters:** {f.get('why_it_matters', '(missing)')}")
        lines.append(f"- **Suggested fix:** {f.get('suggested_fix', '(missing)')}")
        lines.append("")

    lines.append("---")
    lines.append("## By lens")
    for cr in critic_results:
        status = f"{len(cr['findings'])} finding(s)" if cr["findings"] else "clean"
        lines.append(f"- **{cr['label']}**: {status}")

    return "\n".join(lines)
