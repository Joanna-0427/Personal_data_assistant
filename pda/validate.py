from __future__ import annotations

import re
from typing import Any, Dict, Optional, Tuple

DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def validate_date(date_str: str) -> bool:
    """Return True if date_str matches YYYY-MM-DD.

    TODO:
    - Keep regex-based validation (required)
    - Optionally add semantic validation (month/day ranges) as stretch
    """
    return bool(DATE_PATTERN.match((date_str or "").strip()))


def parse_amount(value: Any) -> float:
    """Parse amount to float and validate range.

    Rules:
    - Must convert to float
    - Must be within [-100000, 100000]
    """
    amount = float(value)
    if not (-100000 <= amount <= 100000):
        raise ValueError("Amount out of range")
    return round(amount, 2)


def validate_row(row: Dict[str, Any]) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    """Validate and clean a CSV row.

    Returns:
      (is_valid, cleaned_row, error_reason)

    TODO:
    - Validate required fields: date, amount, category
    - Strip whitespace
    - Provide helpful error_reason
    - Keep this function PURE (no file I/O)
    """
    try:
        date = (row.get("date") or "").strip()
        amt_raw = row.get("amount")
        category = (row.get("category") or "").strip()
        description = (row.get("description") or "").strip()

        if not validate_date(date):
            return False, None, "Invalid date format (expected YYYY-MM-DD)"

        amount = parse_amount(amt_raw)

        if not category:
            return False, None, "Empty category"

        cleaned = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description,
        }
        return True, cleaned, None

    except Exception as e:
        return False, None, str(e)
