"""
Runs every critic lens against a spec, in parallel (five independent Claude
calls have no reason to run sequentially), and returns structured findings
per lens.
"""

import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import anthropic

from critics import CRITICS, FINDING_TOOL

sys.path.insert(0, str(Path(__file__).parent.parent / "agent-control-tower"))
try:
    from governed_client import GovernedClient
    _GOVERNANCE_AVAILABLE = True
except ImportError:
    _GOVERNANCE_AVAILABLE = False


def _make_client(api_key: str, daily_budget: float = None):
    if _GOVERNANCE_AVAILABLE:
        return GovernedClient("spec-review-agent", api_key=api_key, daily_budget=daily_budget)
    return anthropic.Anthropic(api_key=api_key)


def _run_one_critic(critic: dict, spec_text: str, model: str, api_key: str, daily_budget: float) -> dict:
    client = _make_client(api_key, daily_budget)
    msg = client.messages.create(
        model=model,
        max_tokens=2048,
        system=critic["system_prompt"],
        tools=[FINDING_TOOL],
        tool_choice={"type": "tool", "name": "record_findings"},
        messages=[{"role": "user", "content": f"Here is the spec:\n\n{spec_text}"}],
    )
    for block in msg.content:
        if block.type == "tool_use" and block.name == "record_findings":
            # Same lesson learned twice already elsewhere in this portfolio
            # (exec-status-rollup's judge output, slack-daily-agent's grader):
            # a forced tool schema marking "findings" as required does not
            # guarantee the model actually populates it — seen here with a
            # critic that had nothing to report omitting the key entirely
            # instead of returning an empty array. .get(), not [], and
            # validate the shape before trusting it's a list.
            findings = block.input.get("findings", [])
            if not isinstance(findings, list):
                findings = []
            return {"id": critic["id"], "label": critic["label"], "findings": findings}
    return {"id": critic["id"], "label": critic["label"], "findings": []}


def review_spec(spec_text: str, model: str, api_key: str, daily_budget: float = None) -> list:
    with ThreadPoolExecutor(max_workers=len(CRITICS)) as pool:
        futures = [pool.submit(_run_one_critic, c, spec_text, model, api_key, daily_budget) for c in CRITICS]
        return [f.result() for f in futures]
