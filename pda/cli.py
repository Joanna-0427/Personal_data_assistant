from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .utils import setup_logger
from .ingest import run_ingest
from .analyze import run_analyze
from .enrich import run_enrich
from .report import generate_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pda", description="Personal Data Assistant (PDA)")
    parser.add_argument("--log-file", default="logs/app.log", help="Log file path")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    sub = parser.add_subparsers(dest="command", required=True)

    p_ingest = sub.add_parser("ingest", help="Ingest raw inputs and write processed artifacts")
    p_ingest.add_argument("--csv", required=True, help="Path to expenses.csv")
    p_ingest.add_argument("--notes", required=True, help="Path to notes.txt")
    p_ingest.add_argument("--profile", default=None, help="Optional profile.json")
    p_ingest.add_argument("--out", default="data/processed", help="Output directory for processed artifacts")

    p_analyze = sub.add_parser("analyze", help="Analyze processed artifacts and write summary.json")
    p_analyze.add_argument("--input", required=True, help="Processed artifacts directory (data/processed)")

    p_enrich = sub.add_parser("enrich", help="Enrich summary using an API tool (with caching)")
    p_enrich.add_argument("--input", required=True, help="Processed artifacts directory (data/processed)")
    p_enrich.add_argument("--api", required=True, choices=["exchangerate"], help="Which tool/API to use")
    p_enrich.add_argument("--cache", default="cache", help="Cache directory")

    p_run = sub.add_parser("run", help="Run ingest → analyze → (optional enrich) → report")
    p_run.add_argument("--csv", required=True)
    p_run.add_argument("--notes", required=True)
    p_run.add_argument("--profile", default=None)
    p_run.add_argument("--out", default="data/processed")
    p_run.add_argument("--report", default="reports/report.md")
    p_run.add_argument("--api", default=None, choices=[None, "exchangerate"], help="Optional enrichment tool")
    p_run.add_argument("--cache", default="cache")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    level = logging.DEBUG if args.debug else logging.INFO
    setup_logger(args.log_file, level=level)

    if args.command == "ingest":
        run_ingest(args.csv, args.notes, args.profile, args.out)

    elif args.command == "analyze":
        run_analyze(args.input)

    elif args.command == "enrich":
        run_enrich(args.input, args.api, args.cache)

    elif args.command == "run":
        run_ingest(args.csv, args.notes, args.profile, args.out)
        summary_path = run_analyze(args.out)
        if args.api:
            run_enrich(args.out, args.api, args.cache)
        generate_report(str(summary_path), args.report)

    else:
        raise ValueError(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
