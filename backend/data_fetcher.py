"""
Fetches real macroeconomic data from the FRED API (Federal Reserve Economic Data).

Get a free API key at: https://fred.stlouisfed.org/docs/api/api_key.html
Set it as environment variable: FRED_API_KEY=your_key_here
"""

import os
import requests
import datetime

FRED_API_KEY = os.environ.get('FRED_API_KEY', '')
FRED_BASE_URL = 'https://api.stlouisfed.org/fred/series/observations'

# Map each theme to a FRED series and how to interpret it
FRED_SERIES = {
    "Inflation": {
        "series_id": "CPIAUCSL",       # Consumer Price Index
        "label": "CPI",
        "unit": "index",
        "hot_direction": "up",          # Rising CPI = HOT
    },
    "GDP": {
        "series_id": "GDP",             # Gross Domestic Product
        "label": "GDP",
        "unit": "billions $",
        "hot_direction": "down",        # Falling GDP = HOT (risk)
    },
    "Employment": {
        "series_id": "UNRATE",          # Unemployment Rate
        "label": "Unemployment Rate",
        "unit": "%",
        "hot_direction": "up",          # Rising unemployment = HOT (risk)
    },
    "Housing": {
        "series_id": "HOUST",           # Housing Starts
        "label": "Housing Starts",
        "unit": "thousands",
        "hot_direction": "down",        # Falling starts = HOT (risk)
    },
    "Tech": {
        "series_id": "NASDAQCOM",       # NASDAQ Composite
        "label": "NASDAQ",
        "unit": "index",
        "hot_direction": "down",        # Falling NASDAQ = HOT (risk)
    },
    "Energy": {
        "series_id": "DCOILWTICO",      # Crude Oil Price (WTI)
        "label": "Oil (WTI)",
        "unit": "$/barrel",
        "hot_direction": "up",          # Rising oil = HOT (risk)
    },
}


def fetch_series(series_id, limit=2):
    """Fetch the latest observations from FRED for a given series."""
    if not FRED_API_KEY:
        return None

    try:
        resp = requests.get(FRED_BASE_URL, params={
            'series_id': series_id,
            'api_key': FRED_API_KEY,
            'file_type': 'json',
            'sort_order': 'desc',
            'limit': limit,
        }, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        observations = data.get('observations', [])
        # Filter out missing values
        return [o for o in observations if o.get('value', '.') != '.']
    except Exception as e:
        print(f"[FRED] Error fetching {series_id}: {e}")
        return None


def fetch_all_themes():
    """
    Fetches real data for all themes. Returns a dict keyed by theme name:
    {
        "Inflation": {
            "current_value": 314.5,
            "previous_value": 313.2,
            "change_pct": 0.41,
            "label": "CPI",
            "unit": "index",
            "date": "2025-12-01",
            "sentiment_score": 0.85,
            "headline": "CPI at 314.5 (up 0.41% from previous period)"
        },
        ...
    }
    Returns None if FRED_API_KEY is not set.
    """
    if not FRED_API_KEY:
        return None

    results = {}
    for theme, config in FRED_SERIES.items():
        obs = fetch_series(config['series_id'])
        if not obs or len(obs) < 2:
            continue

        try:
            current = float(obs[0]['value'])
            previous = float(obs[1]['value'])
        except (ValueError, KeyError):
            continue

        change_pct = ((current - previous) / previous) * 100 if previous != 0 else 0

        # Calculate sentiment score based on direction of change
        # "hot_direction" tells us which direction means risk
        abs_change = abs(change_pct)
        if config['hot_direction'] == 'up':
            # Rising = risky
            if change_pct > 0:
                score = min(0.5 + abs_change * 0.1, 0.99)
            else:
                score = max(0.5 - abs_change * 0.1, 0.05)
        else:
            # Falling = risky
            if change_pct < 0:
                score = min(0.5 + abs_change * 0.1, 0.99)
            else:
                score = max(0.5 - abs_change * 0.1, 0.05)

        direction = "up" if change_pct > 0 else "down"
        headline = f"{config['label']} at {current:,.1f} ({direction} {abs(change_pct):.2f}% from previous period)"

        results[theme] = {
            "current_value": round(current, 2),
            "previous_value": round(previous, 2),
            "change_pct": round(change_pct, 2),
            "label": config['label'],
            "unit": config['unit'],
            "date": obs[0].get('date', ''),
            "sentiment_score": round(score, 2),
            "headline": headline,
        }

    return results if results else None


def is_available():
    """Returns True if FRED API key is configured."""
    return bool(FRED_API_KEY)
