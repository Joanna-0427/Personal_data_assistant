from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def generate_report(summary_json_path: str, report_path: str) -> Path:
    """Generate a Markdown report from summary.json.

    Required sections:
    - Overview
    - Expenses summary (total, average)
    - Top categories table
    - Largest transactions
    - Notes: action items + topics
    - Enrichment (if present)

    TODO:
    - Make formatting clean and readable
    - Use Markdown tables where appropriate
    """
    summary = json.loads(Path(summary_json_path).read_text(encoding="utf-8"))

    expenses = summary.get("expenses", {})
    notes = summary.get("notes", {})
    enrichment = summary.get("enrichment")

    lines: List[str] = []
    lines.append("# Personal Data Assistant Report\n")

    # Overview
    lines.append("## Overview")
    lines.append(f"- Total spend: **${expenses.get('total_spend', 0):.2f}**")
    lines.append(f"- Average amount: **${expenses.get('average_amount', 0):.2f}**\n")

    # Top categories
    lines.append("## Top Categories")
    lines.append("| Category | Total |")
    lines.append("|---|---:|")
    for cat, total in expenses.get("top_3_categories_by_total", []):
        lines.append(f"| {cat} | {total:.2f} |")
    lines.append("")

    # Largest transactions
    lines.append("## Largest Transactions")
    lines.append("| Date | Category | Amount | Description |")
    lines.append("|---|---|---:|---|")
    for r in expenses.get("largest_5_transactions", []):
        lines.append(f"| {r.get('date','')} | {r.get('category','')} | {float(r.get('amount',0)):.2f} | {r.get('description','')} |")
    lines.append("")

    # Notes
    lines.append("## Notes — Action Items")
    for item in notes.get("action_items", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Notes — Topics")
    topics = notes.get("topics", {})
    if topics:
        lines.append("| Topic | Count |")
        lines.append("|---|---:|")
        for t, c in sorted(topics.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"| {t} | {c} |")
    else:
        lines.append("_No topics found._")
    lines.append("")

    # Enrichment
    lines.append("## Enrichment")
    if enrichment:
        lines.append(f"- Type: {enrichment.get('type')}")
        lines.append(f"- Source: {enrichment.get('source')}")
        lines.append(f"- Base/Target: {enrichment.get('base')}→{enrichment.get('target')}")
        lines.append(f"- Rate: {enrichment.get('rate')}")
    else:
        lines.append("_No enrichment performed._")

    out = Path(report_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
