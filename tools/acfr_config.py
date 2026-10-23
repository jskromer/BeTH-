"""Explicit source-year configuration; no inference of years from ledger values."""
import json
from pathlib import Path

CONFIG_DIR = Path(__file__).resolve().parent / 'acfr_years'


def load_year(year=2025):
    path = CONFIG_DIR / f'{int(year)}.json'
    with path.open() as stream:
        config = json.load(stream)
    if config['fiscal_year'] != int(year):
        raise ValueError(f'Fiscal year mismatch in {path}')
    return config
