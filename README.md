# Personal Data Assistant (PDA) — Starter Project

A Python foundations capstone that simulates an “agent-style” workflow:

**Ingest → Validate → Analyze → (Enrich via API) → Report → Logs**

You will implement a CLI that reads CSV/JSON/TXT, cleans and summarizes data, optionally calls a public API (as a “tool”), caches responses, and outputs artifacts.

---

## What you’ll build

### CLI commands
- `ingest` — read raw inputs, validate/clean, write processed artifacts
- `analyze` — compute stats + notes summary, write `summary.json`
- `enrich` — call 1 public API, cache results, write enriched outputs
- `run` — one-shot pipeline: ingest → analyze → (optional enrich) → report

### Required outputs
- `data/processed/cleaned_expenses.csv`
- `data/processed/rejected_rows.csv` *(recommended)*
- `data/processed/notes_extracted.json`
- `data/processed/summary.json`
- `reports/report.md`
- `logs/app.log`

---

## Repo structure

```
personal_data_assistant/
  pda/
    cli.py
    ingest.py
    validate.py
    analyze.py
    enrich.py
    report.py
    utils.py
  data/
    raw/
      expenses.csv
      notes.txt
      profile.json
    processed/
  reports/
  logs/
  cache/
  tests/
```

---

## Setup

### 1) Create and activate a virtual environment

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

---

## Quick start (using the provided sample inputs)

### Ingest
```bash
python -m pda.cli ingest   --csv data/raw/expenses.csv   --notes data/raw/notes.txt   --profile data/raw/profile.json   --out data/processed
```

### Analyze
```bash
python -m pda.cli analyze   --input data/processed  
```

### Enrich (pick one API tool)
```bash
python -m pda.cli enrich   --input data/processed   --api exchangerate   --cache cache
```

### Run pipeline (recommended)
```bash
python -m pda.cli run   --csv data/raw/expenses.csv   --notes data/raw/notes.txt   --profile data/raw/profile.json   --out data/processed   --report reports/report.md   --api exchangerate   --cache cache
```

---

## Sample data

This starter includes:
- `data/raw/expenses.csv` (contains valid + invalid rows for validation practice)
- `data/raw/notes.txt` (contains action items and #topics)
- `data/raw/profile.json` (optional config; program must work even if missing)

---

## Implementation checklist (definition of done)

- [ ] CLI works with `--help` and subcommands (`ingest`, `analyze`, `enrich`, `run`)
- [ ] Regex date validation (YYYY-MM-DD)
- [ ] Robust CSV parsing: invalid rows do not crash program
- [ ] Writes required artifacts and report
- [ ] Logging to `logs/app.log`
- [ ] API tool: timeout + non-200 handling + JSON parsing guard
- [ ] Caching: cache hit avoids extra API calls
- [ ] Tests: at least 8 unit tests pass

---

## Testing

Run:
```bash
python -m unittest -v
```

Or if you prefer `pytest`, you can add it and run:
```bash
pytest -q
```

---

## Notes

- You may use the Python standard library freely.
- Avoid heavy analysis libraries (pandas) for this capstone—practice core Python.

Good luck and build it like a tool an AI agent would use.
