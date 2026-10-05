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


def test_unknown_severity_does_not_crash_and_sorts_last():
    findings = [{"id": "a", "label": "Lens A", "findings": [
        finding("critical", "weird issue"), finding("minor", "minor issue"), finding("blocker", "blocker issue")]}]
    report = render_report(findings, "spec.md")
    assert "[UNKNOWN] weird issue" in report
    assert report.index("blocker issue") < report.index("minor issue") < report.index("weird issue")
    assert "1 with unrecognized severity" in report


def test_missing_or_non_string_severity_is_unknown():
    bad = {"issue": "no sev", "section": "s", "why_it_matters": "w", "suggested_fix": "f"}
    report = render_report([{"id": "a", "label": "L", "findings": [bad, finding(None, "none sev")]}], "spec.md")
    assert "[UNKNOWN] no sev" in report and "[UNKNOWN] none sev" in report


def test_severity_case_and_whitespace_normalized():
    report = render_report([{"id": "a", "label": "L", "findings": [finding(" Blocker ")]}], "spec.md")
    assert "1 blocker(s)" in report


def test_missing_fields_and_non_dict_findings_do_not_crash():
    report = render_report([{"id": "a", "label": "L", "findings": [{"severity": "major"}, "junk"]}], "spec.md")
    assert "(missing)" in report and "1 blocker(s) · 0 major" not in report and "0 blocker(s) · 1 major" in report
