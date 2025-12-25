from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Dict, List, Tuple

from .utils import ensure_dir
from .validate import validate_row


ACTION_KEYWORDS = ("TODO", "ACTION", "FOLLOW UP", "FOLLOW-UP", "NEXT")


def ingest_csv(csv_path: str, output_dir: str) -> Tuple[Path, Path]:
    """Read CSV, validate rows, write cleaned + rejected CSV.

    Outputs:
      - cleaned_expenses.csv
      - rejected_rows.csv

    TODO:
    - Use csv.DictReader for reading
    - For rejected rows: include an 'error' column with reason
    - Log counts
    - Return output Paths (cleaned_path, rejected_path)
    """
    out_dir = ensure_dir(output_dir)
    cleaned_path = out_dir / "cleaned_expenses.csv"
    rejected_path = out_dir / "rejected_rows.csv"

    cleaned_rows: List[Dict[str, str]] = []
    rejected_rows: List[Dict[str, str]] = []

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ok, cleaned, err = validate_row(row)
            if ok and cleaned:
                cleaned_rows.append(cleaned)
            else:
                row = dict(row)
                row["error"] = err or "Unknown error"
                rejected_rows.append(row)

    # TODO: write cleaned_path (columns: date, amount, category, description)
    with open(cleaned_path,'w') as file:
        write = csv.DictWriter(file,fieldnames=['date','amount','category','description'])
        write.writeheader()
        for rows in cleaned_rows:
            write.writerow({'date':rows['date'],'amount':rows['amount'],'category':rows['category'],'description':rows['description']})
    # TODO: write rejected_path (original columns + error)
    with open(rejected_path,'w') as file:
        write = csv.DictWriter(file,fieldnames=['date','amount','category','description','error'])
        write.writeheader()
        for rows in rejected_rows:
            write.writerow({'date':rows['date'],'amount':rows['amount'],'category':rows['category'],'description':rows['description'],'error':rows['error']})

    logging.info("Ingest CSV: cleaned=%s rejected=%s", len(cleaned_rows), len(rejected_rows))
    return cleaned_path, rejected_path


def ingest_notes(notes_path: str, output_dir: str) -> Path:
    """Read notes.txt and extract action items + hashtag topics.

    Output:
      - notes_extracted.json with keys:
          action_items: list[str]
          topics: dict[str,int]
          total_lines: int

    TODO:
    - Extract action items by keyword match (case-insensitive)
    - Extract topics as hashtags (#finance, #health, etc.)
    - Log how many action items were found
    """
    out_dir = ensure_dir(output_dir)
    out_path = out_dir / "notes_extracted.json"

    action_items: List[str] = []
    topics: Dict[str, int] = {}
    total_lines = 0

    with open(notes_path, encoding="utf-8") as f:
        for line in f:
            total_lines += 1
            s = line.strip()
            if not s:
                continue

            upper = s.upper()
            if any(k in upper for k in ACTION_KEYWORDS):
                action_items.append(s)

            for token in s.split():
                if token.startswith("#") and len(token) > 1:
                    topics[token] = topics.get(token, 0) + 1

    payload = {
        "action_items": action_items,
        "topics": topics,
        "total_lines": total_lines,
    }

    # TODO: write payload to out_path as JSON (pretty-printed)
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False),encoding="utf-8")
    logging.info("Ingest notes: action_items=%s topics=%s", len(action_items), len(topics))
    return out_path


def load_profile(profile_path: str | None) -> dict:
    """Load optional profile.json safely.

    TODO:
    - If profile_path is None or file missing, return {}
    - Must NOT crash
    """
    if not profile_path:
        return {}
    p = Path(profile_path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def run_ingest(csv_path: str, notes_path: str, profile_path: str | None, output_dir: str) -> dict:
    """Run ingestion for all inputs and return a small manifest dict."""
    cleaned_path, rejected_path = ingest_csv(csv_path, output_dir)
    notes_out = ingest_notes(notes_path, output_dir)
    profile = load_profile(profile_path)

    manifest = {
        "cleaned_csv": str(cleaned_path),
        "rejected_csv": str(rejected_path),
        "notes_json": str(notes_out),
        "profile_loaded": bool(profile),
    }
    return manifest
