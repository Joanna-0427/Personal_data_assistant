from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, stdev
from typing import Dict, List, Tuple

from .utils import ensure_dir


def read_cleaned_expenses(cleaned_csv_path: str) -> List[dict]:
    """Read cleaned_expenses.csv into a list of dicts."""
    rows: List[dict] = []
    with open(cleaned_csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        next(reader)
        for r in reader:
            rows.append(r)
    return rows


def analyze_expenses(cleaned_csv_path: str) -> dict:
    """Compute required statistics from cleaned CSV.

    Required:
    - total_spend
    - average_amount
    - count_by_category
    - total_by_category
    - top_3_categories_by_total
    - largest_5_transactions (by amount)
    - anomalies (simple rule, e.g. > mean + 2*std)

    TODO:
    - Convert amounts to float safely (they SHOULD be clean already)
    - Ensure outputs are JSON-serializable
    """
    rows = read_cleaned_expenses(cleaned_csv_path)

    amounts: List[float] = []
    total_by_cat: Dict[str, float] = defaultdict(float)
    count_by_cat: Dict[str, int] = defaultdict(int)

    parsed_rows: List[dict] = []
    for r in rows:
        amt = float(r["amount"])
        cat = r["category"]
        amounts.append(amt)
        total_by_cat[cat] += amt
        count_by_cat[cat] += 1
        parsed_rows.append({**r, "amount": amt})

    if not amounts:
        return {
            "total_spend": 0.0,
            "average_amount": 0.0,
            "count_by_category": dict(count_by_cat),
            "total_by_category": dict(total_by_cat),
            "top_3_categories_by_total": [],
            "largest_5_transactions": [],
            "anomalies": [],
        }

    avg = mean(amounts)
    sd = stdev(amounts) if len(amounts) >= 2 else 0.0
    threshold = avg + 2 * sd

    top3 = sorted(total_by_cat.items(), key=lambda x: x[1], reverse=True)[:3]
    largest5 = sorted(parsed_rows, key=lambda x: x["amount"], reverse=True)[:5]
    anomalies = [r for r in parsed_rows if r["amount"] > threshold]

    return {
        "total_spend": round(sum(amounts), 2),
        "average_amount": round(avg, 2),
        "count_by_category": dict(count_by_cat),
        "total_by_category": {k: round(v, 2) for k, v in total_by_cat.items()},
        "top_3_categories_by_total": [(k, round(v, 2)) for k, v in top3],
        "largest_5_transactions": largest5,
        "anomaly_rule": {"type": "mean_plus_2std", "threshold": round(threshold, 2)},
        "anomalies": anomalies,
    }


def analyze_notes(notes_json_path: str) -> dict:
    """Load notes_extracted.json."""
    return json.loads(Path(notes_json_path).read_text(encoding="utf-8"))


def write_summary(output_dir: str, summary: dict) -> Path:
    """Write summary.json to output_dir."""
    out_dir = ensure_dir(output_dir)
    out_path = out_dir / "summary.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def run_analyze(input_dir: str) -> Path:
    """Compute and write summary.json based on processed artifacts."""
    input_dir = str(Path(input_dir))
    cleaned_csv = str(Path(input_dir) / "cleaned_expenses.csv")
    notes_json = str(Path(input_dir) / "notes_extracted.json")

    expenses_summary = analyze_expenses(cleaned_csv)
    notes_summary = analyze_notes(notes_json)

    combined = {
        "expenses": expenses_summary,
        "notes": notes_summary,
    }
    return write_summary(input_dir, combined)
