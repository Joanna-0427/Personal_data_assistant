from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

import requests

from .utils import ensure_dir


def cache_get(cache_dir: str, key: str) -> Optional[dict]:
    """Return cached payload if exists, else None."""
    p = Path(cache_dir) / f"{key}.json"
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def cache_set(cache_dir: str, key: str, payload: dict) -> Path:
    """Write payload to cache and return path."""
    ensure_dir(cache_dir)
    p = Path(cache_dir) / f"{key}.json"
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return p


def fetch_exchange_rate(base: str, target: str) -> float:
    """Fetch FX rate from a public endpoint.

    TODO:
    - Add robust error handling for non-200, JSON errors
    - Use timeout (required)
    - Consider retry (optional stretch)
    """
    url = "https://api.exchangerate.host/latest"
    resp = requests.get(url, params={"base": base}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    rate = float(data["rates"][target])
    return rate


def enrich_summary_with_fx(summary_path: str, cache_dir: str, base: str = "USD", target: str = "EUR") -> dict:
    """Example enrichment: add FX rate info to summary.json.

    Required features:
    - Cache hit/miss logging
    - API failure should NOT crash pipeline; must fallback gracefully

    TODO:
    - Read summary.json
    - Get FX rate (cache first, otherwise API)
    - Add fields under summary['enrichment']
    - Write summary.json back (or write a new enriched_summary.json)
    """
    cache_key = f"fx_{base}_{target}".lower()
    cached = cache_get(cache_dir, cache_key)

    if cached and "rate" in cached:
        logging.info("FX cache hit: %s", cache_key)
        rate = float(cached["rate"])
        source = "cache"
    else:
        logging.info("FX cache miss: %s", cache_key)
        try:
            rate = fetch_exchange_rate(base, target)
            cache_set(cache_dir, cache_key, {"rate": rate})
            source = "api"
        except Exception as e:
            logging.error("FX API failed: %s", e)
            rate = None
            source = "failed"

    p = Path(summary_path)
    summary = json.loads(p.read_text(encoding="utf-8"))
    summary["enrichment"] = {
        "type": "exchange_rate",
        "base": base,
        "target": target,
        "rate": rate,
        "source": source,
    }

    # TODO: decide whether to overwrite summary.json or write a new file
    #write stored_data'summary.json' to a file
    p.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    #return stored_data to use directly
    return summary


def run_enrich(input_dir: str, api_name: str, cache_dir: str) -> Path:
    """Entry point for enrich command.

    Currently supports:
    - exchangerate: enrich summary.json with FX rate info

    TODO:
    - Add more tools (weather, wiki) as stretch
    """
    input_dir_p = Path(input_dir)
    summary_path = str(input_dir_p / "summary.json")

    if api_name == "exchangerate":
        enrich_summary_with_fx(summary_path, cache_dir, base="USD", target="EUR")
        return Path(summary_path)

    raise ValueError(f"Unsupported api: {api_name}")
