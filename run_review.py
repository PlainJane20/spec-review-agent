#!/usr/bin/env python3
"""
Spec/PRD Quality Reviewer — five independent critic lenses review a spec
before it goes to engineering.

Usage:
  python run_review.py path/to/spec.md
  python run_review.py path/to/spec.md --out review.md
"""

import argparse
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

load_dotenv(Path(__file__).parent / ".env")

from reviewer import review_spec
from report import render_report

console = Console()


def _resolve_api_key() -> str:
    """Falls back to slack-daily-agent's .env if this repo's own .env
    doesn't have the key set — same sibling-repo credential reuse pattern
    used across this portfolio, so the same key doesn't get duplicated a
    fourth time."""
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key
    fallback = Path(__file__).parent.parent / "slack-daily-agent" / ".env"
    if fallback.exists():
        from dotenv import dotenv_values
        return dotenv_values(fallback).get("ANTHROPIC_API_KEY", "")
    return ""


def main():
    parser = argparse.ArgumentParser(description="Spec/PRD Quality Reviewer")
    parser.add_argument("spec_path", help="Path to the spec/PRD markdown file")
    parser.add_argument("--out", help="Save the report to this file")
    parser.add_argument("--model", default="claude-sonnet-5")
    parser.add_argument("--daily-budget", type=float, default=None)
    args = parser.parse_args()

    api_key = _resolve_api_key()
    if not api_key:
        console.print("[red]Missing ANTHROPIC_API_KEY[/]")
        sys.exit(1)

    spec_path = Path(args.spec_path)
    if not spec_path.exists():
        console.print(f"[red]File not found:[/] {spec_path}")
        sys.exit(1)

    spec_text = spec_path.read_text()
    console.print(f"[bold cyan]Running 5 critic lenses against {spec_path.name}...[/]")

    critic_results = review_spec(spec_text, args.model, api_key, args.daily_budget)
    report = render_report(critic_results, spec_path.name)

    console.print()
    console.print(Markdown(report))

    if args.out:
        Path(args.out).write_text(report)
        console.print(f"\n[green]✓[/] Saved to {args.out}")


if __name__ == "__main__":
    main()
