from __future__ import annotations

import logging
from pathlib import Path

def setup_logger(log_file: str = "logs/app.log", level: int = logging.INFO) -> None:
    """Configure logging to both console and a file.

    TODO:
    - Ensure parent folder exists
    - Include timestamps and log levels
    - Add a DEBUG mode option in CLI (optional)
    """
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )


def ensure_dir(path: str) -> Path:
    """Create directory if missing and return Path."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p
