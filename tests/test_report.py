import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from report import render_report


def finding(severity, issue="issue", section="section"):
    return {"severity": severity, "section": section, "issue": issue,
            "why_it_matters": "matters", "suggested_fix": "fix it"}


def test_no_findings_reports_clean():
    report = render_report([{"id": "a", "label": "Lens A", "findings": []}], "spec.md")
    assert "No findings" in report


def test_blocker_triggers_warning_banner():
    report = render_report([{"id": "a", "label": "Lens A", "findings": [finding("blocker")]}], "spec.md")
    assert "should not move to engineering" in report


def test_no_blocker_no_warning_banner():
    report = render_report([{"id": "a", "label": "Lens A", "findings": [finding("minor")]}], "spec.md")
    assert "should not move to engineering" not in report


def test_findings_sorted_blocker_first():
    findings = [
        {"id": "a", "label": "Lens A", "findings": [finding("minor", "minor issue")]},
        {"id": "b", "label": "Lens B", "findings": [finding("blocker", "blocker issue")]},
    ]
    report = render_report(findings, "spec.md")
    assert report.index("blocker issue") < report.index("minor issue")


def test_counts_are_accurate():
    findings = [{"id": "a", "label": "Lens A", "findings": [finding("blocker"), finding("major"), finding("major")]}]
    report = render_report(findings, "spec.md")
    assert "1 blocker(s) · 2 major · 0 minor" in report


def test_by_lens_summary_lists_every_lens_even_when_clean():
    findings = [
        {"id": "a", "label": "Lens A", "findings": [finding("minor")]},
        {"id": "b", "label": "Lens B", "findings": []},
    ]
    report = render_report(findings, "spec.md")
    assert "**Lens B**: clean" in report
    assert "**Lens A**: 1 finding(s)" in report
